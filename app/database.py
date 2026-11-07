import sqlite3
import os

class Database:
    def __init__(self, nombre="mygestor.db"):
        self.nombre = nombre
        self.conectar()

    def conectar(self):
        # check_same_thread=False es necesario para FastAPI
        self.conexion = sqlite3.connect(self.nombre, check_same_thread=False)
        # Permite acceder a los resultados como diccionarios
        self.conexion.row_factory = sqlite3.Row
        self.cursor = self.conexion.cursor()

    def cerrar(self):
        if self.conexion:
            self.conexion.close()

    def crear_tablas(self):
        # Tabla de Productos
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS productos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                categoria TEXT DEFAULT 'General',
                stock REAL NOT NULL DEFAULT 0,
                costo REAL NOT NULL,
                precio_venta REAL NOT NULL,
                creado TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Tabla de Empleados
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS empleados (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                rol TEXT NOT NULL, -- 'gestor', 'vendedor', 'admin'
                comision_porcentaje REAL DEFAULT 0,
                periodo_pago TEXT DEFAULT 'mensual', -- 'semanal', 'quincenal', 'mensual'
                activo INTEGER DEFAULT 1
            )
        """)

        # Tabla de Movimientos (Ventas, Gastos, Reinversiones)
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS movimientos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                tipo TEXT NOT NULL, -- 'venta', 'gasto', 'reinversion', 'pago_empleado'
                monto REAL NOT NULL,
                descripcion TEXT,
                producto_id INTEGER,
                empleado_id INTEGER,
                fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (producto_id) REFERENCES productos (id),
                FOREIGN KEY (empleado_id) REFERENCES empleados (id)
            )
        """)

        # Tabla de Banco (Caja)
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS banco (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                saldo_fuerte REAL DEFAULT 0,
                saldo_tarjeta REAL DEFAULT 0,
                saldo_ahorros REAL DEFAULT 0
            )
        """)
        
        # Insertar fila inicial en banco si no existe
        self.cursor.execute("SELECT COUNT(*) FROM banco")
        if self.cursor.fetchone()[0] == 0:
            self.cursor.execute("INSERT INTO banco (saldo_fuerte, saldo_tarjeta, saldo_ahorros) VALUES (0, 0, 0)")

        self.conexion.commit()

# Instancia global
db = Database()