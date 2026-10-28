import os
import time
import socket
import hashlib
from datetime import datetime, timezone
from typing import Optional
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

app = FastAPI(
    title="GlobalLogistics S.A. - Shipment & Tracking Microservice",
    description="Microservicio Cloud-Native para seguimiento logístico y alta concurrencia.",
    version="1.0.0"
)

START_TIME = time.time()
HOSTNAME = socket.gethostname()
INSTANCE_NAME = os.getenv("INSTANCE_NAME", HOSTNAME)

def get_memory_rss_mb() -> float:
    """Obtiene el uso de memoria RSS en MB de forma nativa sin dependencias externas."""
    try:
        import resource
        # ru_maxrss en Linux devuelve kilobytes
        return round(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1024, 2)
    except Exception:
        return 0.0

@app.get("/", summary="Endpoint Principal")
async def root(request: Request):
    """
    Endpoint principal exigido por la consigna:
    Debe devolver obligatoriamente el Hostname o ID del contenedor/instancia.
    """
    client_host = request.client.host if request.client else "unknown"
    return {
        "status": "success",
        "service": "GlobalLogistics S.A. - Fleet & Tracking Service",
        "container_id": HOSTNAME,
        "hostname": HOSTNAME,
        "instance_name": INSTANCE_NAME,
        "client_ip": client_host,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "architecture": "Cloud-Native Microservices",
        "load_balanced": True
    }

@app.get("/health", summary="Health Check")
async def health():
    """
    Endpoint de Health Check para comprobar el estado de la réplica por el
    balanceador de carga Nginx y Docker Compose.
    """
    return {
        "status": "UP",
        "healthy": True,
        "container_id": HOSTNAME,
        "instance_name": INSTANCE_NAME,
        "uptime_seconds": round(time.time() - START_TIME, 2),
        "memory_rss_mb": get_memory_rss_mb()
    }

@app.get("/stress", summary="Simulación de Carga CPU Intensiva")
async def stress(iterations: Optional[int] = 50000):
    """
    Endpoint para pruebas de estrés bajo concurrencia extrema (saturación de CPU).
    Simula procesamiento intensivo de optimización de rutas y algoritmos criptográficos.
    """
    start_calc = time.perf_counter()
    
    # Trabajo CPU-bound determinístico
    data = f"GlobalLogistics-RouteOptimization-{HOSTNAME}".encode()
    digest = data
    for _ in range(iterations):
        digest = hashlib.sha256(digest).digest()
        
    duration = time.perf_counter() - start_calc
    
    return {
        "status": "processed",
        "container_id": HOSTNAME,
        "instance_name": INSTANCE_NAME,
        "iterations": iterations,
        "duration_seconds": round(duration, 4),
        "hash_prefix": digest.hex()[:16]
    }
