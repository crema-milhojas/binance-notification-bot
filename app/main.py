from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routes import p2p

# Definición de FastAPI
app = FastAPI(
    title="Binance Notification Bot",
    description="Api para notificaciones en Binance",
    version="1.0.0"
)

# Middleware CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Rutas de la aplicación
app.include_router(p2p.router, prefix="/v1/monitoring", tags=["Monitoreo"])

@app.get("/")
async def root():
    return {"message": "¡API bot de notificaciones de Binance!"}