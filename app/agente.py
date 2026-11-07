import os
from google import genai
from google.genai import types
from dotenv import load_dotenv
from app.database import db

load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

def obtener_contexto_negocio() -> str:
    """Recopila datos clave de SQLite para la IA."""
    db.conectar()
    
    # 1. Productos (Analizar stock y rentabilidad)
    db.cursor.execute("SELECT nombre, stock, costo, precio_venta, (precio_venta - costo) as margen FROM productos")
    productos = [dict(p) for p in db.cursor.fetchall()]
    
    # 2. Ventas (Para saber qué se mueve)
    db.cursor.execute("""
        SELECT p.nombre, COUNT(m.id) as cantidad_vendida, SUM(m.monto) as total_recaudado
        FROM movimientos m 
        JOIN productos p ON m.producto_id = p.id 
        WHERE m.tipo = 'venta' 
        GROUP BY p.id
        ORDER BY cantidad_vendida DESC LIMIT 5
    """)
    ventas = [dict(v) for v in db.cursor.fetchall()]
    
    # 3. Banco
    db.cursor.execute("SELECT saldo_fuerte, saldo_tarjeta, saldo_ahorros FROM banco WHERE id = 1")
    banco = dict(db.cursor.fetchone()) if db.cursor.rowcount > 0 else {}
    
    db.cerrar()
    
    return f"""
    DATOS DEL NEGOCIO:
    - Inventario: {productos}
    - Top 5 Ventas: {ventas}
    - Saldos (Banco): {banco}
    """

def analizar_negocio(pregunta: str) -> str:
    contexto = obtener_contexto_negocio()
    
    # Instrucciones estrictas para Gemini
    prompt_sistema = f"""
    Eres el Asesor de Negocios experto de MyGestor. 
    Tu objetivo es analizar los datos y dar recomendaciones prácticas al dueño.
    
    REGLAS DE ANÁLISIS:
    1. ALERTA DE STOCK: Si un producto tiene menos de 5 unidades, recomienda reponerlo.
    2. ALERTA DE PÉRDIDA: Si el margen (precio_venta - costo) es 0 o negativo, avisa que se está perdiendo dinero.
    3. REINVERSIÓN: Si hay saldo en el banco, sugiere invertir en los productos del "Top 5 Ventas".
    4. Responde de forma breve, directa y profesional. Usa viñetas si es necesario.
    
    {contexto}
    
    PREGUNTA DEL DUEÑO: {pregunta}
    """
    
    try:
        response = client.models.generate_content(
            model='gemini-3.5-flash', # Usando el que te funcionó
            contents=pregunta,
            config=types.GenerateContentConfig(
                system_instruction=prompt_sistema,
                temperature=0.4, 
            )
        )
        return response.text
    except Exception as e:
        return f"Error al consultar la IA: {str(e)}"