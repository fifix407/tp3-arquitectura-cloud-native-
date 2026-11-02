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

def set_cell_background(cell, fill_hex):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_hex}"/>')
    tcPr.append(shd)

def add_callout(doc, text_list, bg_hex="F7FAFC", border_hex="3182CE"):
    table = doc.add_table(rows=1, cols=1)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    cell = table.cell(0, 0)
    set_cell_background(cell, bg_hex)
    
    tcPr = cell._tc.get_or_add_tcPr()
    tcBorders = parse_xml(
        f'<w:tcBorders {nsdecls("w")}>'
        f'<w:top w:val="none"/>'
        f'<w:left w:val="single" w:sz="24" w:space="0" w:color="{border_hex}"/>'
        f'<w:bottom w:val="none"/>'
        f'<w:right w:val="none"/>'
        f'</w:tcBorders>'
    )
    tcPr.append(tcBorders)
    
    cell.paragraphs[0].text = ""
    for idx, t in enumerate(text_list):
        p = cell.add_paragraph() if idx > 0 else cell.paragraphs[0]
        p.paragraph_format.space_before = Pt(2)
        p.paragraph_format.space_after = Pt(2)
        p.paragraph_format.line_spacing = 1.15
        run = p.add_run(t)
        run.font.name = "Segoe UI"
        run.font.size = Pt(9.5)
        run.font.color.rgb = COLOR_TEXT
    doc.add_paragraph().paragraph_format.space_after = Pt(4)

def add_dialog_box(doc, speaker, text, bg_hex="F8FAFC", border_hex="4A5568"):
    table = doc.add_table(rows=1, cols=1)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    cell = table.cell(0, 0)
    set_cell_background(cell, bg_hex)
    
    tcPr = cell._tc.get_or_add_tcPr()
    tcBorders = parse_xml(
        f'<w:tcBorders {nsdecls("w")}>'
        f'<w:top w:val="single" w:sz="6" w:space="0" w:color="{border_hex}"/>'
        f'<w:left w:val="single" w:sz="20" w:space="0" w:color="{border_hex}"/>'
        f'<w:bottom w:val="single" w:sz="6" w:space="0" w:color="{border_hex}"/>'
        f'<w:right w:val="single" w:sz="6" w:space="0" w:color="{border_hex}"/>'
        f'</w:tcBorders>'
    )
    tcPr.append(tcBorders)
    
    p = cell.paragraphs[0]
    p.paragraph_format.space_before = Pt(3)
    p.paragraph_format.space_after = Pt(3)
    p.paragraph_format.line_spacing = 1.15
    
    r_spk = p.add_run(f"{speaker}: ")
    r_spk.font.name = "Segoe UI"
    r_spk.font.bold = True
    r_spk.font.size = Pt(9)
    if "PROFESOR" in speaker:
        r_spk.font.color.rgb = COLOR_RED
    else:
        r_spk.font.color.rgb = COLOR_GREEN
        
    r_txt = p.add_run(text)
    r_txt.font.name = "Segoe UI"
    r_txt.font.size = Pt(9)
    r_txt.font.color.rgb = COLOR_TEXT
    doc.add_paragraph().paragraph_format.space_after = Pt(3)

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
r_title = p_title.add_run("Guía Maestra para Presentar y Defender el TP N° 3")
r_title.font.name = "Segoe UI"
r_title.font.size = Pt(17)
r_title.font.bold = True
r_title.font.color.rgb = COLOR_PRIMARY
p_title.paragraph_format.space_after = Pt(2)

p_sub = doc.add_paragraph()
r_sub = p_sub.add_run("Despliegue de Arquitectura Cloud-Native: Guión Paso a Paso, Explicación de Conceptos y Preguntas Trampa de Examen")
r_sub.font.name = "Segoe UI"
r_sub.font.size = Pt(10)
r_sub.font.color.rgb = COLOR_SECONDARY
p_sub.paragraph_format.space_after = Pt(8)

meta = [
    "Alumnos: Lucía Astorga, Emmanuel Bustos, Santiago Militello",
    "Materia: Arquitectura de Sistemas (Ciclo 2026)",
    "Caso de Estudio: GlobalLogistics S.A. (Plataforma Distribuida de Telemetría)",
    "Objetivo de esta Guía: Saber explicar con seguridad técnica cada parte del trabajo, qué hace cada archivo y cómo responder cualquier pregunta que hagan los docentes en la defensa oral."
]
add_callout(doc, meta, bg_hex="F7FAFC", border_hex="2B6CB0")

# ------------------------------------------------------------------------------
# PARTE 1: LA INTRODUCCIÓN PERFECTA
# ------------------------------------------------------------------------------
h1 = doc.add_heading("1. Cómo Arrancar la Presentación (El Discurso de 1 Minuto)", level=1)
h1.paragraph_format.space_before = Pt(10)
h1.paragraph_format.space_after = Pt(4)

p = doc.add_paragraph(
    "Cuando el profesor les diga: 'Bueno chicos, cuéntennos qué hicieron en este TP3', NO empiecen diciendo 'hicimos un docker compose'. "
    "Empiecen hablando del problema de negocio como verdaderos Arquitectos de Software. Decir esto te garantiza un 10 de entrada:"
)
p.paragraph_format.line_spacing = 1.15
p.paragraph_format.space_after = Pt(4)

intro_speech = [
    "\"Buenas tardes profesores. Para este Trabajo Práctico N° 3 nos pusimos en el rol de Arquitectos Cloud para la empresa GlobalLogistics S.A.\"",
    "\"El problema central era certificar si la plataforma distribuida de telemetría y rastreo de camiones era capaz de soportar picos transaccionales comerciales sin intervención operativa manual y sin degradar la calidad de servicio pactada en el TP2 (SLA: p95 <= 300 ms, p99 <= 800 ms y 0% de errores).\"",
    "\"Para resolverlo, diseñamos y desplegamos una arquitectura Cloud-Native completa con Infraestructura como Código: levantamos un clúster balanceado en Capa 7 con Nginx y tres réplicas activas de una API REST en FastAPI, con aislamiento estricto de recursos y Health Checks continuos. Luego, la sometimos a una batería rigurosa de pruebas de estrés con Apache Benchmark para encontrar su punto de rotura y justificar técnicamente su comportamiento temporal.\""
]
add_callout(doc, intro_speech, bg_hex="EBF8FF", border_hex="3182CE")

# ------------------------------------------------------------------------------
# PARTE 2: CONSIGNA 1 EXPLICADA AL DETALLE
# ------------------------------------------------------------------------------
h2 = doc.add_heading("2. Consigna 1: Configuración del Entorno e IaC (30 Puntos)", level=1)
h2.paragraph_format.space_before = Pt(10)
h2.paragraph_format.space_after = Pt(4)

p = doc.add_paragraph(
    "¿Qué nos pedían? Crear los manifiestos de Infraestructura como Código (docker-compose.yml) para levantar de forma 100% automatizada exactamente 1 balanceador y 3 réplicas."
)
p.paragraph_format.line_spacing = 1.15
p.paragraph_format.space_after = Pt(4)

c1_puntos = [
    "1. ¿Qué es IaC (Infraestructura como Código)? En vez de instalar Nginx y Python a mano en una máquina virtual, escribimos un archivo declarativo (docker-compose.yml). Con un solo comando ('docker compose up -d'), cualquier desarrollador o servidor en la nube levanta exactamente la misma topología de red en segundos de forma determinística.",
    "2. ¿Por qué 1 balanceador y 3 réplicas? El balanceador ('globallogistics_loadbalancer') es la única puerta de entrada pública (expone el puerto 8080). Las 3 réplicas ('globallogistics_app_1', 'app_2' y 'app_3') procesan las peticiones en paralelo.",
    "3. Aislamiento de Red: Las réplicas NO tienen puertos abiertos hacia Windows (0.0.0.0). Viven dentro de una red privada virtual tipo bridge ('globallogistics_net'). Solo Nginx puede comunicarse con ellas por el puerto interno 8000.",
    "4. Límites de Recursos (cpus: '0.50', memory: 512M): A cada réplica le restringimos la potencia a medio núcleo y medio giga de RAM. ¿Por qué? Para observar matemáticamente cómo satura el CPU bajo estrés.",
    "5. Arranque Condicional por Salud ('condition: service_healthy'): Nginx tiene la directiva 'depends_on' con 'service_healthy'. Nginx no abre su puerto ni recibe a ningún cliente hasta que las 3 réplicas respondan con éxito a su prueba médica interna (/health)."
]
add_callout(doc, c1_puntos, bg_hex="F8FAFC", border_hex="3182CE")

add_dialog_box(
    doc,
    "PREGUNTA TÍPICA DEL PROFESOR",
    "¿Qué pasa si una réplica tarda 10 segundos en arrancar?",
    bg_hex="FFF5F5",
    border_hex="E53E3E"
)
add_dialog_box(
    doc,
    "CÓMO RESPONDER",
    "Gracias a la directiva 'condition: service_healthy' en el docker-compose.yml, Nginx espera pacientemente. Docker ejecuta el test de salud cada 5 segundos contra /health. Recién cuando las 3 réplicas están en estado 'healthy', Nginx se inicia y comienza a aceptar tráfico. Así se evitan los errores 502 por arranques prematuros.",
    bg_hex="F0FFF4",
    border_hex="38A169"
)

# ------------------------------------------------------------------------------
# PARTE 3: CONSIGNA 2 EXPLICADA AL DETALLE
# ------------------------------------------------------------------------------
h3 = doc.add_heading("3. Consigna 2: Microservicio y Balanceador L7 (30 Puntos)", level=1)
h3.paragraph_format.space_before = Pt(10)
h3.paragraph_format.space_after = Pt(4)

p = doc.add_paragraph(
    "¿Qué nos pedían? Desarrollar la API REST (FastAPI) donde el endpoint raíz devuelva obligatoriamente el Hostname/Container ID, y configurar Nginx con Round-Robin y Health Checks mostrando capturas de la rotación."
)
p.paragraph_format.line_spacing = 1.15
p.paragraph_format.space_after = Pt(4)

c2_puntos = [
    "1. El Microservicio (Python 3.12 + FastAPI + Uvicorn): Elegimos FastAPI por ser asíncrono y de ultra alto rendimiento. En el endpoint 'GET /' se hace la llamada al sistema 'socket.gethostname()', devolviendo en el JSON el ID hexadecimal único del contenedor que atendió la petición.",
    "2. Endpoint de Salud (/health): Retorna un JSON con {'status': 'UP', 'uptime': ..., 'memory_rss_mb': ...}. Este endpoint es consumido cada 5 segundos por Docker y por Nginx para monitorear que la réplica no esté colgada.",
    "3. Endpoint de Carga (/stress o /work): Ejecuta miles de iteraciones de hashing criptográfico SHA-256 en bucle cerrado. Es una tarea 100% CPU-bound que simula algoritmos pesados de optimización logística.",
    "4. El Balanceador Nginx (Capa 7): Opera como Reverse Proxy. En 'nginx.conf' definimos el bloque upstream 'microservices_backend' con algoritmo Round-Robin.",
    "5. Health Checks Pasivos y Tolerancia a Fallos: En el upstream pusimos 'max_fails=3' y 'fail_timeout=10s'. Si una réplica falla 3 veces seguidas, Nginx la saca de la rotación por 10 segundos. Además, con 'proxy_next_upstream', si una réplica da timeout o error 500, Nginx reenvía esa misma petición a otra réplica viva en milisegundos sin que el usuario se entere (Zero Downtime).",
    "6. Demostración de Rotación: Con el script verify_loadbalancing.ps1 enviamos 12 peticiones seguidas y mostramos que Nginx reparte matemáticamente un tercio (33.3%) a cada Container ID."
]
add_callout(doc, c2_puntos, bg_hex="F8FAFC", border_hex="3182CE")

add_dialog_box(
    doc,
    "PREGUNTA TÍPICA DEL PROFESOR",
    "¿Por qué decimos que Nginx balancea en Capa 7 y no en Capa 4?",
    bg_hex="FFF5F5",
    border_hex="E53E3E"
)
add_dialog_box(
    doc,
    "CÓMO RESPONDER",
    "Porque Nginx opera a nivel de Aplicación (Capa 7 del modelo OSI). Lee y entiende el protocolo HTTP: puede inspeccionar la URL (/health vs /work), leer encabezados (Host, User-Agent), inyectar cabeceras de trazabilidad (X-Served-By, X-Upstream-Response-Time) y decidir reintentar una petición si recibe un código de error HTTP 500 o 502. Un balanceador de Capa 4 solo vería paquetes TCP/IP y puertos, sin entender qué viaja adentro.",
    bg_hex="F0FFF4",
    border_hex="38A169"
)

# ------------------------------------------------------------------------------
# PARTE 4: CONSIGNA 3 EXPLICADA AL DETALLE
# ------------------------------------------------------------------------------
h4 = doc.add_heading("4. Consigna 3: Pruebas de Estrés y Análisis Crítico (40 Puntos)", level=1)
h4.paragraph_format.space_before = Pt(10)
h4.paragraph_format.space_after = Pt(4)

p = doc.add_paragraph(
    "Esta es la sección que define la nota. Acá evalúan si entienden las métricas, los percentiles y por qué el sistema se rompe."
)
p.paragraph_format.line_spacing = 1.15
p.paragraph_format.space_after = Pt(4)

c3_puntos = [
    "1. La Herramienta Utilizada: Apache Benchmark 2.3 (ab). El comando utilizado fue: 'ab -k -l -n <peticiones> -c <concurrencia> <URL>'. El flag -k habilita conexiones persistentes Keep-Alive; el flag -l evita que ab marque error cuando el tamaño de respuesta varía ligeramente por los distintos Container IDs devueltos.",
    "2. El Criterio SLA del TP2 (Objetivo a Cumplir): Exige que el p95 sea <= 300 ms, el p99 <= 800 ms y 0 errores HTTP (non-2xx).",
    "3. Escenario A (Moderado: 100 concurrentes / GET /) -> CUMPLE: Latencia media de 72 ms, p95 de 93 ms (muy por debajo de 300 ms), Throughput de 1.384 req/s y 0% de errores. La arquitectura sobra para el tráfico comercial estándar.",
    "4. Escenarios B, C y D (Alta y Extrema: 500, 1.000 y 2.000 concurrentes) -> NO CUMPLEN: En B el p95 sube a 426 ms; en C a 789 ms; en D a 1.627 ms. No cumplen por exceso de latencia.",
    "5. Escenario E (Cómputo CPU Intensivo /work) -> NO CUMPLE (COLAPSO): Throughput cae a 325 req/s, el p95 se dispara a 2 y 4 segundos, y entre el 59% y 89% de las peticiones fallan con error HTTP 502/504.",
    "6. Escenario G (POST /envíos: 100 concurrentes) -> PARCIAL: En latencia cumple perfecto (p95 = 118 ms), pero fallaron 33 peticiones (0.7% de error). Como el SLA pedía cero errores, queda en observación."
]
add_callout(doc, c3_puntos, bg_hex="F8FAFC", border_hex="3182CE")

# ------------------------------------------------------------------------------
# PARTE 5: LAS 3 PREGUNTAS TÉCNICAS FUNDAMENTALES
# ------------------------------------------------------------------------------
h5 = doc.add_heading("5. Los 3 Porqués que Pregunta Todo Docente", level=1)
h5.paragraph_format.space_before = Pt(10)
h5.paragraph_format.space_after = Pt(4)

add_dialog_box(
    doc,
    "PREGUNTA 1 DEL PROFESOR",
    "¿Por qué en los Escenarios B, C y D la latencia sube a 700 ms si el uso de CPU de las réplicas estaba bajo (apenas 20%)?",
    bg_hex="FFF5F5",
    border_hex="E53E3E"
)
add_dialog_box(
    doc,
    "CÓMO RESPONDER",
    "Porque la degradación NO fue por falta de procesador, sino por ENCOLAMIENTO EN EL BUFFER DE RED (Socket Backlog). Las peticiones a GET / son livianas en cómputo, pero al meter 500 o 1.000 clientes simultáneos, cada réplica tiene que mantener abiertos cientos de sockets TCP. Las peticiones se acumulan en la cola del sistema operativo esperando que el Event Loop monohilo de Uvicorn las despache. Ese tiempo de espera en la fila de red es lo que infla los percentiles p95 y p99.",
    bg_hex="F0FFF4",
    border_hex="38A169"
)

add_dialog_box(
    doc,
    "PREGUNTA 2 DEL PROFESOR",
    "¿Por qué en el Escenario E (/work) el sistema colapsó completamente y tiró hasta un 89% de errores?",
    bg_hex="FFF5F5",
    border_hex="E53E3E"
)
add_dialog_box(
    doc,
    "CÓMO RESPONDER",
    "Por dos fenómenos combinados: 1) Tarea Bloqueante en Event Loop: FastAPI corre sobre un bucle de eventos asíncrono. Como el cálculo criptográfico es síncrono y pesado, monopoliza el único hilo del proceso impidiendo atender otras peticiones; 2) Throttling de CPU del kernel Linux: En docker-compose.yml limitamos a cpus: '0.50'. Cada contenedor tiene asignada una cuota de 50 ms por ciclo en el planificador CFS de Linux. Al hacer cálculo intensivo, la réplica agota sus 50 ms inmediatamente y el kernel la congela (suspende) hasta el ciclo siguiente. Las colas se desbordan, expiran los timeouts de Nginx y se producen errores 504 Gateway Timeout y 502 Bad Gateway.",
    bg_hex="F0FFF4",
    border_hex="38A169"
)

add_dialog_box(
    doc,
    "PREGUNTA 3 DEL PROFESOR",
    "¿Cumple o no cumple con restricciones de Tiempo Real?",
    bg_hex="FFF5F5",
    border_hex="E53E3E"
)
add_dialog_box(
    doc,
    "CÓMO RESPONDER",
    "Depende de la clasificación: 1) Hard Real-Time (Tiempo Real Estricto): NO CUMPLE bajo ningún concepto. En sistemas críticos (como frenos ABS o satélites), exceder un plazo temporal invalida el resultado. La virtualización en Docker y el scheduler del sistema operativo generan varianza en las colas (el p99 se va a 2.7 segundos), lo cual es inadmisible en Hard Real-Time; 2) Soft Real-Time (Web Transaccional): CUMPLE holgadamente para el tráfico comercial normal de 100 usuarios (p95 = 93 ms <= 300 ms), pero NO CUMPLE bajo picos de alta concurrencia ni con tareas de cómputo intensivo.",
    bg_hex="F0FFF4",
    border_hex="38A169"
)

# ------------------------------------------------------------------------------
# PARTE 6: LAS TRAMPAS DEL COLOQUIO (MANIPULAR EL SISTEMA EN VIVO)
# ------------------------------------------------------------------------------
h6 = doc.add_heading("6. Las Preguntas Trampa del Coloquio: Cómo Modificar el Sistema en Vivo", level=1)
h6.paragraph_format.space_before = Pt(10)
h6.paragraph_format.space_after = Pt(4)

p = doc.add_paragraph(
    "A muchos profesores les gusta decirte: 'A ver, mostrame en vivo... cambiá algo en el código para que lo que anda deje de andar, o para que lo que no anda pase a andar'. "
    "Tené estas respuestas memorizadas:"
)
p.paragraph_format.line_spacing = 1.15
p.paragraph_format.space_after = Pt(4)

trampas = [
    "Trampa 1: '¿Cómo hacés que el Escenario A (que CUMPLE) pase a NO CUMPLIR?'\n"
    "Respuesta: 1) Edito docker-compose.yml y le bajo la cuota de CPU a 'cpus: 0.05' (el kernel suspenderá constantemente a los contenedores inflando la latencia); 2) Apago 2 réplicas ('docker stop globallogistics_app_2 globallogistics_app_3') para que la única que quede se sature de inmediato; 3) Le quito a nginx.conf la línea 'keepalive 32' para obligar a hacer handshakes TCP completos por cada request.",
    
    "Trampa 2: '¿Cómo hacés que el Escenario B o C (que NO CUMPLE) pase a CUMPLIR?'\n"
    "Respuesta: 1) Escalo horizontalmente de 3 a 8 réplicas en Docker para repartir las conexiones y reducir el encolamiento por contenedor; 2) Configuro Uvicorn con múltiples workers ('--workers 4') en el Dockerfile para que aproveche más hilos y procese sockets en paralelo.",
    
    "Trampa 3: '¿Cómo se resuelve como Arquitecto el colapso del Escenario E (/work)?'\n"
    "Respuesta: Desacoplando la arquitectura con un patrón Asíncrono orientado a eventos. El cliente no debe esperar a que el servidor calcule la ruta en vivo. La API debe recibir los datos, publicar un mensaje en una cola como RabbitMQ o Apache Kafka, y responderle inmediatamente al cliente un HTTP 202 Accepted ('Solicitud en proceso') en menos de 20 ms. Luego, workers en segundo plano (Celery) procesan el cálculo pesado sin bloquear la web."
]
add_callout(doc, trampas, bg_hex="FFFBEB", border_hex="D97706")

# ------------------------------------------------------------------------------
# PARTE 7: RESUMEN FINAL DE ENTREGA
# ------------------------------------------------------------------------------
h7 = doc.add_heading("7. Checklist Rápido antes de Entregar", level=1)
h7.paragraph_format.space_before = Pt(10)
h7.paragraph_format.space_after = Pt(4)

checklist = [
    "[OK] Archivo PDF listo en Escritorio: TP3_Arquitectura_Cloud_Native_Astorga_Bustos_Militello.pdf",
    "[OK] Archivo Word editable en Escritorio: TP3_Arquitectura_Cloud_Native_Astorga_Bustos_Militello.docx",
    "[OK] Archivo ZIP para subir al campus: TP3_Arquitectura_Cloud_Native_Entrega.zip",
    "[OK] Repositorio público de GitHub actualizado con todo el código: https://github.com/fifix407/tp3-arquitectura-cloud-native-",
    "[OK] Capturas reales incrustadas: 1) docker compose ps, 2) rotación verify_loadbalancing.ps1, 3) ab moderado, 4) ab saturación CPU.",
    "[OK] Tabla de 11 columnas completa con los 7 escenarios oficiales y colores de cumplimiento de SLA."
]
add_callout(doc, checklist, bg_hex="F0FFF4", border_hex="38A169")

doc.save(str(output_path))
print(f"[EXITO] Guía de defensa oral generada en: {output_path}")
