import sqlite3
import os
from datetime import datetime
from custom_logger import logger

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'monitor.db')

def get_connection(db_path=DB_PATH):
    return sqlite3.connect(db_path)

def init_db(conn=None):
    close_connection = False
    if conn is None:
        conn = get_connection()
        close_connection = True
    try:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS historico_analises (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                data_hora TEXT NOT NULL,
                usuario_solicitante TEXT NOT NULL,
                versao_modelo TEXT NOT NULL,
                paciente_nome TEXT NOT NULL,
                tendencia TEXT NOT NULL,
                justificativa TEXT NOT NULL
            )
        ''')
        conn.commit()
        logger.info("Tabela historico_analises pronta/inicializada no SQLite.")
    except Exception as e:
        logger.error(f"Erro ao inicializar banco de dados SQLite: {str(e)}")
    finally:
        if close_connection:
            conn.close()

def log_analysis_result(usuario, modelo, paciente, tendencia, justificativa, conn=None):
    close_connection = False
    if conn is None:
        conn = get_connection()
        close_connection = True
        
    try:
        cursor = conn.cursor()
        data_hora = datetime.now().strftime("%Y/%m/%d %H:%M:%S")
        cursor.execute('''
            INSERT INTO historico_analises 
            (data_hora, usuario_solicitante, versao_modelo, paciente_nome, tendencia, justificativa) 
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (data_hora, usuario, modelo, paciente, tendencia, justificativa))
        conn.commit()
        logger.info(f"Persistência SQL relizada para paciente {paciente} (Veredito: {tendencia}).")
    except Exception as e:
        logger.error(f"Erro persistindo análise no banco SQLite: {str(e)}")
    finally:
        if close_connection:
            conn.close()
