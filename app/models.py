from pydantic import BaseModel, Field
from typing import Optional

# --- MODELOS DE PRODUCTO ---
class ProductoBase(BaseModel):
    nombre: str = Field(..., min_length=1, max_length=100)
    categoria: str = Field(default="General")
    stock: float = Field(..., ge=0) # ge=0 significa "mayor o igual a 0"
    costo: float = Field(..., gt=0) # gt=0 significa "mayor que 0"
    precio_venta: float = Field(..., gt=0)

class ProductoCreate(ProductoBase):
    pass

class ProductoResponse(ProductoBase):
    id: int

# --- MODELOS DE EMPLEADO ---
class EmpleadoBase(BaseModel):
    nombre: str = Field(..., min_length=1)
    rol: str = Field(..., pattern="^(gestor|vendedor|admin)$") # Solo permite estos 3 roles
    comision_porcentaje: float = Field(default=0, ge=0, le=100)
    periodo_pago: str = Field(default="mensual", pattern="^(semanal|quincenal|mensual)$")

class EmpleadoCreate(EmpleadoBase):
    pass

class EmpleadoResponse(EmpleadoBase):
    id: int
    activo: int

# --- MODELOS DE MOVIMIENTO ---
class MovimientoBase(BaseModel):
    tipo: str = Field(..., pattern="^(venta|gasto|reinversion|pago_empleado)$")
    monto: float = Field(..., gt=0)
    descripcion: Optional[str] = None
    producto_id: Optional[int] = None
    empleado_id: Optional[int] = None

class MovimientoCreate(MovimientoBase):
    pass

class MovimientoResponse(MovimientoBase):
    id: int
    fecha: str