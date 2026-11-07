from app.database import db
from app.models import ProductoCreate, EmpleadoCreate, MovimientoCreate

# --- FUNCIONES DE PRODUCTOS ---
def crear_producto(prod: ProductoCreate):
    db.conectar()
    db.cursor.execute(
        "INSERT INTO productos (nombre, categoria, stock, costo, precio_venta) VALUES (?, ?, ?, ?, ?)",
        (prod.nombre, prod.categoria, prod.stock, prod.costo, prod.precio_venta)
    )
    db.conexion.commit()
    nuevo_id = db.cursor.lastrowid
    db.cerrar()
    return {"id": nuevo_id, **prod.model_dump()}

def obtener_productos():
    db.conectar()
    db.cursor.execute("SELECT * FROM productos ORDER BY nombre")
    filas = db.cursor.fetchall()
    db.cerrar()
    return [dict(f) for f in filas]

# --- FUNCIONES DE EMPLEADOS ---
def crear_empleado(emp: EmpleadoCreate):
    db.conectar()
    db.cursor.execute(
        "INSERT INTO empleados (nombre, rol, comision_porcentaje, periodo_pago) VALUES (?, ?, ?, ?)",
        (emp.nombre, emp.rol, emp.comision_porcentaje, emp.periodo_pago)
    )
    db.conexion.commit()
    nuevo_id = db.cursor.lastrowid
    db.cerrar()
    return {"id": nuevo_id, **emp.model_dump()}

def obtener_empleados():
    db.conectar()
    db.cursor.execute("SELECT * FROM empleados WHERE activo = 1")
    filas = db.cursor.fetchall()
    db.cerrar()
    return [dict(f) for f in filas]

# --- FUNCIONES DE MOVIMIENTOS (VENTAS/GASTOS) ---
def registrar_movimiento(mov: MovimientoCreate):
    db.conectar()
    
    # Si es una venta, restamos el stock del producto
    if mov.tipo == 'venta' and mov.producto_id:
        db.cursor.execute("SELECT stock FROM productos WHERE id = ?", (mov.producto_id,))
        prod = db.cursor.fetchone()
        if not prod:
            db.cerrar()
            return {"error": "Producto no encontrado"}
        if prod["stock"] < 1: # Asumimos venta de 1 unidad para simplificar esta fase
            db.cerrar()
            return {"error": "Stock insuficiente"}
        
        # Restamos 1 al stock
        db.cursor.execute("UPDATE productos SET stock = stock - 1 WHERE id = ?", (mov.producto_id,))

    # Insertamos el movimiento
    db.cursor.execute(
        "INSERT INTO movimientos (tipo, monto, descripcion, producto_id, empleado_id) VALUES (?, ?, ?, ?, ?)",
        (mov.tipo, mov.monto, mov.descripcion, mov.producto_id, mov.empleado_id)
    )
    db.conexion.commit()
    nuevo_id = db.cursor.lastrowid
    db.cerrar()
    return {"id": nuevo_id, **mov.model_dump()}

def obtener_movimientos():
    db.conectar()
    db.cursor.execute("SELECT * FROM movimientos ORDER BY fecha DESC")
    filas = db.cursor.fetchall()
    db.cerrar()
    return [dict(f) for f in filas]

# --- FUNCIONES DE BANCO ---
def obtener_banco():
    db.conectar()
    db.cursor.execute("SELECT * FROM banco WHERE id = 1")
    fila = db.cursor.fetchone()
    db.cerrar()
    return dict(fila) if fila else {}