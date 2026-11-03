from flask import Flask, jsonify, render_template, url_for, redirect
from psycopg2.extras import RealDictCursor
from conexao import criar_conexao

uber2 = Flask(__name__)

@uber2.route('/login', methods=['GET'])
def pagina_login():
    return render_template()