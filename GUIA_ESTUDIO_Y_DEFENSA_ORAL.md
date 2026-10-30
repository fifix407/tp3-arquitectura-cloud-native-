# Guía de Estudio y Defensa Oral: TP N° 3 (Arquitectura Cloud-Native)

**Materia:** Arquitectura de Sistemas – Licenciatura en Sistemas de Información (Ciclo 2026)  
**Caso de Estudio:** GlobalLogistics S.A.  
**Integrantes:** Lucía Astorga, Emmanuel Bustos, Santiago Militello  
**Repositorio GitHub:** [https://github.com/fifix407/tp3-arquitectura-cloud-native-](https://github.com/fifix407/tp3-arquitectura-cloud-native-)

---

## 🎯 1. ¿Cuál era el objetivo del trabajo?
La empresa ficticia **GlobalLogistics S.A.** necesitaba desplegar una nueva arquitectura de microservicios para rastreo de flotas y paquetes, asegurando que:
1. La infraestructura sea **Cloud-Native** y reproducible mediante **Infraestructura como Código (IaC)**.
2. Soporte **escalabilidad horizontal** sin intervención manual.
3. Tenga alta disponibilidad y resiliencia con **balanceo de carga y Health Checks**.
4. Se validen atributos de calidad no funcionales (**latencia**, **tiempo de respuesta** y **concurrencia**) mediante pruebas de carga reales con **Apache Benchmark**.

---

## 🏗️ 2. ¿Cómo está armada la arquitectura? (Visión General)

La solución corre sobre **Docker** y se divide en 3 capas fundamentales:

```
               [ Cliente / Navegador / Apache Benchmark ]
                                   │
                           Puerto :8080
                                   ▼
        ┌──────────────────────────────────────────────────────┐
        │        Balanceador de Carga Nginx (Reverse Proxy)     │
        │           Contenedor: globallogistics_loadbalancer   │
        │           Algoritmo: Round-Robin                     │
        │           Health Checks: pasivos (max_fails=3)       │
        └──────────────────────────┬───────────────────────────┘
                                   │ Red virtual bridge: globallogistics_net
                ┌──────────────────┼──────────────────┐
                ▼                  ▼                  ▼
       ┌─────────────────┐┌─────────────────┐┌─────────────────┐
       │   Réplica 1     ││   Réplica 2     ││   Réplica 3     │
       │ globallogistics ││ globallogistics ││ globallogistics │
       │     _app_1      ││     _app_2      ││     _app_3      │
       │ Python/FastAPI  ││ Python/FastAPI  ││ Python/FastAPI  │
       │ CPU: 0.5 Cores  ││ CPU: 0.5 Cores  ││ CPU: 0.5 Cores  │
       │ RAM: 512 MB     ││ RAM: 512 MB     ││ RAM: 512 MB     │
       └─────────────────┘└─────────────────┘└─────────────────┘
```

### Componentes Clave:
1. **Red Virtual (`globallogistics_net`):** Una red privada tipo *bridge*. Ninguna réplica expone sus puertos directamente a Windows; solo el balanceador Nginx tiene acceso directo a ellas. Esto añade una capa de seguridad.
2. **Reverse Proxy (Nginx en Alpine Linux):** Recibe las peticiones en el puerto `8080` y las reparte cíclicamente entre las 3 réplicas.
3. **Microservicio REST (FastAPI + Uvicorn en Python 3.12-slim):** API liviana y asíncrona con tres endpoints:
   * `GET /`: Devuelve obligatoriamente el **Hostname / Container ID** de la instancia asignada.
   * `GET /health`: Diagnóstico de salud (uptime, memoria RAM consumida).
   * `GET /stress`: Endpoint con cómputo criptográfico intensivo (SHA-256) para simular saturación de CPU.

---

## 💻 3. Detalle de lo que se hizo código por código

### A. Infraestructura como Código (`docker-compose.yml`)
* Define 4 servicios: `loadbalancer`, `app1`, `app2` y `app3`.
* Usa la directiva `depends_on` con condición `service_healthy`. Esto significa que Nginx **no arranca hasta que las 3 réplicas respondan "OK" en sus chequeos de salud**.
* Usa límites de recursos en cada réplica:
  ```yaml
  deploy:
    resources:
      limits:
        cpus: '0.50'
        memory: 512M
  ```
  *¿Por qué pusimos este límite?* Para que el comportamiento de saturación bajo estrés sea predecible y medible en el laboratorio sin congelar la máquina anfitriona.

### B. Microservicio (`microservice/main.py`)
* Programado con FastAPI.
* En el endpoint raíz `/` se obtiene el identificador único del contenedor con:
  ```python
  import socket
  container_id = socket.gethostname()
  ```
  En Docker, el `hostname` predeterminado de un contenedor es exactamente su **ID de contenedor** (los primeros 12 caracteres hexadecimales, por ejemplo `4b2d0d7b0413`).

### C. Balanceador y Health Checks (`nginx/nginx.conf`)
* **Upstream:**
  ```nginx
  upstream microservices_backend {
      server app1:8000 max_fails=3 fail_timeout=10s;
      server app2:8000 max_fails=3 fail_timeout=10s;
      server app3:8000 max_fails=3 fail_timeout=10s;
      keepalive 32;
  }
  ```
* **Mecanismo de Resiliencia (`proxy_next_upstream`):**
  Si una réplica se cae o devuelve error 500/502/503/timeout, Nginx reintenta la petición instantáneamente en otra réplica viva sin que el usuario reciba un error.

---

## 📊 4. Las Pruebas de Carga con Apache Benchmark (Consigna 3)

Se ejecutaron pruebas reales usando el contenedor oficial `httpd:alpine` dentro de la misma red de Docker.

### Escenario 1: Concurrencia Moderada (I/O Ligero)
* **Condiciones:** 5.000 peticiones, 100 usuarios concurrentes al endpoint principal (`GET /`).
* **Resultados reales:**
  * Throughput: **561 req/segundo**.
  * Latencia promedio: **178 ms**.
  * Mediana (p50): **39 ms** (el 50% de las peticiones tardó menos de 39 milisegundos).
  * Percentil 95 (p95): **966 ms**.
  * Percentil 99 (p99): **2.713 ms**.
  * Tasa de error: **0% (100% de peticiones exitosas)**.

### Escenario 2: Concurrencia Extrema (Saturación de CPU)
* **Condiciones:** 2.500 peticiones, 100 usuarios concurrentes al endpoint de estrés (`GET /stress?iterations=2500`).
* **Resultados reales:**
  * Throughput: Cayó a **170 req/segundo** (🔻 **-69.5%** de capacidad).
  * Latencia promedio: Subió a **585 ms** (🔺 **+228%** de aumento).
  * Mediana (p50): **177 ms**.
  * Percentil 95 (p95): **3.016 ms (más de 3 segundos)**.
  * Percentil 99 (p99): **6.258 ms (más de 6 segundos)**.
  * Tasa de éxito: **92.5%** (comenzaron a formarse colas de espera en los buffers TCP).

---

## 🧠 5. Análisis Crítico: ¿Qué significan estos números? (Para la defensa)

### ¿En qué punto se degrada el sistema?
El sistema se comporta de forma lineal y elástica mientras las operaciones sean de Entrada/Salida (I/O). El **punto de degradación** ocurre cuando las 100 peticiones simultáneas compiten por los 1.5 núcleos virtuales disponibles (0.5 CPU x 3 réplicas). Al saturarse la CPU, el planificador del kernel Linux (*CFS Throttling*) suspende temporalmente los contenedores que agotaron su cuota, haciendo que las peticiones se encolen en el socket y la latencia se dispare de forma casi exponencial.

### ¿Cumple con restricciones de Tiempo Real?
* **Tiempo Real Estricto (Hard Real-Time):** **NO cumple**. En estos sistemas, pasarse de un plazo (deadline, ej. < 50 ms) es una falla catastrófica. Debido a la variabilidad del sistema operativo y Docker, el p99 llega a más de 2 segundos.
* **Tiempo Real Blando (Soft Real-Time / Web Transaccional):**
  * En **carga moderada CUMPLE** con los Acuerdos de Nivel de Servicio (SLA estándar de la industria: p95 < 1.000 ms; obtuvimos 966 ms).
  * En **saturación de CPU NO CUMPLE**, ya que tiempos de 3 a 6 segundos provocarían desconexiones y carritos de compra/rastreos caídos en una aplicación comercial real.

### ¿Cuál es la solución recomendada como Arquitectos Cloud?
Pasar de un escalado estático a un orquestador como **Kubernetes** con **HPA (Horizontal Pod Autoscaler)**, que monitoree el uso de CPU y cuando supere el 70%, cree automáticamente más réplicas (por ejemplo de 3 a 10 réplicas).

---

## ❓ 6. Banco de Preguntas y Respuestas para los Profesores

### P1: "¿Por qué usaron Round-Robin como algoritmo de balanceo?"
> **Respuesta:** "Usamos Round-Robin porque es el algoritmo estándar y equitativo para microservicios con réplicas de igual capacidad de hardware. Sin embargo, en nuestro análisis crítico explicamos que ante peticiones de duración variable (cálculo pesado de rutas), un algoritmo como `least_conn` (mínimas conexiones activas) habría sido más eficiente para evitar mandar trabajo a un contenedor que ya tiene una tarea pesada en ejecución."

### P2: "¿Cómo garantiza Nginx la alta disponibilidad si una réplica se apaga?"
> **Respuesta:** "Mediante dos directivas en `nginx.conf`:
> 1. `max_fails=3` y `fail_timeout=10s`: si un contenedor falla 3 veces seguidas, Nginx lo saca del pool de servidores activos durante 10 segundos.
> 2. `proxy_next_upstream`: si una réplica falla al intentar responder, Nginx no le devuelve el error 502 al cliente; en su lugar, reenvía esa misma petición de inmediato a otra de las réplicas disponibles, logrando tolerancia a fallos con cero impacto para el usuario."

### P3: "¿Por qué en el endpoint devuelven el Hostname y dicen que es el Container ID?"
> **Respuesta:** "Porque en los contenedores Docker basados en Linux, el motor de Docker asigna de forma predeterminada los primeros 12 caracteres del hash del contenedor como el Hostname del sistema operativo dentro del namespace. Al invocar `socket.gethostname()` en Python, obtenemos con precisión el identificador único del contenedor donde se está ejecutando la instancia."

### P4: "¿Qué diferencia hay entre la latencia promedio y los percentiles p95 o p99?"
> **Respuesta:** "El promedio puede ocultar anomalías porque un 90% de peticiones muy rápidas enmascara a los usuarios que sufrieron demoras extremas. Los percentiles p95 y p99 indican el peor escenario que experimenta el 5% y el 1% de los usuarios respectivamente. En la ingeniería de software moderna, los SLAs se miden en p95 y p99 para garantizar la calidad de servicio en la cola larga de latencia."

### P5: "¿Por qué ejecutaron Apache Benchmark desde un contenedor dentro de la misma red de Docker?"
> **Respuesta:** "Para aislar la prueba de variables externas como la latencia de la placa de red física del host, firewalls de Windows o el stack de virtualización del puerto expuesto. Al ejecutar `ab` en un contenedor dentro de `globallogistics_net`, medimos con máxima precisión el rendimiento puro del balanceador y las réplicas."

### P6: "¿Cómo se levanta todo el proyecto desde cero?"
> **Respuesta:** "Con un solo comando de Infraestructura como Código: `docker compose up -d --build`. Docker Compose se encarga de crear la red virtual, compilar las imágenes de Nginx y Python, verificar los Health Checks de las réplicas y, una vez saludables, activar el balanceador en el puerto 8080."
