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
        try:
            cursor.execute("ALTER TABLE historico_analises ADD COLUMN feedback_tipo TEXT")
            cursor.execute("ALTER TABLE historico_analises ADD COLUMN feedback_motivo TEXT")
            cursor.execute("ALTER TABLE historico_analises ADD COLUMN feedback_data TEXT")
        except:
            pass # Colunas de feedback já existem
            
        try:
            cursor.execute("ALTER TABLE historico_analises ADD COLUMN whatsapp_enviado INTEGER DEFAULT 0")
        except:
            pass

            
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
        inserted_id = cursor.lastrowid
        conn.commit()
        logger.info(f"Persistência SQL relizada para paciente {paciente} (Veredito: {tendencia}).")
        return inserted_id
    except Exception as e:
        logger.error(f"Erro persistindo análise no banco SQLite: {str(e)}")
        return None
    finally:
        if close_connection:
            conn.close()

def salvar_feedback(analise_id, tipo, motivo, conn=None):
    close_connection = False
    if conn is None:
        conn = get_connection()
        close_connection = True
        
    try:
        cursor = conn.cursor()
        
        cursor.execute("SELECT feedback_tipo FROM historico_analises WHERE id = ?", (analise_id,))
        row = cursor.fetchone()
        
        if row is None:
            return False
            
        if row[0] is not None:
            logger.warning(f"Tentativa de duplicar feedback para análise ID {analise_id} mitigada.")
            return False
            
        feedback_data = datetime.now().strftime("%Y/%m/%d %H:%M:%S")
        cursor.execute('''
            UPDATE historico_analises 
            SET feedback_tipo = ?, feedback_motivo = ?, feedback_data = ?
            WHERE id = ?
        ''', (tipo, motivo, feedback_data, analise_id))
        
        conn.commit()
        logger.info(f"Feedback recebido para análise ID {analise_id}: {tipo} - Motivo: {motivo}")
        return True
    except Exception as e:
        logger.error(f"Erro salvando feedback (RLHF): {str(e)}")
        return False
    finally:
        if close_connection:
            conn.close()

def get_melhores_exemplos(limit=3, conn=None):
    close_connection = False
    if conn is None:
        conn = get_connection()
        close_connection = True
    try:
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute('''
            SELECT paciente_nome, tendencia, justificativa 
            FROM historico_analises 
            WHERE feedback_tipo = 'LIKE'
            ORDER BY id DESC
            LIMIT ?
        ''', (limit,))
        return [dict(row) for row in cursor.fetchall()]
    except Exception as e:
        logger.error(f"Erro efetuando select de melhores exemplos SQLite: {str(e)}")
        return []
    finally:
        if close_connection:
            conn.close()

def count_analises_paciente(paciente_nome, conn=None):
    close_connection = False
    if conn is None:
        conn = get_connection()
        close_connection = True
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(id) FROM historico_analises WHERE paciente_nome = ?", (paciente_nome,))
        return cursor.fetchone()[0]
    except Exception as e:
        logger.error(f"Erro calculando total de análises SQLite: {str(e)}")
        return 0
    finally:
        if close_connection:
            conn.close()

def get_analises_paciente(paciente_nome, limit, offset, conn=None):
    close_connection = False
    if conn is None:
        conn = get_connection()
        close_connection = True
        
    try:
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute('''
            SELECT id, data_hora, usuario_solicitante, versao_modelo, tendencia, justificativa, feedback_tipo, feedback_motivo, feedback_data, whatsapp_enviado 
            FROM historico_analises 
            WHERE paciente_nome = ?
            ORDER BY id DESC
            LIMIT ? OFFSET ?
        ''', (paciente_nome, limit, offset))
        rows = cursor.fetchall()
        return [dict(row) for row in rows]
    except Exception as e:
        logger.error(f"Erro efetuando select de melhores exemplos SQLite: {str(e)}")
        return []
    finally:
        if close_connection:
            conn.close()

def get_ultimas_correcoes(limit=2, conn=None):
    close_connection = False
    if conn is None:
        conn = get_connection()
        close_connection = True
    try:
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute('''
            SELECT paciente_nome, tendencia, justificativa, feedback_motivo
            FROM historico_analises 
            WHERE feedback_tipo = 'DISLIKE' AND feedback_motivo IS NOT NULL AND feedback_motivo != ''
            ORDER BY id DESC
            LIMIT ?
        ''', (limit,))
        return [dict(row) for row in cursor.fetchall()]
    except Exception as e:
        logger.error(f"Erro buscando correções de RLHF SQLite: {str(e)}")
        return []
    finally:
        if close_connection:
            conn.close()

def confirmar_envio_whatsapp(analise_id, conn=None):
    close_connection = False
    if conn is None:
        conn = get_connection()
        close_connection = True
    try:
        cursor = conn.cursor()
        cursor.execute("UPDATE historico_analises SET whatsapp_enviado = 1 WHERE id = ?", (analise_id,))
        conn.commit()
    except Exception as e:
        logger.error(f"Erro confirmando envio de Whatsapp SQLite: {str(e)}")
    finally:
        if close_connection:
            conn.close()
