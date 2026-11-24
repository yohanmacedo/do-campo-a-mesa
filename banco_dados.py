import sqlite3
from app import PRODUTOS

conexao = sqlite3.connect("loja.db")
cursor = conexao.cursor()

cursor.execute("""
    CREATE TABLE IF NOT EXISTS produtos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        produtor TEXT NOT NULL,
        preco REAL NOT NULL,
        unidade TEXT NOT NULL,
        categoria TEXT NOT NULL
    )
""")
for produto in PRODUTOS:
    cursor.execute(
    "INSERT INTO produtos (nome, produtor, preco, unidade, categoria) VALUES (?, ?, ?, ?, ?)",
    (produto["nome"], produto["produtor"], produto["preco"], produto["unidade"], produto["categoria"]),
    )

conexao.commit()
conexao.close()