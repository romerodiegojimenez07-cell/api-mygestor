# MyGestor API 🧠

MyGestor API es un motor backend (sin interfaz gráfica) diseñado para la gestión operativa de pequeños negocios. Permite administrar inventario, registrar ventas y controlar los saldos de caja. 

Su principal valor diferencial es la integración de un **Agente de Inteligencia Artificial (Google Gemini)** que actúa como asesor de negocios: analiza los datos en tiempo real, alerta sobre stock crítico, detecta productos con márgenes negativos y sugiere estrategias de reinversión.

## 🛠️ Stack Tecnológico

*   **Python 3.10+**
*   **FastAPI** (Framework web para la API REST)
*   **SQLite3** (Base de datos relacional, usando SQL puro sin ORM)
*   **Pydantic** (Validación estricta de datos)
*   **google-genai** (SDK oficial de Google para la IA)
*   **Uvicorn** (Servidor ASGI)

## 📁 Estructura del Proyecto

```text
api-mygestor/
├── app/
│   ├── main.py          # Arranca FastAPI, define rutas y seguridad
│   ├── database.py      # Conexión a SQLite y creación de tablas
│   ├── models.py        # Esquemas Pydantic (Validación)
│   ├── crud.py          # Lógica SQL (Insertar, buscar, actualizar)
│   └── agente.py        # Lógica de IA (Prompts y conexión a Gemini)
├── .env.example         # Plantilla de variables de entorno
├── .gitignore           # Protege .env y la base de datos
├── requirements.txt     # Dependencias
└── README.md