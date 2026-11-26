from flask import Flask, render_template, request, abort, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
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
    conexao = conectar()
    produto_encontrado = conexao.execute(
        "SELECT * FROM produtos WHERE id = ?", (produto_id,)
    ).fetchone()
    conexao.close()

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

@app.route("/cadastrar_produto", methods=["GET", "POST"])
def cadastro_produto():
    conexao = conectar()
    categorias = conexao.execute("SELECT DISTINCT categoria FROM produtos").fetchall()
    conexao.close()

    if request.method == "POST":
        conexao = conectar()
        conexao.execute(
            "INSERT INTO produtos (nome, produtor, preco, unidade, categoria) VALUES (?, ?, ?, ?, ?)",
        (
                request.form["nome"],
                "nao informado",
                float(request.form["preco"]),
                request.form["unidade"],
                request.form["categoria"],
        )
        )
        conexao.commit()
        conexao.close()
        return redirect(url_for('index'))
    return render_template("cadastro_produto.html", categorias=categorias)


@app.route("/cadastrar_usuario", methods=["GET", "POST"])
def cadastrar_usuario():
    if request.method == "POST":
        nome = request.form["nome"]
        email = request.form["email"]
        senha = request.form["senha"]
        tipo = request.form["tipo"]

        senha_hash = generate_password_hash(senha)

        if tipo not in ("agricultor", "consumidor"):
            abort(400)

        conexao = conectar()
        try:
            conexao.execute(
                "INSERT INTO usuarios (nome, email, senha_hash, tipo) VALUES (?, ?, ?, ?)",
                (nome, email, senha_hash, tipo)
            )
            conexao.commit()
        except sqlite3.IntegrityError:
            return "Email já cadastrado!"
        finally:
            conexao.close()

        return redirect(url_for('index'))

    return render_template("cadastrar_usuario.html")

if __name__ == "__main__":
    app.run(debug=True)