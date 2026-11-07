import os
from fastapi import FastAPI, Depends, HTTPException, Security
from fastapi.security import APIKeyHeader
from pydantic import BaseModel
from dotenv import load_dotenv

from app.database import db
from app.models import ProductoCreate, EmpleadoCreate, MovimientoCreate
from app import crud
from app.agente import analizar_negocio

# ==========================================
# CONFIGURACIÓN Y SEGURIDAD
# ==========================================
load_dotenv()
API_PASSWORD = os.getenv("API_PASSWORD", "api.1std")

app = FastAPI(
    title="MyGestor API",
    description="Motor backend para gestión de negocios con Agente IA.",
    version="1.0.0"
)

api_key_header = APIKeyHeader(
    name="X-API-Key", 
    auto_error=False, 
    description="Escribe la contraseña: api.1std"
)

def verificar_password(api_key: str = Security(api_key_header)):
    if api_key != API_PASSWORD:
        raise HTTPException(
            status_code=403, 
            detail="Acceso denegado. Contraseña incorrecta."
        )
    return api_key

# ==========================================
# EVENTOS DE INICIO
# ==========================================
@app.on_event("startup")
def startup_event():
    db.crear_tablas()

# ==========================================
# RUTAS BÁSICAS
# ==========================================
@app.get("/", tags=["Root"])
def read_root():
    return {"mensaje": "Bienvenido a MyGestor API. Ve a /docs para probar los endpoints."}

# ==========================================
# RUTAS DE PRODUCTOS
# ==========================================
@app.post("/productos/", tags=["Productos"], dependencies=[Depends(verificar_password)])
def api_crear_producto(prod: ProductoCreate):
    return crud.crear_producto(prod)

@app.get("/productos/", tags=["Productos"], dependencies=[Depends(verificar_password)])
def api_obtener_productos():
    return crud.obtener_productos()

# ==========================================
# RUTAS DE EMPLEADOS
# ==========================================
@app.post("/empleados/", tags=["Empleados"], dependencies=[Depends(verificar_password)])
def api_crear_empleado(emp: EmpleadoCreate):
    return crud.crear_empleado(emp)

@app.get("/empleados/", tags=["Empleados"], dependencies=[Depends(verificar_password)])
def api_obtener_empleados():
    return crud.obtener_empleados()

# ==========================================
# RUTAS DE MOVIMIENTOS
# ==========================================
@app.post("/movimientos/", tags=["Movimientos"], dependencies=[Depends(verificar_password)])
def api_registrar_movimiento(mov: MovimientoCreate):
    resultado = crud.registrar_movimiento(mov)
    if "error" in resultado:
        raise HTTPException(status_code=400, detail=resultado["error"])
    return resultado

@app.get("/movimientos/", tags=["Movimientos"], dependencies=[Depends(verificar_password)])
def api_obtener_movimientos():
    return crud.obtener_movimientos()

# ==========================================
# RUTAS DE BANCO
# ==========================================
@app.get("/banco/", tags=["Banco"], dependencies=[Depends(verificar_password)])
def api_obtener_banco():
    return crud.obtener_banco()

# ==========================================
# RUTAS DEL AGENTE IA
# ==========================================
class PreguntaRequest(BaseModel):
    pregunta: str

@app.post("/agente/analizar", tags=["Agente IA"], dependencies=[Depends(verificar_password)])
def api_analizar_negocio(request: PreguntaRequest):
    respuesta = analizar_negocio(request.pregunta)
    return {"respuesta": respuesta}