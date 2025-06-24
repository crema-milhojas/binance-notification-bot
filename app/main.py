from dotenv import load_dotenv
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routes import p2p
from apscheduler.schedulers.background import BackgroundScheduler
from .services.monitoring_service import MonitoringService

load_dotenv()

# Definición de FastAPI
app = FastAPI(
    title="Binance Notification Bot",
    description="Api para notificaciones en Binance",
    version="1.0.0"
)
print("Ejecutando en entorno: ", os.environ.get("ENVIRONMENT"))

# Middleware CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Rutas de la aplicación
app.include_router(p2p.router, prefix="/v1/p2p", tags=["P2P"])

# Ejecución automática de tareas
# scheduler = BackgroundScheduler()
# scheduler.add_job(MonitoringService.consult_market_usdt, 'interval', seconds=10)
# scheduler.start()

@app.get("/")
async def root():
    return {"message": "¡API bot de notificaciones de Binance!"}