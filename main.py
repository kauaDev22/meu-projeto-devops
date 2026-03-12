import os
import psycopg2
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

# --- NOVO: Configuração do CORS ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permite que qualquer frontend acesse (na Vercel)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# ----------------------------------

DATABASE_URL = os.getenv("DATABASE_URL")

def get_db_connection():
    return psycopg2.connect(DATABASE_URL)

@app.get("/")
def home():
    return {"status": "Backend na nuvem operante! 🚀"}

@app.get("/mensagens")
def listar_mensagens():
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT id, texto, data_criacao FROM mensagens;")
        linhas = cur.fetchall()
        cur.close()
        conn.close()
        return {"mensagens": [{"id": l[0], "texto": l[1], "data": l[2]} for l in linhas]}
    except Exception as e:
        return {"erro": str(e)}