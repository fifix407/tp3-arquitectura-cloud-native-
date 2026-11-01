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

output_path = desktop / "TP3_Arquitectura_Cloud_Native_Astorga_Bustos_Militello.docx"

doc = docx.Document()

# Márgenes
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
        run.font.size = Pt(9)
        run.font.color.rgb = COLOR_TEXT
    doc.add_paragraph().paragraph_format.space_after = Pt(4)

def add_image_box(doc, img_path, caption_title, description_text):
    table = doc.add_table(rows=1, cols=1)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    cell = table.cell(0, 0)
    set_cell_background(cell, "F8FAFC")
    
    tcPr = cell._tc.get_or_add_tcPr()
    tcBorders = parse_xml(
        f'<w:tcBorders {nsdecls("w")}>'
        f'<w:top w:val="single" w:sz="8" w:space="0" w:color="CBD5E1"/>'
        f'<w:left w:val="single" w:sz="8" w:space="0" w:color="CBD5E1"/>'
        f'<w:bottom w:val="single" w:sz="8" w:space="0" w:color="CBD5E1"/>'
        f'<w:right w:val="single" w:sz="8" w:space="0" w:color="CBD5E1"/>'
        f'</w:tcBorders>'
    )
    tcPr.append(tcBorders)
    
    p = cell.paragraphs[0]
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(4)
    p.paragraph_format.space_after = Pt(4)
    
    if os.path.exists(img_path):
        p_img = cell.add_paragraph()
        p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_img.paragraph_format.space_before = Pt(2)
        p_img.paragraph_format.space_after = Pt(4)
        run_img = p_img.add_run()
        run_img.add_picture(img_path, width=Inches(6.2))
    
    p_cap = cell.add_paragraph()
    p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_cap.paragraph_format.space_before = Pt(2)
    p_cap.paragraph_format.space_after = Pt(4)
    r_cap = p_cap.add_run(f"📸 {caption_title}\n")
    r_cap.font.name = "Segoe UI"
    r_cap.font.bold = True
    r_cap.font.size = Pt(9)
    r_cap.font.color.rgb = COLOR_PRIMARY
    
    r_desc = p_cap.add_run(description_text)
    r_desc.font.name = "Segoe UI"
    r_desc.font.italic = True
    r_desc.font.size = Pt(8)
    r_desc.font.color.rgb = RGBColor(100, 116, 139)
    
    doc.add_paragraph().paragraph_format.space_after = Pt(4)

# ------------------------------------------------------------------------------
# ENCABEZADO
# ------------------------------------------------------------------------------
p_univ = doc.add_paragraph()
r_univ = p_univ.add_run("UNIVERSIDAD CHAMPAGNAT — LICENCIATURA EN SISTEMAS DE INFORMACIÓN (CICLO 2026)")
r_univ.font.name = "Segoe UI"
r_univ.font.size = Pt(8.5)
r_univ.font.bold = True
r_univ.font.color.rgb = COLOR_GRAY
p_univ.paragraph_format.space_after = Pt(2)

p_title = doc.add_paragraph()
r_title = p_title.add_run("Trabajo Práctico N° 3: Despliegue de Arquitectura Cloud-Native")
r_title.font.name = "Segoe UI"
r_title.font.size = Pt(16.5)
r_title.font.bold = True
r_title.font.color.rgb = COLOR_PRIMARY
p_title.paragraph_format.space_after = Pt(2)

p_sub = doc.add_paragraph()
r_sub = p_sub.add_run("Validación de Atributos de Calidad, Balanceo de Carga L7 y Pruebas de Estrés en Contenedores")
r_sub.font.name = "Segoe UI"
r_sub.font.size = Pt(10.5)
r_sub.font.color.rgb = COLOR_SECONDARY
p_sub.paragraph_format.space_after = Pt(10)

meta_info = [
    "Integrantes del Grupo: Lucía Astorga, Emmanuel Bustos, Santiago Militello",
    "Empresa Caso de Estudio: GlobalLogistics S.A. — Plataforma Distribuida de Telemetría",
    "Repositorio Oficial Git: https://github.com/fifix407/tp3-arquitectura-cloud-native-",
    "Criterio de Evaluación SLA (Objetivo TP2): p95 <= 300 ms, p99 <= 800 ms, 0 errores HTTP (non-2xx)"
]
add_callout(doc, meta_info, bg_hex="F7FAFC", border_hex="2B6CB0")

# ------------------------------------------------------------------------------
# 1. RESUMEN EJECUTIVO Y CONTEXTO
# ------------------------------------------------------------------------------
h1 = doc.add_heading("1. Resumen Ejecutivo y Contexto del Desafío", level=1)
h1.paragraph_format.space_before = Pt(12)
h1.paragraph_format.space_after = Pt(4)

p = doc.add_paragraph(
    "El presente informe documenta la solución técnica desarrollada para GlobalLogistics S.A. ante la necesidad "
    "crítica de certificar que su nueva infraestructura de microservicios distribuida soporte los picos transaccionales comerciales "
    "sin degradación crítica ni intervención operativa manual."
)
p.paragraph_format.line_spacing = 1.15
p.paragraph_format.space_after = Pt(6)

p = doc.add_paragraph(
    "Como Arquitectos Cloud, se diseñó e implementó un entorno de infraestructura virtualizada basada en contenedores Docker y orquestada "
    "mediante manifiestos declarativos de Infraestructura como Código (IaC). La topología cuenta con un balanceador de carga de Capa 7 (Nginx Reverse Proxy) "
    "y un clúster de tres (3) réplicas activas de una API REST de telemetría y logística desarrollada con Python 3.12 y FastAPI. Se evaluó "
    "experimentalmente la resiliencia ante contingencias de red, el comportamiento de los mecanismos de Health Checks y el rendimiento temporal frente a una "
    "matriz exhaustiva de carga mediante Apache Benchmark (concurrencia de 100 a 2.000 usuarios y endpoints de cómputo CPU-bound intensivo)."
)
p.paragraph_format.line_spacing = 1.15
p.paragraph_format.space_after = Pt(8)

# ------------------------------------------------------------------------------
# 2. CONFIGURACIÓN DEL ENTORNO E IAC (CONSIGNA 1)
# ------------------------------------------------------------------------------
h2 = doc.add_heading("2. Configuración del Entorno e IaC (Consigna 1 - 30 Puntos)", level=1)
h2.paragraph_format.space_before = Pt(12)
h2.paragraph_format.space_after = Pt(4)

p = doc.add_paragraph(
    "Para garantizar reproducibilidad determinística y cumplir con las mejores prácticas Cloud-Native, la infraestructura completa fue modelada "
    "mediante el manifiesto docker-compose.yml. La especificación orquesta exactamente un (1) balanceador de carga y tres (3) réplicas independientes "
    "del microservicio, asociadas a una red virtual tipo bridge personalizada (globallogistics_net)."
)
p.paragraph_format.line_spacing = 1.15
p.paragraph_format.space_after = Pt(6)

iac_principles = [
    "Arranque Condicional Basado en Salud (condition: service_healthy): Nginx no expone el puerto ni despacha tráfico hasta que las 3 réplicas superan su prueba interna de Health Check (/health).",
    "Aislamiento de Recursos (Limits): Cada réplica está acotada estrictamente a 0.50 CPU y 512MB RAM, lo que permite observar matemáticamente la saturación de procesamiento bajo estrés.",
    "Seguridad por Aislamiento de Red: Las réplicas no publican sus puertos en la interfaz del host físico (0.0.0.0), quedando accesibles exclusivamente a través de la red interna de Docker desde Nginx."
]
add_callout(doc, iac_principles, bg_hex="EBF8FF", border_hex="3182CE")

img_dir = Path(os.environ["USERPROFILE"]) / "OneDrive" / "Imágenes" / "Capturas de pantalla"
img_cap1 = str(img_dir / "Captura de pantalla 2026-11-01 200138.png")
img_cap2 = str(img_dir / "Captura de pantalla 2026-11-01 193423.png")
img_cap3 = str(img_dir / "Captura de pantalla 2026-11-01 190214.png")
img_cap4 = str(img_dir / "Captura de pantalla 2026-11-01 190306.png")

add_image_box(
    doc,
    img_cap1,
    "CAPTURA 1: ESTADO DEL CLÚSTER DE CONTENEDORES (docker compose ps)",
    "Evidencia de ejecución en terminal: 1 balanceador Nginx (globallogistics_loadbalancer en puerto 8080) y 3 réplicas de microservicio (globallogistics_app_1, 2, 3) en estado 'Up' y 'healthy'."
)

# ------------------------------------------------------------------------------
# 3. IMPLEMENTACIÓN DEL COMPONENTE Y BALANCEO (CONSIGNA 2)
# ------------------------------------------------------------------------------
h3 = doc.add_heading("3. Implementación del Componente y Balanceo (Consigna 2 - 30 Puntos)", level=1)
h3.paragraph_format.space_before = Pt(12)
h3.paragraph_format.space_after = Pt(4)

p = doc.add_paragraph(
    "El microservicio fue implementado en Python 3.12 con FastAPI sobre el servidor ASGI Uvicorn. Cumple con el requisito estricto de retornar "
    "el Hostname / Container ID en el endpoint raíz mediante la llamada al sistema socket.gethostname(), además de incorporar endpoints especializados "
    "para comprobación de estado (/health) y trabajo CPU-bound (/work o /stress)."
)
p.paragraph_format.line_spacing = 1.15
p.paragraph_format.space_after = Pt(6)

p = doc.add_paragraph(
    "Nginx actúa como Reverse Proxy L7 con balanceo Round-Robin y Health Checks pasivos mediante max_fails=3 y fail_timeout=10s. "
    "La directiva proxy_next_upstream asegura que, ante cualquier fallo o timeout en una réplica, la petición se reintente de inmediato contra otra réplica viva (Zero Downtime)."
)
p.paragraph_format.line_spacing = 1.15
p.paragraph_format.space_after = Pt(6)

add_image_box(
    doc,
    img_cap2,
    "CAPTURA 2: ROTACIÓN DE CONTAINER IDS EN BALANCEADOR ROUND-ROBIN (verify_loadbalancing.ps1)",
    "Evidencia de ejecución: Peticiones consecutivas a http://localhost:8080/ alternando equitativamente entre los tres Container IDs (1/3 por réplica) con respuestas 200 OK y latencias menores a 10 ms."
)

# ------------------------------------------------------------------------------
# 4. PRUEBAS DE ESTRÉS Y ATRIBUTOS DE CALIDAD (CONSIGNA 3 - 40 PUNTOS)
# ------------------------------------------------------------------------------
h4 = doc.add_heading("4. Pruebas de Estrés y Atributos de Calidad (Consigna 3 - 40 Puntos)", level=1)
h4.paragraph_format.space_before = Pt(12)
h4.paragraph_format.space_after = Pt(4)

p = doc.add_paragraph(
    "4.1 Metodología de Pruebas:\n"
    "• Herramienta: Apache Benchmark 2.3 ejecutado dentro de la red virtual contra el balanceador: ab -k -l -n <N> -c <C> <URL>. El flag -l evita que ab cuente como falla las pequeñas diferencias de bytes debidas a los distintos IDs de contenedor y timestamps; el flag -k simula conexiones persistentes Keep-Alive.\n"
    "• Limitación de Aislamiento: ab, NGINX, las réplicas y el motor Docker comparten la misma máquina host, por lo que el tráfico atraviesa la pila de virtualización, introduciendo overhead en valores absolutos."
)
p.paragraph_format.line_spacing = 1.15
p.paragraph_format.space_after = Pt(6)

add_image_box(
    doc,
    img_cap3,
    "CAPTURA 3: SALIDA DE APACHE BENCHMARK - ESCENARIO MODERADO (100 CONCURRENTES)",
    "Evidencia de prueba de carga moderada: Throughput de ~1.300 req/s, latencia media de 72 ms y p95 de 93 ms sin errores de transporte (CUMPLE con holgura el SLA TP2)."
)

add_image_box(
    doc,
    img_cap4,
    "CAPTURA 4: SALIDA DE APACHE BENCHMARK - ESCENARIO SATURACIÓN DE CPU",
    "Evidencia de prueba de estrés computacional: Fuerte caída de Throughput, degradación severa de latencia alcanzando percentiles de 2 a 4 segundos por agotamiento de cuota CFS (NO CUMPLE SLA)."
)

p_sla_desc = doc.add_paragraph(
    "4.2 Matriz Completa de Resultados y Criterio de Cumplimiento (Objetivo TP2):\n"
    "Los percentiles indican el tiempo por debajo del cual se atendió ese porcentaje de las peticiones (p95: el 95%). "
    "El criterio formal del Objetivo TP2 exige estrictamente: p95 <= 300 ms, p99 <= 800 ms y 0 errores HTTP (non-2xx)."
)
p_sla_desc.paragraph_format.space_after = Pt(4)

# TABLA COMPARATIVA CON FORMATO EXACTO CHAMPAGNAT
table = doc.add_table(rows=8, cols=11)
table.alignment = WD_TABLE_ALIGNMENT.CENTER
table.autofit = False

headers = ["Escenario", "Conc.", "Pet.", "Resp. Error", "Req/s", "Media ms", "p50 ms", "p95 ms", "p99 ms", "Máx ms", "Objetivo TP2"]
for i, h in enumerate(headers):
    cell = table.cell(0, i)
    cell.text = h
    set_cell_background(cell, "1E3A8A") # Azul Oscuro
    p = cell.paragraphs[0]
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = p.runs[0]
    run.font.bold = True
    run.font.size = Pt(7)
    run.font.color.rgb = RGBColor(255, 255, 255)

table_data = [
    ("A - moderada GET /", "100", "5.000", "0", "1.384,0", "72,3", "68", "93", "104", "157", "Cumple"),
    ("B - alta GET /", "500", "10.000", "0", "1.364,3", "366,5", "338", "426", "430", "543", "No cumple (p95)"),
    ("C - extrema GET /", "1.000", "10.000", "0", "1.430,6", "699,0", "676", "789", "819", "830", "No cumple"),
    ("D - extrema GET /", "2.000", "20.000", "0", "1.279,6", "1.563,1", "1.438", "1.627", "1.680", "2.119", "No cumple"),
    ("E - CPU GET /work", "100", "5.000", "2.966 (59,3%)", "325,5", "307,2", "22", "2.003", "2.418", "6.004", "No cumple"),
    ("E - CPU GET /work", "1.000", "5.000", "4.456 (89,1%)", "660,2", "1.514,8", "566", "4.442", "5.367", "7.418", "No cumple (colapso)"),
    ("G - POST /envios", "100", "5.000", "33 (0,7%)", "1.216,8", "82,2", "73", "118", "134", "174", "Latencia sí; 0,7% error")
]

for r_idx, row in enumerate(table_data):
    for c_idx, val in enumerate(row):
        cell = table.cell(r_idx + 1, c_idx)
        cell.text = val
        if (r_idx % 2) == 1:
            set_cell_background(cell, "F8FAFC")
        p = cell.paragraphs[0]
        if c_idx > 0:
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        run = p.runs[0]
        run.font.size = Pt(7)
        run.font.color.rgb = COLOR_TEXT
        
        # Resaltado de la columna Objetivo TP2
        if c_idx == 10:
            run.font.bold = True
            if "Cumple" in val and "No" not in val:
                set_cell_background(cell, "DEF7EC") # Verde claro
                run.font.color.rgb = COLOR_GREEN
            elif "No cumple" in val:
                set_cell_background(cell, "FDE8E8") # Rojo claro
                run.font.color.rgb = COLOR_RED
            else:
                set_cell_background(cell, "FEF08A") # Amarillo

p_nota = doc.add_paragraph()
r_nota = p_nota.add_run(
    "Nota Técnica: ab cuenta todas las respuestas, incluidas las de error. En el Escenario E solo fueron exitosas 2.034 de 5.000 peticiones (c=100) "
    "y 544 de 5.000 (c=1.000), arrojando 132 y 72 respuestas útiles por segundo respectivamente. Failed requests fue 0 en todos los escenarios "
    "porque ab contabiliza como 'failed' los problemas de transporte TCP, no los códigos HTTP de error devueltos por el proxy (Non-2xx)."
)
r_nota.font.size = Pt(7.5)
r_nota.font.italic = True
r_nota.font.color.rgb = COLOR_GRAY
p_nota.paragraph_format.space_after = Pt(4)

p_diag = doc.add_paragraph()
r_diag = p_diag.add_run(
    "Diagnóstico de CPU (docker stats durante las pruebas): En peticiones GET / las réplicas promediaron entre 12% y 25% de uso de CPU y NGINX 40-50%, "
    "sin acercarse al tope de 0.5 CPU por réplica (~50%). En GET /work con cálculo intensivo, las réplicas alcanzaron su tope máximo de 50-54% (agotando su cuota CFS), "
    "mientras NGINX se mantuvo en 21-37%. Máximas conexiones activas en NGINX: 1.929 en el Escenario D y 1.001 en el Escenario E (c=1.000)."
)
r_diag.font.size = Pt(7.5)
r_diag.font.color.rgb = COLOR_TEXT
p_diag.paragraph_format.space_after = Pt(8)

# ------------------------------------------------------------------------------
# 5. ANÁLISIS CRÍTICO Y TIEMPO REAL
# ------------------------------------------------------------------------------
h5 = doc.add_heading("5. Análisis Crítico, Justificación y Preguntas de Coloquio", level=1)
h5.paragraph_format.space_before = Pt(12)
h5.paragraph_format.space_after = Pt(4)

p = doc.add_paragraph(
    "5.1 ¿En qué punto exacto se degrada el sistema y por qué?\n"
    "El sistema presenta dos comportamientos radicalmente diferentes según la naturaleza de la carga:\n"
    "1. Degradación por Encolamiento de Red (Escenarios B, C y D): Con peticiones I/O ligeras, la CPU permanece ociosa (< 25%). Sin embargo, al escalar de 100 a 500 y 1.000 usuarios concurrentes, cada réplica debe sostener cientos de sockets TCP abiertos simultáneamente. El tiempo que las solicitudes pasan esperando en el buffer de red (backlog) antes de ser despachadas por el event loop de Uvicorn eleva la latencia: el p95 pasa de 93 ms (Cumple) a 426 ms y 789 ms (No Cumple).\n"
    "2. Colapso por Saturación de CPU (Escenario E): Con operaciones CPU-bound (/work), el hilo monohilo de Python es monopolizado por el cálculo matemático. Al estar acotados por docker-compose a cpus: '0.50', los contenedores agotan su cuota de 50 ms por ciclo y el planificador CFS del kernel Linux suspende forzosamente su ejecución (CPU Throttling). Las peticiones colapsan los buffers, expiran los timeouts de Nginx y se produce entre un 59% y 89% de errores HTTP."
)
p.paragraph_format.line_spacing = 1.15
p.paragraph_format.space_after = Pt(6)

p = doc.add_paragraph(
    "5.2 Cumplimiento de Restricciones de Tiempo Real:\n"
    "• Hard Real-Time (Tiempo Real Estricto): NO CUMPLE bajo ninguna circunstancia. En estos sistemas, exceder un plazo temporal estricto (ej. deadline < 50 ms) invalida el resultado y constituye un fallo crítico del sistema. La variabilidad del kernel y la virtualización en Docker genera colas en el percentil 99 que superan con creces cualquier cota determinística.\n"
    "• Soft Real-Time (Web Transaccional / Objetivo TP2):\n"
    "  - CUMPLE holgadamente en el Escenario A (p95 = 93 ms <= 300 ms, p99 = 104 ms <= 800 ms, 0% errores).\n"
    "  - NO CUMPLE en los Escenarios B, C y D por exceso de latencia p95/p99 debida al encolamiento de conexiones concurrentes.\n"
    "  - NO CUMPLE en el Escenario E debido al colapso por saturación de CPU, donde demoras de 2 a 4 segundos y pérdidas del 60-90% de paquetes destruyen cualquier estándar de calidad de servicio."
)
p.paragraph_format.line_spacing = 1.15
p.paragraph_format.space_after = Pt(6)

p = doc.add_paragraph(
    "5.3 Cómo manipular el sistema en el laboratorio (Trampas de Coloquio):\n"
    "• ¿Cómo hacer que lo que CUMPLE (Escenario A) NO CUMPLA? 1) Reducir la cuota de CPU en Compose a cpus: '0.05' (el kernel suspenderá constantemente a los contenedores inflando el p95); 2) Apagar 2 réplicas (docker stop app2 app3) para saturar la única restante; 3) Quitar la directiva keepalive 32 en Nginx para forzar el costo de handshakes TCP completos por cada request.\n"
    "• ¿Cómo hacer que lo que NO CUMPLE (Escenario B o C) PASE A CUMPLIR? 1) Escalar horizontalmente de 3 a 8 réplicas para reducir las conexiones simultáneas por contenedor; 2) Configurar Uvicorn con múltiples workers (--workers 4) para procesar colas de red en paralelo.\n"
    "• ¿Cómo resolver el colapso del Escenario E? Desacoplar la arquitectura: el endpoint HTTP no debe calcular la ruta sincrónicamente; debe encolar la tarea en RabbitMQ/Kafka, responder 202 Accepted de inmediato (latencia < 20 ms), y procesar el cálculo con workers asíncronos en segundo plano."
)
p.paragraph_format.line_spacing = 1.15
p.paragraph_format.space_after = Pt(8)

# ------------------------------------------------------------------------------
# 6. CONCLUSIONES
# ------------------------------------------------------------------------------
h6 = doc.add_heading("6. Conclusiones y Recomendaciones de Ingeniería", level=1)
h6.paragraph_format.space_before = Pt(12)
h6.paragraph_format.space_after = Pt(4)

conclusiones = [
    "1. Validación de la IaC y Automatización: Se logró un despliegue Cloud-Native 100% reproducible, declarativo y resiliente con exactamente un balanceador y tres réplicas operativas mediante un único comando docker compose up -d.",
    "2. Resiliencia Demostrada (Zero Downtime): La integración de Health Checks en el proxy Nginx garantiza la continuidad operativa total: la desconexión imprevista de una réplica es absorbida en milisegundos sin arrojar errores al usuario final.",
    "3. Ruta hacia la Escalabilidad Elástica (Kubernetes / HPA): Para neutralizar la degradación por saturación de CPU observada en el Escenario E, la arquitectura debe evolucionar hacia un orquestador que soporte Horizontal Pod Autoscaling (HPA) basado en métricas de CPU (> 70%), permitiendo que el clúster escale dinámicamente de 3 a 10+ réplicas de forma automática."
]
add_callout(doc, conclusiones, bg_hex="F7FAFC", border_hex="38A169")

doc.save(str(output_path))
print(f"[EXITO] Documento DOCX actualizado con imágenes incrustadas: {output_path}")
