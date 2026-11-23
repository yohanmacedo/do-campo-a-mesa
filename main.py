from flask import Flask, render_template

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def inicio():
    # Requisição GET: apenas exibe a página sem resultado
    if request.method == "GET":
        return render_template("form.html", resultado=None)
    
    return render_template("form.html", resultado=resultado)


if __name__ == "__main__":
    app.run(debug=True)