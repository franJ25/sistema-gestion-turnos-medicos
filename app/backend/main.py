import os
from pathlib import Path
from dotenv import load_dotenv

# Cargar variables de entorno desde .env del backend
_env_path = Path(__file__).resolve().parent / ".env"
load_dotenv(_env_path)

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.backend.api.routes import router as api_router
from app.backend.db.db import Base, engine
from app.backend.db.init_estados import init_estados
from app.backend.db.init_roles_and_admin import init_roles_and_admin
# ⭐ Crear tablas si no existen
Base.metadata.create_all(bind=engine)


# ⭐ Nuevo sistema de Lifespan
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Se ejecuta AL INICIAR FastAPI
    print("▶ Cargando estados en la base de datos...")
    init_estados()
    init_roles_and_admin()
    print("✔ Estados y roles inicializados correctamente.")

    yield  # ← punto donde la app ya está levantada

    # Se ejecuta AL APAGAR FastAPI (opcional)
    print("▶ Finalizando Turnero Médico API...")

origins = [
    "http://localhost:3000",
    # "https://tu-sitio-en-produccion.com", 
]
# ⭐ Declaración correcta del objeto FastAPI usando lifespan
app = FastAPI(title="Turnero Médico API", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Permite todos los orígenes
    allow_credentials=True,
    allow_methods=["*"],  # Permite todos los métodos
    allow_headers=["*"],  # Permite todos los encabezados
)


# ⭐ Incluir routers
app.include_router(api_router, prefix="/api")


@app.get("/")
def root():
    return {"msg": "API funcionando correctamente"}
