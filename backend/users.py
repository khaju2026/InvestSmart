import sqlite3
import os

# Caminho do banco de dados
DB_PATH = os.path.join(os.path.dirname(__file__), "investsmart.db")

def inicializar_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    # Tabela de usuários
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL
        )
    """)
    # Tabela de preferências
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS preferencias (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario_id INTEGER NOT NULL,
            ativo TEXT NOT NULL,
            alerta REAL,
            FOREIGN KEY(usuario_id) REFERENCES usuarios(id)
        )
    """)
    conn.commit()
    conn.close()

inicializar_db()

def cadastrar_usuario(nome, email):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("INSERT OR IGNORE INTO usuarios (nome, email) VALUES (?, ?)", (nome, email))
    conn.commit()
    conn.close()
    return f"Usuário {nome} cadastrado com sucesso."

def listar_usuarios():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT id, nome, email FROM usuarios")
    usuarios = cursor.fetchall()
    conn.close()
    return usuarios

def salvar_preferencia(email, ativo, alerta=None):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM usuarios WHERE email = ?", (email,))
    usuario = cursor.fetchone()
    if usuario:
        usuario_id = usuario[0]
        cursor.execute("INSERT INTO preferencias (usuario_id, ativo, alerta) VALUES (?, ?, ?)",
                       (usuario_id, ativo, alerta))
        conn.commit()
        conn.close()
        return f"Preferência salva: {ativo} com alerta {alerta if alerta else 'nenhum'}"
    else:
        conn.close()
        return "Usuário não encontrado."

def carregar_preferencias(email):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM usuarios WHERE email = ?", (email,))
    usuario = cursor.fetchone()
    if usuario:
        usuario_id = usuario[0]
        cursor.execute("SELECT ativo, alerta FROM preferencias WHERE usuario_id = ?", (usuario_id,))
        prefs = cursor.fetchall()
        conn.close()
        return prefs
    else:
        conn.close()
        return []
