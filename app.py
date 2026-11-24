from flask import Flask, render_template, request, abort
import sqlite3

def conectar():
    conexao = sqlite3.connect("loja.db")
    conexao.row_factory = sqlite3.Row
    return conexao

app = Flask(__name__)

@app.route("/")
def index():
    categoria = request.args.get("categoria")
    conexao = conectar()

    # categorias sem repetir
    categorias = conexao.execute("SELECT DISTINCT categoria FROM produtos").fetchall()

    # produtos filtrados ou todos
    if categoria:
        produtos = conexao.execute(
            "SELECT * FROM produtos WHERE categoria = ?", (categoria,)
        ).fetchall()
    else:
        produtos = conexao.execute("SELECT * FROM produtos").fetchall()

    conexao.close()

    return render_template(
        "index.html",
        produtos=produtos,
        categorias=categorias,
        categoria_ativa=categoria,
    )

@app.route("/produtos/<int:produto_id>")
def produto(produto_id):
    produto_encontrado = None

    for item in PRODUTOS:
        if item["id"] == produto_id:
            produto_encontrado = item

    if produto_encontrado is None:
        abort(404)

    return render_template("produto.html", produto=produto_encontrado)

@app.route("/produtores")
def produtores():
    return render_template("produtores.html")

@app.route("/perfil")
def perfil():
    return render_template("perfil.html")

@app.route("/carrinho")
def carrinho():
    return render_template("carrinho.html")


if __name__ == "__main__":
    app.run(debug=True)