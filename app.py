from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/produtores")
def produtores():
    return render_template("produtores.html")

@app.route("/categorias")
def categorias():
    return render_template("categorias.html")

@app.route("/perfil")
def perfil():
    return render_template("perfil.html")

@app.route("/carrinho")
def carrinho():
    return render_template("carrinho.html")

if __name__ == "__main__":
    app.run(debug=True)