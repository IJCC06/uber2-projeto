from flask import Flask, jsonify, render_template, url_for, redirect
from psycopg2.extras import RealDictCursor
from conexao import criar_conexao

uber2 = Flask(__name__)

@uber2.route('/teste/db', methods=['GET'])
def testar_conexao():
    conn = criar_conexao()
    print('Testando conexão: ', conn)
    conn.close()
    return jsonify({"message": "Banco conectado com sucesso!"}), 200


@uber2.route('/', methods=['GET'])
def login():
    return render_template('login.html')

@uber2.route('/login/admin', methods=['GET'])
def login_adm():
    return render_template('login_admin.html')


if __name__ == "__main__":
    uber2.run(debug=True)