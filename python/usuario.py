from flask_login import UserMixin

class Usuario(UserMixin):
    def __init__(self, id, nome, tipo):
        self.id = id
        self.nome = nome
        self.tipo = tipo

    def get_id(self):
        return f"{self.tipo}:{self.id}"