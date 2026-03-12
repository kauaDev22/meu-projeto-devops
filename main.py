import os
import psycopg2
from fastapi import FastAPI
from dotenv import load_dotenv

# Carrega as variáveis do arquivo .env
load_dotenv()

app = FastAPI()

# Pega a URL do banco que está no .env
DATABASE_URL = os.getenv("DATABASE_URL")

# Função para conectar no banco
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
        
        # Busca as mensagens no Supabase
        cur.execute("SELECT id, texto, data_criacao FROM mensagens;")
        linhas = cur.fetchall()
        
        # Fecha a conexão
        cur.close()
        conn.close()
        
        # Formata o resultado para JSON
        resultado = [{"id": linha[0], "texto": linha[1], "data": linha[2]} for linha in linhas]
        return {"mensagens": resultado}
        
    except Exception as e:
        return {"erro": str(e)}