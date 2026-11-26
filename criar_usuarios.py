import sqlite3


conexao = sqlite3.connect("loja.db")
cursor = conexao.cursor()

cursor.execute("""
    CREATE TABLE IF NOT EXISTS usuarios (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        email TEXT NOT NULL UNIQUE,
        senha_hash TEXT NOT NULL,
        tipo TEXT NOT NULL
    )
""")