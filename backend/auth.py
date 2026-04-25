import sqlite3
import os
import hashlib

DB_PATH = os.path.join(os.path.dirname(__file__), "investsmart.db")

def inicializar_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            senha TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

inicializar_db()

def hash_senha(senha):
    return hashlib.sha256(senha.encode("utf-8")).hexdigest()

def cadastrar_usuario(nome, email, senha):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    senha_hash = hash_senha(senha)
    cursor.execute("INSERT OR IGNORE INTO usuarios (nome, email, senha) VALUES (?, ?, ?)", (nome, email, senha_hash))
    conn.commit()
    conn.close()
    return f"Usuário {nome} cadastrado com sucesso."

def autenticar_usuario(email, senha):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    senha_hash = hash_senha(senha)
    cursor.execute("SELECT id, nome FROM usuarios WHERE email = ? AND senha = ?", (email, senha_hash))
    usuario = cursor.fetchone()
    conn.close()
    if usuario:
        return True, usuario[1]
    return False, None
