import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import parse_xml
from docx.oxml.ns import nsdecls
import os
from pathlib import Path

desktop = Path(os.environ["USERPROFILE"]) / "OneDrive" / "Escritorio"
if not desktop.exists():
    desktop = Path(os.environ["USERPROFILE"]) / "Desktop"

output_path = desktop / "GUIA_DEFINITIVA_DEFENSA_ORAL_TP3.docx"

doc = docx.Document()

# Márgenes amplios y limpios
for section in doc.sections:
    section.top_margin = Inches(0.7)
    section.bottom_margin = Inches(0.7)
    section.left_margin = Inches(0.75)
    section.right_margin = Inches(0.75)

COLOR_PRIMARY = RGBColor(26, 54, 93)      # Azul Marino #1a365d
COLOR_SECONDARY = RGBColor(43, 108, 176)  # Azul Medio #2b6cb0
COLOR_TEXT = RGBColor(45, 55, 72)         # Gris Oscuro #2d3748
COLOR_GRAY = RGBColor(113, 128, 150)      # Gris Claro
COLOR_RED = RGBColor(197, 48, 48)         # Rojo #c53030
COLOR_GREEN = RGBColor(39, 103, 73)       # Verde #276749
COLOR_ORANGE = RGBColor(192, 86, 33)     # Naranja

def set_cell_background(cell, fill_hex):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_hex}"/>')
    tcPr.append(shd)

def add_box(doc, title, text_list, bg_hex="F8FAFC", border_hex="3182CE", title_color=COLOR_PRIMARY):
    table = doc.add_table(rows=1, cols=1)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    cell = table.cell(0, 0)
    set_cell_background(cell, bg_hex)
    
    tcPr = cell._tc.get_or_add_tcPr()
    tcBorders = parse_xml(
        f'<w:tcBorders {nsdecls("w")}>'
        f'<w:top w:val="single" w:sz="6" w:space="0" w:color="{border_hex}"/>'
        f'<w:left w:val="single" w:sz="24" w:space="0" w:color="{border_hex}"/>'
        f'<w:bottom w:val="single" w:sz="6" w:space="0" w:color="{border_hex}"/>'
        f'<w:right w:val="single" w:sz="6" w:space="0" w:color="{border_hex}"/>'
        f'</w:tcBorders>'
    )
    tcPr.append(tcBorders)
    
    p = cell.paragraphs[0]
    p.paragraph_format.space_before = Pt(3)
    p.paragraph_format.space_after = Pt(2)
    r_t = p.add_run(title)
    r_t.font.name = "Segoe UI"
    r_t.font.bold = True
    r_t.font.size = Pt(9.5)
    r_t.font.color.rgb = title_color
    
    for t in text_list:
        p_c = cell.add_paragraph()
        p_c.paragraph_format.space_before = Pt(2)
        p_c.paragraph_format.space_after = Pt(2)
        p_c.paragraph_format.line_spacing = 1.15
        r_c = p_c.add_run(t)
        r_c.font.name = "Segoe UI"
        r_c.font.size = Pt(9)
        r_c.font.color.rgb = COLOR_TEXT
        
    doc.add_paragraph().paragraph_format.space_after = Pt(4)

# ------------------------------------------------------------------------------
# ENCABEZADO
# ------------------------------------------------------------------------------
p_univ = doc.add_paragraph()
r_univ = p_univ.add_run("UNIVERSIDAD CHAMPAGNAT — LICENCIATURA EN SISTEMAS DE INFORMACIÓN (2026)")
r_univ.font.name = "Segoe UI"
r_univ.font.size = Pt(8.5)
r_univ.font.bold = True
r_univ.font.color.rgb = COLOR_GRAY
p_univ.paragraph_format.space_after = Pt(2)

p_title = doc.add_paragraph()
r_title = p_title.add_run("Guión de Defensa Oral Consigna a Consigna (TP N° 3)")
r_title.font.name = "Segoe UI"
r_title.font.size = Pt(17)
r_title.font.bold = True
r_title.font.color.rgb = COLOR_PRIMARY
p_title.paragraph_format.space_after = Pt(2)

p_sub = doc.add_paragraph()
r_sub = p_sub.add_run("Estructura Idéntica al Trabajo Práctico: Qué pide la consigna, qué se hizo y las palabras exactas para explicarlo al profesor")
r_sub.font.name = "Segoe UI"
r_sub.font.size = Pt(10)
r_sub.font.color.rgb = COLOR_SECONDARY
p_sub.paragraph_format.space_after = Pt(8)

# ------------------------------------------------------------------------------
# CONTEXTO PREVIO: EL CASO DE ESTUDIO
# ------------------------------------------------------------------------------
h0 = doc.add_heading("Contexto Inicial: El Desafío de GlobalLogistics S.A.", level=1)
h0.paragraph_format.space_before = Pt(8)
h0.paragraph_format.space_after = Pt(4)

add_box(
    doc,
    "📌 ¿QUÉ PIDE LA CONSIGNA GENERAL?",
    [
        "\"El equipo de ingeniería de GlobalLogistics S.A. ha diseñado la nueva arquitectura distribuida, pero ahora debe asegurar que la infraestructura soporte las operaciones. Como Arquitectos Cloud, el desafío consiste en desplegar un entorno de prueba que demuestre que el sistema escala horizontalmente sin intervención manual y mantiene tiempos de respuesta estables bajo estrés comercial.\""
    ],
    bg_hex="F7FAFC",
    border_hex="2B6CB0"
)

add_box(
    doc,
    "🗣️ CÓMO EXPLICARLO CON TUS PALABRAS AL EMPEZAR LA DEFENSA:",
    [
        "\"Buenas tardes profesores. Para este TP3 asumimos el rol de Arquitectos Cloud para GlobalLogistics S.A., una empresa de rastreo y logística en tiempo real.\"",
        "\"El objetivo principal no era solo programar una API, sino garantizar los atributos de calidad de la arquitectura: certificar que el sistema soporte alta concurrencia sin intervención manual, verificar que el balanceo reparta el trabajo equitativamente, comprobar la tolerancia a fallos ante la caída de un servidor, y someter el clúster a pruebas de estrés para contrastarlo rigurosamente contra el SLA del TP2 (responder en menos de 300 ms sin errores).\""
    ],
    bg_hex="EBF8FF",
    border_hex="3182CE",
    title_color=COLOR_GREEN
)

# ------------------------------------------------------------------------------
# CONSIGNA 1: CONFIGURACIÓN DEL ENTORNO E IAC
# ------------------------------------------------------------------------------
h1 = doc.add_heading("Consigna 1: Configuración del Entorno e IaC (30 Puntos)", level=1)
h1.paragraph_format.space_before = Pt(14)
h1.paragraph_format.space_after = Pt(4)

add_box(
    doc,
    "📌 ¿QUÉ PIDE TEXTUALMENTE LA CONSIGNA 1?",
    [
        "\"Desarrollen los manifiestos de Infraestructura como Código (docker-compose.yml) necesarios para levantar los servicios de forma automatizada.\"",
        "Entregable: Código fuente de los manifiestos. Deben asegurar que la configuración levante exactamente un (1) balanceador de carga y tres (3) réplicas del microservicio."
    ],
    bg_hex="F7FAFC",
    border_hex="2B6CB0"
)

add_box(
    doc,
    "⚙️ ¿QUÉ HICIMOS TÉCNICAMENTE EN EL PROYECTO?",
    [
        "1. Archivo docker-compose.yml: Define en código declarativo 4 servicios: 'loadbalancer' (Nginx en puerto 8080) y 3 réplicas idénticas ('app1', 'app2', 'app3') basadas en Python 3.12 y FastAPI.",
        "2. Red Virtual Privada (globallogistics_net): Creamos una red tipo bridge aislada. Las 3 réplicas no publican puertos a Windows (0.0.0.0), solo Nginx tiene acceso a ellas por el puerto interno 8000.",
        "3. Límites Estrictos de Recursos: En la sección deploy.resources.limits fijamos exactamente cpus: '0.50' y memory: 512M por réplica, para poder evaluar el comportamiento de saturación bajo estrés.",
        "4. Arranque Condicional por Salud (depends_on con condition: service_healthy): Nginx no expone su puerto ni arranca hasta que las 3 réplicas superen su prueba interna de Health Check en /health."
    ],
    bg_hex="F8FAFC",
    border_hex="4A5568"
)

add_box(
    doc,
    "🗣️ CÓMO EXPLICAR LA CONSIGNA 1 FRENTE AL PROFESOR (PALABRA POR PALABRA):",
    [
        "\"En la Consigna 1 implementamos Infraestructura como Código (IaC) mediante el manifiesto docker-compose.yml. En lugar de configurar servidores a mano, la infraestructura completa es declarativa y reproducible con un único comando: docker compose up -d.\"",
        "\"El clúster levanta exactamente un balanceador Nginx y tres réplicas del microservicio. Aplicamos tres principios arquitectónicos clave:\n"
        "1) Seguridad y aislamiento de red: las réplicas no exponen puertos al host físico, solo se comunican internamente con Nginx en la red globallogistics_net.\n"
        "2) Aislamiento de recursos: a cada réplica le restringimos la potencia a 0.5 CPU y 512MB RAM para observar de forma controlada el punto de saturación bajo estrés.\n"
        "3) Arranque condicional basado en salud: con la directiva condition: service_healthy, Nginx no comienza a despachar tráfico hasta que las tres réplicas hayan superado exitosamente su prueba de vida en /health, evitando errores 502 en el despliegue inicial.\"",
        "\"En el informe adjuntamos el código fuente completo del manifiesto y la Captura 1 de la terminal con 'docker compose ps' mostrando los 4 contenedores en estado Up y healthy.\""
    ],
    bg_hex="EBF8FF",
    border_hex="3182CE",
    title_color=COLOR_GREEN
)

add_box(
    doc,
    "❓ PREGUNTA TÍPICA DE EXAMEN SOBRE CONSIGNA 1:",
    [
        "Profesor: '¿Por qué limitaron la CPU a 0.50 en lugar de dejar que use todo lo que pueda el procesador?'",
        "Tu respuesta: 'Lo limitamos a propósito a 0.50 CPU para simular una arquitectura de microservicios realista en la nube (como contenedores en AWS ECS o Kubernetes con recursos acotados). Si dejábamos la CPU ilimitada, las tres réplicas consumirían todos los núcleos de la laptop host y no podríamos identificar matemáticamente el punto de saturación ni observar el mecanismo de throttling del planificador CFS de Linux durante las pruebas de estrés.'"
    ],
    bg_hex="FFF5F5",
    border_hex="E53E3E",
    title_color=COLOR_RED
)

# ------------------------------------------------------------------------------
# CONSIGNA 2: IMPLEMENTACIÓN DEL COMPONENTE Y BALANCEO
# ------------------------------------------------------------------------------
h2_c = doc.add_heading("Consigna 2: Implementación del Componente y Balanceo (30 Puntos)", level=1)
h2_c.paragraph_format.space_before = Pt(14)
h2_c.paragraph_format.space_after = Pt(4)

add_box(
    doc,
    "📌 ¿QUÉ PIDE TEXTUALMENTE LA CONSIGNA 2?",
    [
        "\"Desarrollen un microservicio (API REST) en el lenguaje de su preferencia. El endpoint principal debe devolver obligatoriamente el Hostname o ID del contenedor/instancia.\"",
        "Entregable: Archivos de configuración del balanceador de carga (ej. nginx.conf) integrando Health Checks para comprobar el estado de las réplicas. Capturas de pantalla donde se observe que peticiones consecutivas al balanceador son respondidas por distintos IDs de instancia."
    ],
    bg_hex="F7FAFC",
    border_hex="2B6CB0"
)

add_box(
    doc,
    "⚙️ ¿QUÉ HICIMOS TÉCNICAMENTE EN EL PROYECTO?",
    [
        "1. API REST en FastAPI (microservice/main.py): Desarrollada en Python 3.12 sobre el servidor ASGI Uvicorn.",
        "   - Endpoint GET /: Ejecuta socket.gethostname() y devuelve en el JSON los campos 'container_id' y 'hostname' obligatorios.",
        "   - Endpoint GET /health: Devuelve estado UP, uptime y memoria RSS en MB para los chequeos de salud.",
        "   - Endpoint GET /work (o /stress): Ejecuta miles de rondas de hashing SHA-256 (cómputo CPU-bound puro).",
        "2. Balanceador Nginx (nginx/nginx.conf): Opera en Capa 7 (Reverse Proxy).",
        "   - Bloque upstream: Agrupa a las réplicas (app1:8000, app2:8000, app3:8000) bajo el algoritmo Round-Robin.",
        "   - Health Checks Pasivos: max_fails=3 y fail_timeout=10s. Si una réplica falla 3 veces, queda suspendida por 10 segundos.",
        "   - Resiliencia (Zero Downtime): Directiva 'proxy_next_upstream error timeout http_500 http_502 http_503 http_504'. Si una réplica se cae, Nginx reenvía la solicitud inmediatamente a otra réplica sana sin error para el usuario.",
        "   - Trazabilidad: Agrega encabezados HTTP 'X-Served-By' y 'X-Upstream-Response-Time'.",
        "3. Captura de Rotación: Con verify_loadbalancing.ps1 ejecutamos 12 peticiones seguidas demostrando que los IDs rotan en estricto orden 1 -> 2 -> 3 -> 1 -> 2 -> 3 (33.3% por nodo)."
    ],
    bg_hex="F8FAFC",
    border_hex="4A5568"
)

add_box(
    doc,
    "🗣️ CÓMO EXPLICAR LA CONSIGNA 2 FRENTE AL PROFESOR (PALABRA POR PALABRA):",
    [
        "\"Para la Consigna 2 desarrollamos el microservicio en Python 3.12 utilizando FastAPI por su naturaleza asíncrona de alto rendimiento. En el endpoint raíz GET / cumplimos la consigna obligatoria devolviendo el Container ID mediante la llamada socket.gethostname().\"",
        "\"En la capa de balanceo configuramos Nginx como un Reverse Proxy L7. Definimos un grupo upstream con las tres réplicas utilizando balanceo Round-Robin, e incorporamos dos mecanismos fundamentales de disponibilidad:\n"
        "1) Health Checks pasivos con max_fails=3 y fail_timeout=10s: si un contenedor se muere, Nginx lo saca de la rotación automáticamente por 10 segundos para no mandarle tráfico inútil.\n"
        "2) Conmutación por error transparente mediante proxy_next_upstream: si una réplica se apaga o responde con un error 500/502, Nginx reintenta la petición instantáneamente en otra réplica viva, logrando Zero Downtime.\"",
        "\"Como evidencia, incluimos en el informe el archivo nginx.conf completo y la Captura 2 de la terminal ejecutando el script de verificación, donde se observa claramente la alternancia matemática perfecta entre los tres Container IDs con respuestas 200 OK y latencias menores a 10 ms.\""
    ],
    bg_hex="EBF8FF",
    border_hex="3182CE",
    title_color=COLOR_GREEN
)

add_box(
    doc,
    "❓ PREGUNTA TÍPICA DE EXAMEN SOBRE CONSIGNA 2:",
    [
        "Profesor: '¿Qué diferencia hay entre un Health Check activo y uno pasivo en Nginx?'",
        "Tu respuesta: 'Un Health Check ACTIVO (típico de Nginx Plus pago) envía 'pings' periódicos en segundo plano al backend independientemente de si hay usuarios navegando o no. Un Health Check PASIVO (el que implementamos en Nginx Community mediante max_fails y fail_timeout) evalúa la salud con el tráfico real: si una petición de un usuario falla 3 veces seguidas contra una réplica, Nginx la marca como caída y deja de enviarle peticiones durante 10 segundos, reintentando la solicitud en otra réplica viva con proxy_next_upstream.'"
    ],
    bg_hex="FFF5F5",
    border_hex="E53E3E",
    title_color=COLOR_RED
)

# ------------------------------------------------------------------------------
# CONSIGNA 3: PRUEBAS DE ESTRÉS Y ATRIBUTOS DE CALIDAD
# ------------------------------------------------------------------------------
h3_c = doc.add_heading("Consigna 3: Pruebas de Estrés y Atributos de Calidad (40 Puntos)", level=1)
h3_c.paragraph_format.space_before = Pt(14)
h3_c.paragraph_format.space_after = Pt(4)

add_box(
    doc,
    "📌 ¿QUÉ PIDE TEXTUALMENTE LA CONSIGNA 3?",
    [
        "\"Sometan la arquitectura a pruebas de carga utilizando Apache Benchmark (ab) o herramientas equivalentes. Deben ejecutar dos escenarios: concurrencia moderada (ej. 100 usuarios concurrentes) y concurrencia extrema (saturación de CPU).\"",
        "Entregable: Reporte de métricas temporales (latencia promedio, percentiles p95 y p99).",
        "Análisis Crítico: Conclusión formal indicando en qué punto el sistema degrada sus tiempos de respuesta, si la latencia máxima cumple con restricciones de tiempo real, y cómo justifica el comportamiento observado en función de la arquitectura desplegada."
    ],
    bg_hex="F7FAFC",
    border_hex="2B6CB0"
)

add_box(
    doc,
    "⚙️ ¿QUÉ HICIMOS TÉCNICAMENTE EN EL PROYECTO?",
    [
        "1. Herramienta: Apache Benchmark (ab -k -l) ejecutado dentro de la red virtual de Docker contra el balanceador.",
        "2. Escenario Moderado (GET / con c=100, n=5.000): Throughput de 1.384 req/s, latencia promedio 72.3 ms, p95 de 93 ms y p99 de 104 ms. Errores: 0. CUMPLE holgadamente el SLA del TP2 (p95 <= 300 ms, p99 <= 800 ms).",
        "3. Escenarios de Carga Alta (GET / con c=500, c=1.000 y c=2.000): La latencia se incrementa: p95 = 426 ms (c=500), 789 ms (c=1.000) y 1.627 ms (c=2.000). NO CUMPLE por degradación temporal.",
        "4. Escenario de Saturación de CPU (GET /work con c=100 y c=1.000): Cálculo intensivo de hashing. El Throughput cae abruptamente a 325 req/s (-70%), el p95 se dispara a 2 y 4.4 segundos, y entre el 59% y 89% de las peticiones fallan por timeout de Nginx (NO CUMPLE, colapso total).",
        "5. Escenario POST /envíos (c=100, n=5.000): Latencia promedio 82 ms y p95 118 ms (cumple en tiempo), pero arrojó 33 errores (0.7% de fallo)."
    ],
    bg_hex="F8FAFC",
    border_hex="4A5568"
)

add_box(
    doc,
    "🗣️ CÓMO EXPLICAR LA CONSIGNA 3 FRENTE AL PROFESOR (PALABRA POR PALABRA):",
    [
        "\"Para la Consigna 3 sometimos la arquitectura a pruebas de estrés con Apache Benchmark ejecutando dos tipos de carga: I/O liviano en GET / y trabajo intensivo de CPU en GET /work, contrastando los resultados contra el SLA del TP2.\"",
        "\"Presentamos una matriz completa de 11 columnas con todos los percentiles:\n"
        "• En Concurrencia Moderada (100 usuarios): El clúster rinde de forma óptima procesando 1.384 peticiones por segundo con un p95 de apenas 93 ms y 0% de errores, CUMPLIENDO el SLA del TP2.\n"
        "• En Concurrencia Alta y Extrema (500 a 2.000 usuarios): El sistema NO CUMPLE el SLA porque el p95 sube a 426 ms y 789 ms debido a una causa bien identificada: no es falta de CPU (el uso rondaba el 20%), sino ENCOLAMIENTO EN EL BUFFER DE RED (Socket Backlog). Mantener abiertos cientos de sockets TCP simultáneos demora la llegada de paquetes al Event Loop de Uvicorn.\n"
        "• En Saturación de CPU (GET /work): El sistema NO CUMPLE y entra en COLAPSO. El Throughput se desploma, el p95 sube a más de 2 y 4 segundos y se produce entre un 59% y 89% de errores HTTP. ¿Por qué ocurre esto? Porque las réplicas agotan la cuota de 50 ms asignada por el planificador CFS del kernel Linux (cpus: 0.50), y el sistema operativo suspende los contenedores (CPU Throttling), provocando que Nginx alcance sus timeouts de espera.\"",
        "\"Respecto a las Restricciones de Tiempo Real:\n"
        "1) Hard Real-Time: NO CUMPLE bajo ninguna condición. La varianza de Docker y las colas del kernel llevan el p99 a 2.7 segundos, lo que viola cualquier deadline estricto.\n"
        "2) Soft Real-Time: CUMPLE para tráfico moderado comercial (93 ms), pero se degrada inaceptablemente bajo saturación de CPU.\""
    ],
    bg_hex="EBF8FF",
    border_hex="3182CE",
    title_color=COLOR_GREEN
)

add_box(
    doc,
    "❓ LAS 3 PREGUNTAS TRAMPA DE EXAMEN SOBRE CONSIGNA 3:",
    [
        "Pregunta 1: '¿Por qué Failed Requests en Apache Benchmark da 0 si en la tabla dicen que hubo 59% de errores en el Escenario E?'\n"
        "Tu respuesta: 'Porque ab define 'Failed requests' como fallos a nivel de transporte TCP (conexiones rechazadas o truncadas). Los códigos de error HTTP 500, 502 o 504 devueltos por Nginx son respuestas HTTP completas válidas en Capa 4, por lo que ab las contabiliza como recibidas pero en la línea 'Non-2xx responses'. En el Escenario E hubo 2.966 respuestas Non-2xx de 5.000 (59.3% de error real de aplicación).'",
        
        "Pregunta 2: '¿Cómo solucionarían el colapso del Escenario E sin gastar más dinero en servidores gigantes?'\n"
        "Tu respuesta: 'Cambiando el patrón arquitectónico a un modelo Asíncrono orientado a eventos. El endpoint HTTP no debe calcular la ruta sincrónicamente. La API debe recibir la solicitud, encolarla en un broker de mensajería (como RabbitMQ o Kafka) y responder inmediatamente un código HTTP 202 Accepted ('En proceso') en menos de 20 ms. Luego, workers asíncronos en segundo plano procesan el cálculo sin saturar la API web.'",
        
        "Pregunta 3: '¿Cómo harían que el Escenario B (500 usuarios) que hoy NO CUMPLE pase a CUMPLIR?'\n"
        "Tu respuesta: 'Escalando horizontalmente las réplicas de 3 a 8 en el clúster (para repartir los sockets de red entre más contenedores) y configurando Uvicorn con múltiples procesos workers (--workers 4) para aprovechar el paralelismo de I/O en cada réplica.'"
    ],
    bg_hex="FFF5F5",
    border_hex="E53E3E",
    title_color=COLOR_RED
)

# ------------------------------------------------------------------------------
# CONDICIONES DE ENTREGA
# ------------------------------------------------------------------------------
h4_c = doc.add_heading("Condiciones de Entrega del Enunciado (Checklist)", level=1)
h4_c.paragraph_format.space_before = Pt(14)
h4_c.paragraph_format.space_after = Pt(4)

add_box(
    doc,
    "📌 VERIFICACIÓN DE REQUISITOS FORMALES:",
    [
        "• Fecha límite: 02/11/2026 -> Entregado y finalizado el 01/11/2026.",
        "• Formato: Archivo comprimido con la resolución en PDF -> Archivo 'TP3_Arquitectura_Cloud_Native_Entrega.zip' en el Escritorio con el PDF oficial.",
        "• Vínculo a Git en el Encabezado -> En el encabezado del PDF figura destacado: https://github.com/fifix407/tp3-arquitectura-cloud-native-",
        "• README.md en el Repositorio -> Contiene la arquitectura, comandos exactos de 'docker compose up -d' y las instrucciones para reproducir los benchmarks de carga."
    ],
    bg_hex="F0FFF4",
    border_hex="38A169",
    title_color=COLOR_GREEN
)

doc.save(str(output_path))
print(f"[EXITO] Documento de Guión Consigna a Consigna generado: {output_path}")
