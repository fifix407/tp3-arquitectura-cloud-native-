# Trabajo Práctico N° 3: Despliegue de Arquitectura Cloud-Native

**Licenciatura en Sistemas de Información – Arquitectura de Sistemas (Ciclo 2026)**  
**Estudiante:** Santiago Militello  
**Caso de Estudio:** GlobalLogistics S.A. – Plataforma Distribuida de Rastreo y Telemetría  
**Repositorio GitHub:** [https://github.com/fifix407/tp3-arquitectura-cloud-native](https://github.com/fifix407/tp3-arquitectura-cloud-native)

---

## 📋 Descripción del Proyecto

Este proyecto implementa una solución de infraestructura como código (**IaC**) basada en contenedores Docker y orquestación con Docker Compose. Se diseñó y desplegó una arquitectura de microservicios resiliente, escalable y balanceada para la empresa ficticia **GlobalLogistics S.A.**, orientada a soportar alta demanda transaccional y verificar atributos de calidad no funcionales (**latencia**, **tiempo de respuesta** y **disponibilidad**).

### Componentes de la Arquitectura
* **Balanceador de Carga (Reverse Proxy):** Nginx (1 instancia) con algoritmo **Round-Robin**, balanceo de carga L7, encabezados de trazabilidad y **Health Checks pasivos**.
* **Clúster de Microservicios:** 3 réplicas idénticas de una API REST de alto rendimiento en **Python 3.12 (FastAPI + Uvicorn)** con endpoints de negocio, diagnóstico y estrés computacional.
* **Red Aislada (Bridge):** Red virtual privada `globallogistics_net` para comunicación interna segura entre el proxy y los backends.

---

## 🏗️ Estructura del Repositorio

```text
.
├── docker-compose.yml          # Manifiesto de Infraestructura como Código (IaC)
├── .env.example                # Variables de entorno de ejemplo (puertos)
├── .env                        # Variables de configuración local
├── README.md                   # Documentación y guía de reproducción
├── nginx/
│   ├── Dockerfile              # Imagen basada en nginx:alpine
│   └── nginx.conf              # Configuración de upstream, balanceo y health checks
├── microservice/
│   ├── Dockerfile              # Imagen optimizada en python:3.12-slim
│   ├── requirements.txt        # Dependencias (FastAPI, Uvicorn)
│   └── main.py                 # Endpoints /, /health y /stress
├── scripts/
│   ├── run_benchmarks.py       # Automatización de pruebas de carga con Apache Benchmark
│   └── verify_loadbalancing.ps1# Script para verificar rotación de Container IDs
└── benchmark_results/
    ├── summary.json            # Métricas consolidadas (latencias, RPS, percentiles)
    ├── scenario1_concurrencia_moderada.txt # Salida cruda de Apache Benchmark (Escenario 1)
    └── scenario2_concurrencia_extrema.txt  # Salida cruda de Apache Benchmark (Escenario 2)
```

---

## 🚀 Instrucciones de Ejecución

### Prerrequisitos
* **Docker Desktop** (con Docker Engine 24+ y Docker Compose v2+ instalado y en ejecución).
* Sistema Operativo: Windows, Linux o macOS.
* Python 3.10+ (opcional, para ejecutar los scripts de automatización).

### 1. Clonar el Repositorio
```bash
git clone https://github.com/fifix407/tp3-arquitectura-cloud-native.git
cd tp3-arquitectura-cloud-native
```

### 2. Configurar Variables de Entorno (Opcional)
Por defecto, el balanceador de carga expone el puerto `8080` para evitar colisiones con servidores web locales (IIS/Apache/HTTP.sys en Windows). Si desea utilizar el puerto `80`, edite el archivo `.env`:
```ini
LB_PORT=8080
```

### 3. Levantar los Servicios con Docker Compose
Ejecute el comando solicitado en la consigna:
```bash
docker compose up -d --build
```

Verifique que se hayan iniciado exactamente **un (1) balanceador** y **tres (3) réplicas**:
```bash
docker ps --filter "name=globallogistics"
```

Salida esperada:
```text
CONTAINER ID   IMAGE                         PORTS                  NAMES
xxxxxxxxxxxx   agitated-volta-loadbalancer   0.0.0.0:8080->80/tcp   globallogistics_loadbalancer
xxxxxxxxxxxx   agitated-volta-app1           8000/tcp (healthy)     globallogistics_app_1
xxxxxxxxxxxx   agitated-volta-app2           8000/tcp (healthy)     globallogistics_app_2
xxxxxxxxxxxx   agitated-volta-app3           8000/tcp (healthy)     globallogistics_app_3
```

---

## 🔍 Verificación del Microservicio y Balanceo de Carga

### 1. Petición al Endpoint Principal
El endpoint principal devuelve obligatoriamente el **Hostname / Container ID** de la instancia asignada:
```bash
curl http://localhost:8080/
```
Respuesta JSON:
```json
{
  "status": "success",
  "service": "GlobalLogistics S.A. - Fleet & Tracking Service",
  "container_id": "4b2d0d7b0413",
  "hostname": "4b2d0d7b0413",
  "instance_name": "microservice-replica-1",
  "client_ip": "172.18.0.5",
  "timestamp": "2026-10-28T21:15:36.123456+00:00",
  "architecture": "Cloud-Native Microservices",
  "load_balanced": true
}
```

### 2. Comprobación de Rotación Round-Robin
Ejecute peticiones consecutivas mediante el script provisto:
* En **PowerShell**:
  ```powershell
  powershell -ExecutionPolicy Bypass -File scripts\verify_loadbalancing.ps1
  ```
* En **Bash / Linux**:
  ```bash
  for i in {1..6}; do curl -s http://localhost:8080/ | jq .container_id; done
  ```

Se observará que cada petición sucesiva es atendida por un ID de contenedor diferente en ciclo estricto (`replica-1` ➔ `replica-2` ➔ `replica-3` ➔ `replica-1`).

### 3. Health Checks y Tolerancia a Fallos
Si una de las réplicas se detiene forzosamente:
```bash
docker stop globallogistics_app_2
```
Nginx detecta la falla mediante las directivas `max_fails=3 fail_timeout=10s` y redirige el tráfico automáticamente a las réplicas activas (`app1` y `app3`) con cero tiempo de inactividad (**Zero Downtime**). Al reiniciar la réplica:
```bash
docker start globallogistics_app_2
```
Docker Compose evalúa el `HEALTHCHECK` interno de la API (`/health`) y, una vez saludable, Nginx la reincorpora transparentemente al pool de balanceo.

---

## 📊 Reproducción de Pruebas de Carga y Estrés (Consigna 3)

Las pruebas se ejecutan utilizando la imagen oficial de **Apache Benchmark** en Docker (`httpd:alpine`), garantizando reproducibilidad sin requerir herramientas instaladas en el host.

### Ejecución Automática (Suite Completa)
```bash
python scripts/run_benchmarks.py
```

### Ejecución Manual de Escenarios

#### Escenario 1: Concurrencia Moderada (100 usuarios concurrentes, 5000 peticiones)
```bash
docker run --rm --network globallogistics_net httpd:alpine ab -n 5000 -c 100 http://globallogistics_loadbalancer/
```

#### Escenario 2: Concurrencia Extrema / Saturación de CPU (100 usuarios concurrentes, 2500 peticiones con carga CPU-bound)
```bash
docker run --rm --network globallogistics_net httpd:alpine ab -n 2500 -c 100 http://globallogistics_loadbalancer/stress?iterations=2500
```

---

## 📈 Resumen de Resultados de Rendimiento

| Métrica Temporal / Atributo | Escenario 1: Concurrencia Moderada | Escenario 2: Concurrencia Extrema (Saturación CPU) | Variación Relativa |
| :--- | :---: | :---: | :---: |
| **Peticiones Totales** | 5.000 | 2.500 | - |
| **Concurrencia (-c)** | 100 usuarios concurrentes | 100 usuarios concurrentes | - |
| **Throughput (RPS)** | **561.04 req/seg** | **170.70 req/seg** | 🔻 **-69.5%** |
| **Latencia Promedio (Mean)** | **178.24 ms** | **585.83 ms** | 🔺 **+228.7%** |
| **Mediana (Percentil 50)** | **39 ms** | **177 ms** | 🔺 **+353.8%** |
| **Percentil 95 (p95)** | **966 ms** | **3.016 ms** | 🔺 **+212.2%** |
| **Percentil 99 (p99)** | **2.713 ms** | **6.258 ms** | 🔺 **+130.7%** |
| **Tasa de Disponibilidad (2xx)** | **100.00%** | **92.52%** | Degradación por cola |

Para un análisis técnico detallado, justificación arquitectónica y evaluación de sistemas de tiempo real, consulte el **Reporte Formal en PDF** adjunto en la entrega.

---

## 🛑 Detener y Limpiar el Entorno

```bash
docker compose down -v
```
