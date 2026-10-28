#!/usr/bin/env python3
"""
Script de automatización para pruebas de carga y estrés con Apache Benchmark.
Cubre los dos escenarios estipulados en la Consigna 3:
1. Concurrencia Moderada (100 usuarios concurrentes, endpoint principal)
2. Concurrencia Extrema / Saturación de CPU (100 usuarios concurrentes, endpoint CPU-bound)
"""

import subprocess
import json
import re
import os
from pathlib import Path

RESULTS_DIR = Path(__file__).resolve().parent.parent / "benchmark_results"
RESULTS_DIR.mkdir(parents=True, exist_ok=True)

def parse_ab_output(text: str) -> dict:
    data = {}
    
    # Extraer métricas clave
    patterns = {
        "server_software": r"Server Software:\s+(.+)",
        "server_hostname": r"Server Hostname:\s+(.+)",
        "concurrency_level": r"Concurrency Level:\s+(\d+)",
        "time_taken": r"Time taken for tests:\s+([\d\.]+)\s+seconds",
        "complete_requests": r"Complete requests:\s+(\d+)",
        "failed_requests": r"Failed requests:\s+(\d+)",
        "non_2xx_responses": r"Non-2xx responses:\s+(\d+)",
        "total_transferred": r"Total transferred:\s+(\d+)\s+bytes",
        "requests_per_sec": r"Requests per second:\s+([\d\.]+)",
        "time_per_request_mean": r"Time per request:\s+([\d\.]+)\s+\[ms\]\s+\(mean\)",
        "time_per_request_concurrent": r"Time per request:\s+([\d\.]+)\s+\[ms\]\s+\(mean, across all concurrent requests\)",
        "transfer_rate": r"Transfer rate:\s+([\d\.]+)\s+\[Kbytes/sec\] received"
    }
    
    for key, pattern in patterns.items():
        match = re.search(pattern, text)
        if match:
            val = match.group(1).strip()
            try:
                if "." in val:
                    data[key] = float(val)
                else:
                    data[key] = int(val)
            except ValueError:
                data[key] = val
        else:
            if key == "non_2xx_responses":
                data[key] = 0

    # Percentiles
    percentiles = {}
    p_pattern = re.compile(r"^\s*(\d+)%\s+(\d+)", re.MULTILINE)
    for m in p_pattern.finditer(text):
        percentiles[f"p{m.group(1)}"] = int(m.group(2))
    data["percentiles"] = percentiles

    return data

def run_ab(scenario_name: str, total_requests: int, concurrency: int, url: str) -> dict:
    print(f"\n=======================================================")
    print(f"Ejecutando {scenario_name}...")
    print(f"Requests: {total_requests} | Concurrencia: {concurrency} | URL: {url}")
    print(f"=======================================================")
    
    cmd = [
        "docker", "run", "--rm",
        "--network", "globallogistics_net",
        "httpd:alpine",
        "ab",
        "-n", str(total_requests),
        "-c", str(concurrency),
        url
    ]
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    output = result.stdout
    if result.returncode != 0 and not output:
        output = result.stderr
        print(f"Error ejecutando ab: {output}")

    # Guardar raw output
    raw_file = RESULTS_DIR / f"{scenario_name.lower().replace(' ', '_')}.txt"
    with open(raw_file, "w", encoding="utf-8") as f:
        f.write(output)
    print(f"Salida cruda guardada en: {raw_file}")
    
    parsed = parse_ab_output(output)
    parsed["scenario"] = scenario_name
    parsed["raw_output_file"] = str(raw_file)
    return parsed

def main():
    print("Iniciando suite de benchmarks Cloud-Native (Apache Benchmark)...")
    
    # Escenario 1: Concurrencia Moderada
    s1 = run_ab(
        scenario_name="scenario1_concurrencia_moderada",
        total_requests=5000,
        concurrency=100,
        url="http://globallogistics_loadbalancer/"
    )
    
    # Escenario 2: Concurrencia Extrema (Saturación de CPU)
    s2 = run_ab(
        scenario_name="scenario2_concurrencia_extrema",
        total_requests=2500,
        concurrency=100,
        url="http://globallogistics_loadbalancer/stress?iterations=2500"
    )
    
    summary = {
        "scenario_1_moderada": s1,
        "scenario_2_extrema": s2
    }
    
    summary_file = RESULTS_DIR / "summary.json"
    with open(summary_file, "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2)
        
    print(f"\n[OK] Resumen consolidado generado en: {summary_file}")
    
    print("\n--- COMPARATIVA DE RESULTADOS ---")
    print(f"{'Métrica':<35} | {'Escenario 1 (Moderado)':<25} | {'Escenario 2 (Extremo/CPU)':<25}")
    print("-" * 90)
    print(f"{'Concurrencia (usuarios)':<35} | {str(s1.get('concurrency_level', 'N/A')):<25} | {str(s2.get('concurrency_level', 'N/A')):<25}")
    print(f"{'Throughput (req/seg)':<35} | {str(s1.get('requests_per_sec', 'N/A')) + ' req/s':<25} | {str(s2.get('requests_per_sec', 'N/A')) + ' req/s':<25}")
    print(f"{'Latencia Promedio (mean)':<35} | {str(s1.get('time_per_request_mean', 'N/A')) + ' ms':<25} | {str(s2.get('time_per_request_mean', 'N/A')) + ' ms':<25}")
    print(f"{'Mediana (p50)':<35} | {str(s1.get('percentiles', {}).get('p50', 'N/A')) + ' ms':<25} | {str(s2.get('percentiles', {}).get('p50', 'N/A')) + ' ms':<25}")
    print(f"{'Percentil 95 (p95)':<35} | {str(s1.get('percentiles', {}).get('p95', 'N/A')) + ' ms':<25} | {str(s2.get('percentiles', {}).get('p95', 'N/A')) + ' ms':<25}")
    print(f"{'Percentil 99 (p99)':<35} | {str(s1.get('percentiles', {}).get('p99', 'N/A')) + ' ms':<25} | {str(s2.get('percentiles', {}).get('p99', 'N/A')) + ' ms':<25}")
    print(f"{'Fallos de red / HTTP':<35} | {str(s1.get('failed_requests', 0)):<25} | {str(s2.get('failed_requests', 0)):<25}")
    print("-" * 90)

if __name__ == "__main__":
    main()
