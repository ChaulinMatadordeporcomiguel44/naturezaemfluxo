from flask import Flask, request, render_template_string, redirect
import csv
import os
from datetime import datetime

app = Flask(__name__)

# --- Pasta onde o CSV ficará ---
DATA_FOLDER = "datas"
CSV_FILE = os.path.join(DATA_FOLDER, "denuncias.csv")

# --- Criar a pasta 'datas' se não existir ---
os.makedirs(DATA_FOLDER, exist_ok=True)

# --- Criar o CSV com cabeçalho se não existir ---
if not os.path.exists(CSV_FILE):
    with open(CSV_FILE, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f, delimiter=";")
        writer.writerow([
            "tipo_problema",
            "titulo",
            "endereco",
            "bairro",
            "ponto_referencia",
            "descricao",
            "severidade",
            "data_ocorrencia",
            "anonimo",
            "data_envio"
        ])


@app.route("/salvar", methods=["POST"])
def salvar():
    dados = [
        request.form.get("tipo_problema", ""),
        request.form.get("titulo", ""),
        request.form.get("endereco", ""),
        request.form.get("bairro", ""),
        request.form.get("ponto_referencia", ""),
        request.form.get("descricao", ""),
        request.form.get("severidade", ""),
        request.form.get("data_ocorrencia", ""),
        "sim" if request.form.get("anonimo") else "nao",
        datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    ]

    # Grava em CSV dentro de datas/denuncias.csv
    with open(CSV_FILE, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f, delimiter=";")
        writer.writerow(dados)

    # Página de retorno
    return """
    <body style="font-family: Arial; background: #eef; padding: 40px;">
        <h2>Denúncia registrada com sucesso!</h2>
        <a href="/">Voltar ao formulário</a>
    </body>
    """


@app.route("/")
def index():
    # Mostra seu formulário original
    with open("formulario.html", "r", encoding="utf-8") as f:
        html = f.read()
    return render_template_string(html)


if __name__ == "__main__":
    app.run(debug=True)