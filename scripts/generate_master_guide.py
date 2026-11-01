#!/usr/bin/env python3
"""
Compilador del PDF Extendido de la Guía Maestra de Estudio para el TP3.
"""

import os
import subprocess
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
TXT_PATH = BASE_DIR / "GUIA_MAESTRA_ESTUDIO_TP3.txt"
HTML_PATH = BASE_DIR / "guia_maestra.html"
PDF_PATH = BASE_DIR / "GUIA_MAESTRA_ESTUDIO_TP3.pdf"

with open(TXT_PATH, "r", encoding="utf-8") as f:
    text = f.read()

# Convertir markdown básico a HTML prolijo
import re

def text_to_html(md_text):
    lines = md_text.split("\n")
    html_lines = []
    in_list = False
    in_code = False
    
    for line in lines:
        if line.startswith("```"):
            if in_code:
                html_lines.append("</pre>")
                in_code = False
            else:
                html_lines.append("<pre>")
                in_code = True
            continue
            
        if in_code:
            html_lines.append(line)
            continue
            
        if line.startswith("# "):
            html_lines.append(f"<h1>{line[2:]}</h1>")
        elif line.startswith("## "):
            html_lines.append(f"<h2>{line[3:]}</h2>")
        elif line.startswith("### "):
            html_lines.append(f"<h3>{line[4:]}</h3>")
        elif line.startswith("* ") or line.startswith("- "):
            if not in_list:
                html_lines.append("<ul>")
                in_list = True
            html_lines.append(f"<li>{line[2:]}</li>")
        elif line.startswith("> "):
            html_lines.append(f"<div class='quote-box'>{line[2:]}</div>")
        elif line.strip() == "---":
            if in_list:
                html_lines.append("</ul>")
                in_list = False
            html_lines.append("<hr/>")
        elif line.strip() == "":
            if in_list:
                html_lines.append("</ul>")
                in_list = False
        else:
            if in_list:
                html_lines.append("</ul>")
                in_list = False
            # Negritas y código inline
            formatted = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', line)
            formatted = re.sub(r'`(.*?)`', r'<code>\1</code>', formatted)
            html_lines.append(f"<p>{formatted}</p>")
            
    if in_list:
        html_lines.append("</ul>")
    return "\n".join(html_lines)

body_html = text_to_html(text)

full_html = f"""<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<title>Guía Maestra de Estudio y Defensa Oral - TP N° 3 Cloud-Native</title>
<style>
    @page {{
        size: A4;
        margin: 18mm 16mm 18mm 16mm;
        @bottom-right {{
            content: "Página " counter(page);
            font-size: 8pt;
            color: #718096;
        }}
    }}
    body {{
        font-family: 'Segoe UI', -apple-system, BlinkMacSystemFont, Roboto, Helvetica, Arial, sans-serif;
        color: #1a202c;
        line-height: 1.5;
        font-size: 9.2pt;
        margin: 0;
        padding: 0;
    }}
    h1 {{
        font-size: 15.5pt;
        color: #1a365d;
        border-bottom: 2.5px solid #2b6cb0;
        padding-bottom: 6px;
        margin-top: 0;
        margin-bottom: 12px;
    }}
    h2 {{
        font-size: 12pt;
        color: #2c5282;
        border-bottom: 1.5px solid #cbd5e0;
        padding-bottom: 3px;
        margin-top: 18px;
        margin-bottom: 8px;
        page-break-after: avoid;
    }}
    h3 {{
        font-size: 10pt;
        color: #2d3748;
        margin-top: 12px;
        margin-bottom: 4px;
        page-break-after: avoid;
    }}
    p {{
        margin-top: 0;
        margin-bottom: 6px;
        text-align: justify;
    }}
    code {{
        font-family: 'Consolas', monospace;
        font-size: 8pt;
        background-color: #edf2f7;
        padding: 1px 4px;
        border-radius: 3px;
        color: #c53030;
    }}
    pre {{
        font-family: 'Consolas', monospace;
        font-size: 7.2pt;
        background-color: #0f172a;
        color: #e2e8f0;
        padding: 8px 10px;
        border-radius: 5px;
        line-height: 1.35;
        margin: 6px 0 10px 0;
        page-break-inside: avoid;
    }}
    .quote-box {{
        background-color: #f8fafc;
        border-left: 4px solid #3b82f6;
        padding: 8px 12px;
        border-radius: 4px;
        margin: 6px 0 10px 0;
        font-size: 8.8pt;
        color: #1e3a8a;
        page-break-inside: avoid;
    }}
    ul, ol {{
        margin-top: 3px;
        margin-bottom: 6px;
        padding-left: 20px;
    }}
    li {{
        margin-bottom: 2px;
    }}
    hr {{
        border: 0;
        border-top: 1px solid #e2e8f0;
        margin: 14px 0;
    }}
</style>
</head>
<body>
{body_html}
</body>
</html>
"""

with open(HTML_PATH, "w", encoding="utf-8") as f:
    f.write(full_html)

edge_path = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
if not os.path.exists(edge_path):
    edge_path = r"C:\Program Files\Microsoft\Edge\Application\msedge.exe"

cmd = [
    edge_path,
    "--headless",
    "--disable-gpu",
    "--no-pdf-header-footer",
    f"--print-to-pdf={PDF_PATH}",
    str(HTML_PATH)
]

res = subprocess.run(cmd, capture_output=True, text=True)
if res.returncode == 0 and PDF_PATH.exists():
    desktop = Path(os.environ["USERPROFILE"]) / "OneDrive" / "Escritorio"
    if not desktop.exists():
        desktop = Path(os.environ["USERPROFILE"]) / "Desktop"
    import shutil
    shutil.copyfile(PDF_PATH, desktop / "GUIA_MAESTRA_ESTUDIO_TP3.pdf")
    shutil.copyfile(TXT_PATH, desktop / "GUIA_MAESTRA_ESTUDIO_TP3.txt")
    print(f"[EXITO] PDF y TXT extendidos generados en el escritorio: {PDF_PATH}")
