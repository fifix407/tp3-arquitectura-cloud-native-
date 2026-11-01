#!/usr/bin/env python3
"""
Generador del Informe Académico Formal en formato PDF para el Trabajo Práctico N° 3.
Sincronizado al 100% con la estructura, capturas, tablas y análisis del documento DOCX.
Utiliza Microsoft Edge en modo headless para compilar HTML+CSS a un PDF idéntico y profesional.
"""

import os
import subprocess
import shutil
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
OUTPUT_HTML = BASE_DIR / "report.html"
OUTPUT_PDF = BASE_DIR / "TP3_Arquitectura_Cloud_Native_Astorga_Bustos_Militello.pdf"

desktop = Path(os.environ["USERPROFILE"]) / "OneDrive" / "Escritorio"
if not desktop.exists():
    desktop = Path(os.environ["USERPROFILE"]) / "Desktop"

img_dir = Path(os.environ["USERPROFILE"]) / "OneDrive" / "Imágenes" / "Capturas de pantalla"
img_cap1 = (img_dir / "Captura de pantalla 2026-11-01 200138.png").as_uri()
img_cap2 = (img_dir / "Captura de pantalla 2026-11-01 193423.png").as_uri()
img_cap3 = (img_dir / "Captura de pantalla 2026-11-01 190214.png").as_uri()
img_cap4 = (img_dir / "Captura de pantalla 2026-11-01 190306.png").as_uri()

html_content = f"""<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<title>Trabajo Práctico N° 3: Despliegue de Arquitectura Cloud-Native</title>
<style>
    @page {{
        size: A4;
        margin: 18mm 16mm 18mm 16mm;
    }}
    body {{
        font-family: 'Segoe UI', -apple-system, BlinkMacSystemFont, Roboto, Helvetica, Arial, sans-serif;
        color: #2d3748;
        line-height: 1.5;
        font-size: 9pt;
        margin: 0;
        padding: 0;
    }}
    .header-banner {{
        border-bottom: 2px solid #2b6cb0;
        padding-bottom: 6px;
        margin-bottom: 12px;
    }}
    .univ-info {{
        font-size: 8pt;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        color: #718096;
        font-weight: 700;
        margin-bottom: 2px;
    }}
    h1 {{
        font-size: 15.5pt;
        color: #1a365d;
        margin: 2px 0;
        font-weight: 700;
        line-height: 1.2;
    }}
    .subtitle {{
        font-size: 10pt;
        color: #2b6cb0;
        font-weight: 600;
        margin-bottom: 8px;
    }}
    .callout {{
        background-color: #f7fafc;
        border: 1px solid #e2e8f0;
        border-left: 4px solid #3182ce;
        border-radius: 4px;
        padding: 8px 12px;
        font-size: 8.5pt;
        margin-bottom: 14px;
    }}
    .callout-green {{
        background-color: #f7fafc;
        border: 1px solid #e2e8f0;
        border-left: 4px solid #38a169;
        border-radius: 4px;
        padding: 8px 12px;
        font-size: 8.5pt;
        margin-bottom: 14px;
    }}
    .callout-blue {{
        background-color: #ebf8ff;
        border: 1px solid #bee3f8;
        border-left: 4px solid #3182ce;
        border-radius: 4px;
        padding: 8px 12px;
        font-size: 8.5pt;
        margin-bottom: 14px;
    }}
    .callout ul, .callout-blue ul, .callout-green ol {{
        margin: 4px 0 0 16px;
        padding: 0;
    }}
    .callout li, .callout-blue li, .callout-green li {{
        margin-bottom: 4px;
    }}
    h2 {{
        font-size: 11.5pt;
        color: #1a365d;
        margin: 14px 0 6px 0;
        padding-bottom: 3px;
        border-bottom: 1px solid #e2e8f0;
    }}
    p {{
        margin: 0 0 7px 0;
        text-align: justify;
    }}
    .image-box {{
        background-color: #f8fafc;
        border: 1px solid #cbd5e1;
        border-radius: 6px;
        padding: 8px;
        margin: 10px 0 14px 0;
        text-align: center;
        page-break-inside: avoid;
    }}
    .image-box img {{
        max-width: 98%;
        height: auto;
        border-radius: 4px;
        border: 1px solid #e2e8f0;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
    }}
    .image-caption {{
        margin-top: 6px;
        font-size: 8pt;
        color: #1a365d;
        font-weight: bold;
    }}
    .image-desc {{
        font-size: 7.5pt;
        color: #64748b;
        font-style: italic;
        margin-top: 2px;
    }}
    table {{
        width: 100%;
        border-collapse: collapse;
        margin: 8px 0 6px 0;
        font-size: 7pt;
    }}
    th {{
        background-color: #1e3a8a;
        color: #ffffff;
        font-weight: 700;
        padding: 4px 5px;
        border: 1px solid #1e3a8a;
        text-align: center;
    }}
    td {{
        padding: 4px 5px;
        border: 1px solid #cbd5e1;
        color: #2d3748;
    }}
    tr:nth-child(even) td {{
        background-color: #f8fafc;
    }}
    .text-center {{
        text-align: center;
    }}
    .badge-cumple {{
        background-color: #def7ec;
        color: #276749;
        font-weight: bold;
        text-align: center;
    }}
    .badge-nocumple {{
        background-color: #fde8e8;
        color: #c53030;
        font-weight: bold;
        text-align: center;
    }}
    .badge-parcial {{
        background-color: #fef08a;
        color: #854d0e;
        font-weight: bold;
        text-align: center;
    }}
    .note-text {{
        font-size: 7.5pt;
        font-style: italic;
        color: #718096;
        margin-bottom: 4px;
        line-height: 1.35;
    }}
    .diag-text {{
        font-size: 7.5pt;
        color: #2d3748;
        margin-bottom: 10px;
        line-height: 1.35;
    }}
    .page-break {{
        page-break-before: always;
    }}
</style>
</head>
<body>

<div class="header-banner">
    <div class="univ-info">Universidad Champagnat — Licenciatura en Sistemas de Información (Ciclo 2026)</div>
    <h1>Trabajo Práctico N° 3: Despliegue de Arquitectura Cloud-Native</h1>
    <div class="subtitle">Validación de Atributos de Calidad, Balanceo de Carga L7 y Pruebas de Estrés en Contenedores</div>
</div>

<div class="callout">
    <strong>Integrantes del Grupo:</strong> Lucía Astorga, Emmanuel Bustos, Santiago Militello<br>
    <strong>Empresa Caso de Estudio:</strong> GlobalLogistics S.A. — Plataforma Distribuida de Telemetría<br>
    <strong>Repositorio Oficial Git:</strong> <a href="https://github.com/fifix407/tp3-arquitectura-cloud-native-" target="_blank" style="color: #2b6cb0; font-weight: bold; text-decoration: none;">https://github.com/fifix407/tp3-arquitectura-cloud-native-</a><br>
    <strong>Criterio de Evaluación SLA (Objetivo TP2):</strong> p95 &le; 300 ms, p99 &le; 800 ms, 0 errores HTTP (non-2xx)
</div>

<h2>1. Resumen Ejecutivo y Contexto del Desafío</h2>
<p>
El presente informe documenta la solución técnica desarrollada para GlobalLogistics S.A. ante la necesidad crítica de certificar que su nueva infraestructura de microservicios distribuida soporte los picos transaccionales comerciales sin degradación crítica ni intervención operativa manual.
</p>
<p>
Como Arquitectos Cloud, se diseñó e implementó un entorno de infraestructura virtualizada basada en contenedores Docker y orquestada mediante manifiestos declarativos de Infraestructura como Código (IaC). La topología cuenta con un balanceador de carga de Capa 7 (Nginx Reverse Proxy) y un clúster de tres (3) réplicas activas de una API REST de telemetría y logística desarrollada con Python 3.12 y FastAPI. Se evaluó experimentalmente la resiliencia ante contingencias de red, el comportamiento de los mecanismos de Health Checks y el rendimiento temporal frente a una matriz exhaustiva de carga mediante Apache Benchmark (concurrencia de 100 a 2.000 usuarios y endpoints de cómputo CPU-bound intensivo).
</p>

<h2>2. Configuración del Entorno e IaC (Consigna 1 - 30 Puntos)</h2>
<p>
Para garantizar reproducibilidad determinística y cumplir con las mejores prácticas Cloud-Native, la infraestructura completa fue modelada mediante el manifiesto <code>docker-compose.yml</code>. La especificación orquesta exactamente un (1) balanceador de carga y tres (3) réplicas independientes del microservicio, asociadas a una red virtual tipo bridge personalizada (<code>globallogistics_net</code>).
</p>

<div class="callout-blue">
    <strong>Principios Arquitectónicos Aplicados en IaC:</strong>
    <ul>
        <li><strong>Arranque Condicional Basado en Salud (<code>condition: service_healthy</code>):</strong> Nginx no expone el puerto ni despacha tráfico hasta que las 3 réplicas superan su prueba interna de Health Check (/health).</li>
        <li><strong>Aislamiento de Recursos (Limits):</strong> Cada réplica está acotada estrictamente a 0.50 CPU y 512MB RAM, lo que permite observar matemáticamente la saturación de procesamiento bajo estrés.</li>
        <li><strong>Seguridad por Aislamiento de Red:</strong> Las réplicas no publican sus puertos en la interfaz del host físico (0.0.0.0), quedando accesibles exclusivamente a través de la red interna de Docker desde Nginx.</li>
    </ul>
</div>

<div class="image-box">
    <img src="{img_cap1}" alt="Captura 1: docker compose ps">
    <div class="image-caption">📸 CAPTURA 1: ESTADO DEL CLÚSTER DE CONTENEDORES (docker compose ps)</div>
    <div class="image-desc">Evidencia de ejecución en terminal: 1 balanceador Nginx (globallogistics_loadbalancer en puerto 8080) y 3 réplicas de microservicio (globallogistics_app_1, 2, 3) en estado 'Up' y 'healthy'.</div>
</div>

<div class="page-break"></div>

<h2>3. Implementación del Componente y Balanceo (Consigna 2 - 30 Puntos)</h2>
<p>
El microservicio fue implementado en Python 3.12 con FastAPI sobre el servidor ASGI Uvicorn. Cumple con el requisito estricto de retornar el Hostname / Container ID en el endpoint raíz mediante la llamada al sistema <code>socket.gethostname()</code>, además de incorporar endpoints especializados para comprobación de estado (<code>/health</code>) y trabajo CPU-bound (<code>/work</code> o <code>/stress</code>).
</p>
<p>
Nginx actúa como Reverse Proxy L7 con balanceo Round-Robin y Health Checks pasivos mediante <code>max_fails=3</code> y <code>fail_timeout=10s</code>. La directiva <code>proxy_next_upstream</code> asegura que, ante cualquier fallo o timeout en una réplica, la petición se reintente de inmediato contra otra réplica viva (Zero Downtime).
</p>

<div class="image-box">
    <img src="{img_cap2}" alt="Captura 2: verify_loadbalancing.ps1">
    <div class="image-caption">📸 CAPTURA 2: ROTACIÓN DE CONTAINER IDS EN BALANCEADOR ROUND-ROBIN (verify_loadbalancing.ps1)</div>
    <div class="image-desc">Evidencia de ejecución: Peticiones consecutivas a http://localhost:8080/ alternando equitativamente entre los tres Container IDs (1/3 por réplica) con respuestas 200 OK y latencias menores a 10 ms.</div>
</div>

<h2>4. Pruebas de Estrés y Atributos de Calidad (Consigna 3 - 40 Puntos)</h2>
<p>
<strong>4.1 Metodología de Pruebas:</strong><br>
• <strong>Herramienta:</strong> Apache Benchmark 2.3 ejecutado dentro de la red virtual contra el balanceador: <code>ab -k -l -n &lt;N&gt; -c &lt;C&gt; &lt;URL&gt;</code>. El flag <code>-l</code> evita que ab cuente como falla las pequeñas diferencias de bytes debidas a los distintos IDs de contenedor y timestamps; el flag <code>-k</code> simula conexiones persistentes Keep-Alive.<br>
• <strong>Limitación de Aislamiento:</strong> ab, NGINX, las réplicas y el motor Docker comparten la misma máquina host, por lo que el tráfico atraviesa la pila de virtualización, introduciendo overhead en valores absolutos.
</p>

<div class="image-box">
    <img src="{img_cap3}" alt="Captura 3: Apache Benchmark Moderado">
    <div class="image-caption">📸 CAPTURA 3: SALIDA DE APACHE BENCHMARK - ESCENARIO MODERADO (100 CONCURRENTES)</div>
    <div class="image-desc">Evidencia de prueba de carga moderada: Throughput de ~1.300 req/s, latencia media de 72 ms y p95 de 93 ms sin errores de transporte (CUMPLE con holgura el SLA TP2).</div>
</div>

<div class="page-break"></div>

<div class="image-box">
    <img src="{img_cap4}" alt="Captura 4: Apache Benchmark CPU">
    <div class="image-caption">📸 CAPTURA 4: SALIDA DE APACHE BENCHMARK - ESCENARIO SATURACIÓN DE CPU</div>
    <div class="image-desc">Evidencia de prueba de estrés computacional: Fuerte caída de Throughput, degradación severa de latencia alcanzando percentiles de 2 a 4 segundos por agotamiento de cuota CFS (NO CUMPLE SLA).</div>
</div>

<p>
<strong>4.2 Matriz Completa de Resultados y Criterio de Cumplimiento (Objetivo TP2):</strong><br>
Los percentiles indican el tiempo por debajo del cual se atendió ese porcentaje de las peticiones (p95: el 95%). El criterio formal del Objetivo TP2 exige estrictamente: <strong>p95 &le; 300 ms, p99 &le; 800 ms y 0 errores HTTP (non-2xx)</strong>.
</p>

<table>
    <thead>
        <tr>
            <th>Escenario</th>
            <th>Conc.</th>
            <th>Pet.</th>
            <th>Resp. Error</th>
            <th>Req/s</th>
            <th>Media ms</th>
            <th>p50 ms</th>
            <th>p95 ms</th>
            <th>p99 ms</th>
            <th>Máx ms</th>
            <th>Objetivo TP2</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td><strong>A - moderada GET /</strong></td>
            <td class="text-center">100</td>
            <td class="text-center">5.000</td>
            <td class="text-center">0</td>
            <td class="text-center">1.384,0</td>
            <td class="text-center">72,3</td>
            <td class="text-center">68</td>
            <td class="text-center">93</td>
            <td class="text-center">104</td>
            <td class="text-center">157</td>
            <td class="badge-cumple">Cumple</td>
        </tr>
        <tr>
            <td><strong>B - alta GET /</strong></td>
            <td class="text-center">500</td>
            <td class="text-center">10.000</td>
            <td class="text-center">0</td>
            <td class="text-center">1.364,3</td>
            <td class="text-center">366,5</td>
            <td class="text-center">338</td>
            <td class="text-center">426</td>
            <td class="text-center">430</td>
            <td class="text-center">543</td>
            <td class="badge-nocumple">No cumple (p95)</td>
        </tr>
        <tr>
            <td><strong>C - extrema GET /</strong></td>
            <td class="text-center">1.000</td>
            <td class="text-center">10.000</td>
            <td class="text-center">0</td>
            <td class="text-center">1.430,6</td>
            <td class="text-center">699,0</td>
            <td class="text-center">676</td>
            <td class="text-center">789</td>
            <td class="text-center">819</td>
            <td class="text-center">830</td>
            <td class="badge-nocumple">No cumple</td>
        </tr>
        <tr>
            <td><strong>D - extrema GET /</strong></td>
            <td class="text-center">2.000</td>
            <td class="text-center">20.000</td>
            <td class="text-center">0</td>
            <td class="text-center">1.279,6</td>
            <td class="text-center">1.563,1</td>
            <td class="text-center">1.438</td>
            <td class="text-center">1.627</td>
            <td class="text-center">1.680</td>
            <td class="text-center">2.119</td>
            <td class="badge-nocumple">No cumple</td>
        </tr>
        <tr>
            <td><strong>E - CPU GET /work</strong></td>
            <td class="text-center">100</td>
            <td class="text-center">5.000</td>
            <td class="text-center">2.966 (59,3%)</td>
            <td class="text-center">325,5</td>
            <td class="text-center">307,2</td>
            <td class="text-center">22</td>
            <td class="text-center">2.003</td>
            <td class="text-center">2.418</td>
            <td class="text-center">6.004</td>
            <td class="badge-nocumple">No cumple</td>
        </tr>
        <tr>
            <td><strong>E - CPU GET /work</strong></td>
            <td class="text-center">1.000</td>
            <td class="text-center">5.000</td>
            <td class="text-center">4.456 (89,1%)</td>
            <td class="text-center">660,2</td>
            <td class="text-center">1.514,8</td>
            <td class="text-center">566</td>
            <td class="text-center">4.442</td>
            <td class="text-center">5.367</td>
            <td class="text-center">7.418</td>
            <td class="badge-nocumple">No cumple (colapso)</td>
        </tr>
        <tr>
            <td><strong>G - POST /envios</strong></td>
            <td class="text-center">100</td>
            <td class="text-center">5.000</td>
            <td class="text-center">33 (0,7%)</td>
            <td class="text-center">1.216,8</td>
            <td class="text-center">82,2</td>
            <td class="text-center">73</td>
            <td class="text-center">118</td>
            <td class="text-center">134</td>
            <td class="text-center">174</td>
            <td class="badge-parcial">Latencia sí; 0,7% error</td>
        </tr>
    </tbody>
</table>

<div class="note-text">
<strong>Nota Técnica:</strong> ab cuenta todas las respuestas, incluidas las de error. En el Escenario E solo fueron exitosas 2.034 de 5.000 peticiones (c=100) y 544 de 5.000 (c=1.000), arrojando 132 y 72 respuestas útiles por segundo respectivamente. Failed requests fue 0 en todos los escenarios porque ab contabiliza como 'failed' los problemas de transporte TCP, no los códigos HTTP de error devueltos por el proxy (Non-2xx).
</div>

<div class="diag-text">
<strong>Diagnóstico de CPU (docker stats durante las pruebas):</strong> En peticiones GET / las réplicas promediaron entre 12% y 25% de uso de CPU y NGINX 40-50%, sin acercarse al tope de 0.5 CPU por réplica (~50%). En GET /work con cálculo intensivo, las réplicas alcanzaron su tope máximo de 50-54% (agotando su cuota CFS), mientras NGINX se mantuvo en 21-37%. Máximas conexiones activas en NGINX: 1.929 en el Escenario D y 1.001 en el Escenario E (c=1.000).
</div>

<h2>5. Análisis Crítico, Justificación y Preguntas de Coloquio</h2>
<p>
<strong>5.1 ¿En qué punto exacto se degrada el sistema y por qué?</strong><br>
El sistema presenta dos comportamientos radicalmente diferentes según la naturaleza de la carga:<br>
<strong>1. Degradación por Encolamiento de Red (Escenarios B, C y D):</strong> Con peticiones I/O ligeras, la CPU permanece ociosa (&lt; 25%). Sin embargo, al escalar de 100 a 500 y 1.000 usuarios concurrentes, cada réplica debe sostener cientos de sockets TCP abiertos simultáneamente. El tiempo que las solicitudes pasan esperando en el buffer de red (backlog) antes de ser despachadas por el event loop de Uvicorn eleva la latencia: el p95 pasa de 93 ms (Cumple) a 426 ms y 789 ms (No Cumple).<br>
<strong>2. Colapso por Saturación de CPU (Escenario E):</strong> Con operaciones CPU-bound (/work), el hilo monohilo de Python es monopolizado por el cálculo matemático. Al estar acotados por docker-compose a <code>cpus: '0.50'</code>, los contenedores agotan su cuota de 50 ms por ciclo y el planificador CFS del kernel Linux suspende forzosamente su ejecución (CPU Throttling). Las peticiones colapsan los buffers, expiran los timeouts de Nginx y se produce entre un 59% y 89% de errores HTTP.
</p>

<p>
<strong>5.2 Cumplimiento de Restricciones de Tiempo Real:</strong><br>
• <strong>Hard Real-Time (Tiempo Real Estricto):</strong> NO CUMPLE bajo ninguna circunstancia. En estos sistemas, exceder un plazo temporal estricto (ej. deadline &lt; 50 ms) invalida el resultado y constituye un fallo crítico del sistema. La variabilidad del kernel y la virtualización en Docker genera colas en el percentil 99 que superan con creces cualquier cota determinística.<br>
• <strong>Soft Real-Time (Web Transaccional / Objetivo TP2):</strong><br>
&nbsp;&nbsp;- <strong>CUMPLE holgadamente</strong> en el Escenario A (p95 = 93 ms &le; 300 ms, p99 = 104 ms &le; 800 ms, 0% errores).<br>
&nbsp;&nbsp;- <strong>NO CUMPLE</strong> en los Escenarios B, C y D por exceso de latencia p95/p99 debida al encolamiento de conexiones concurrentes.<br>
&nbsp;&nbsp;- <strong>NO CUMPLE</strong> en el Escenario E debido al colapso por saturación de CPU, donde demoras de 2 a 4 segundos y pérdidas del 60-90% de paquetes destruyen cualquier estándar de calidad de servicio.
</p>

<p>
<strong>5.3 Cómo manipular el sistema en el laboratorio (Trampas de Coloquio):</strong><br>
• <strong>¿Cómo hacer que lo que CUMPLE (Escenario A) NO CUMPLA?</strong> 1) Reducir la cuota de CPU en Compose a <code>cpus: '0.05'</code> (el kernel suspenderá constantemente a los contenedores inflando el p95); 2) Apagar 2 réplicas (<code>docker stop app2 app3</code>) para saturar la única restante; 3) Quitar la directiva <code>keepalive 32</code> en Nginx para forzar el costo de handshakes TCP completos por cada request.<br>
• <strong>¿Cómo hacer que lo que NO CUMPLE (Escenario B o C) PASE A CUMPLIR?</strong> 1) Escalar horizontalmente de 3 a 8 réplicas para reducir las conexiones simultáneas por contenedor; 2) Configurar Uvicorn con múltiples workers (<code>--workers 4</code>) para procesar colas de red en paralelo.<br>
• <strong>¿Cómo resolver el colapso del Escenario E?</strong> Desacoplar la arquitectura: el endpoint HTTP no debe calcular la ruta sincrónicamente; debe encolar la tarea en RabbitMQ/Kafka, responder 202 Accepted de inmediato (latencia &lt; 20 ms), y procesar el cálculo con workers asíncronos en segundo plano.
</p>

<h2>6. Conclusiones y Recomendaciones de Ingeniería</h2>
<div class="callout-green">
    <ol>
        <li><strong>Validación de la IaC y Automatización:</strong> Se logró un despliegue Cloud-Native 100% reproducible, declarativo y resiliente con exactamente un balanceador y tres réplicas operativas mediante un único comando <code>docker compose up -d</code>.</li>
        <li><strong>Resiliencia Demostrada (Zero Downtime):</strong> La integración de Health Checks en el proxy Nginx garantiza la continuidad operativa total: la desconexión imprevista de una réplica es absorbida en milisegundos sin arrojar errores al usuario final.</li>
        <li><strong>Ruta hacia la Escalabilidad Elástica (Kubernetes / HPA):</strong> Para neutralizar la degradación por saturación de CPU observada en el Escenario E, la arquitectura debe evolucionar hacia un orquestador que soporte <strong>Horizontal Pod Autoscaling (HPA)</strong> basado en métricas de CPU (&gt; 70%), permitiendo que el clúster escale dinámicamente de 3 a 10+ réplicas de forma automática.</li>
    </ol>
</div>

</body>
</html>
"""

with open(OUTPUT_HTML, "w", encoding="utf-8") as f:
    f.write(html_content)

print(f"[OK] Documento HTML generado en: {OUTPUT_HTML}")

# Renderizar HTML a PDF mediante Microsoft Edge Headless
edge_path = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
if not os.path.exists(edge_path):
    edge_path = r"C:\Program Files\Microsoft\Edge\Application\msedge.exe"

print("Compilando PDF académico con Microsoft Edge...")
cmd = [
    edge_path,
    "--headless",
    "--disable-gpu",
    "--no-pdf-header-footer",
    f"--print-to-pdf={OUTPUT_PDF}",
    str(OUTPUT_HTML)
]

res = subprocess.run(cmd, capture_output=True, text=True)
if res.returncode == 0 and OUTPUT_PDF.exists():
    dest_pdf = desktop / "TP3_Arquitectura_Cloud_Native_Astorga_Bustos_Militello.pdf"
    shutil.copyfile(OUTPUT_PDF, dest_pdf)
    
    # También actualizar el nombre corto en Desktop para comodidad
    short_pdf = desktop / "TP3_Arquitectura_Cloud_Native.pdf"
    shutil.copyfile(OUTPUT_PDF, short_pdf)
    
    print(f"[EXITO] PDF compilado satisfactoriamente: {OUTPUT_PDF} ({OUTPUT_PDF.stat().st_size} bytes)")
    print(f"[EXITO] PDF copiado al Escritorio: {dest_pdf}")
else:
    print(f"Error generando PDF: {res.stderr}")
