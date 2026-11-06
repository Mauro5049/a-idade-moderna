import os
import mysql.connector
from flask import Flask

app = Flask(__name__)


def conectar_banco():
    return mysql.connector.connect(
        host=os.environ["DB_HOST"],
        port=int(os.environ.get("DB_PORT", "3306")),
        database=os.environ["DB_NAME"],
        user=os.environ["DB_USER"],
        password=os.environ["DB_PASSWORD"]
    )


@app.route("/")
def home():
    return """
    <h1>Minha primeira aplicação Flask</h1>
    <p>Aplicação executando dentro de containers Docker!</p>
    <p>
        <a href="/sobre">Sobre</a> |
        <a href="/contato">Contato</a> |
        <a href="/alunos">Alunos</a>
    </p>
    """


@app.route("/sobre")
def sobre():
    return """
    <h1>Sobre a aplicação Python/Flask</h1>
    <p>Projeto da disciplina de Redes e Administração de Sistemas.</p>
    """


@app.route("/contato")
def contato():
    return """
    <h1>Contato com os alunos do projeto</h1>
    <p>Instituto Federal de São Paulo, Campus Campos do Jordão (IFSP-CJO).</p>
    """


@app.route("/alunos")
def alunos():
    conexao = conectar_banco()
    cursor = conexao.cursor(dictionary=True)

    try:
        cursor.execute("SELECT id, nome FROM alunos ORDER BY id")
        registros = cursor.fetchall()

        html = "<h1>Alunos cadastrados no MySQL</h1><ul>"

        for aluno in registros:
            html += f"<li>{aluno['id']} - {aluno['nome']}</li>"

        html += "</ul>"
        return html

    finally:
        cursor.close()
        conexao.close()

@app.route("/ottm")
def ottm():
	return "<p>drums please, fab?</p>"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
