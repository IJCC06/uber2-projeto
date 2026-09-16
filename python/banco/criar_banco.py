from banco.conexao import conectar

def criar_tabelas():

    conexao = conectar()
    cursor = conexao.cursor()

    # ==========================================
    # USUÁRIOS
    # ==========================================

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            telefone TEXT NOT NULL,
            senha TEXT NOT NULL,
            data_cadastro TIMESTAMP NOT NULL
                DEFAULT CURRENT_TIMESTAMP
        )
    """)


    # ==========================================
    # MOTORISTAS
    # ==========================================

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS motoristas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            cpf TEXT NOT NULL UNIQUE,
            telefone TEXT NOT NULL,
            cnh TEXT NOT NULL UNIQUE,

            status TEXT NOT NULL DEFAULT 'Ativo'
                CHECK (status IN ('Ativo', 'Inativo'))
        )
    """)


    # ==========================================
    # VEÍCULOS
    # ==========================================

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS veiculos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            id_motorista INTEGER NOT NULL,
            modelo TEXT NOT NULL,
            marca TEXT NOT NULL,
            placa TEXT NOT NULL UNIQUE,
            ano INTEGER NOT NULL,
            cor TEXT,

            FOREIGN KEY (id_motorista)
                REFERENCES motoristas(id)
        )
    """)


    # ==========================================
    # CORRIDAS
    # ==========================================

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS corridas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,

            id_usuario INTEGER NOT NULL,
            id_motorista INTEGER,

            origem TEXT NOT NULL,
            destino TEXT NOT NULL,

            data_hora TIMESTAMP NOT NULL
                DEFAULT CURRENT_TIMESTAMP,

            valor DECIMAL(10, 2)
                CHECK (valor >= 0),

            status TEXT NOT NULL
                DEFAULT 'Solicitada'

                CHECK (
                    status IN (
                        'Solicitada',
                        'Aceita',
                        'Em andamento',
                        'Finalizada',
                        'Cancelada'
                    )
                ),

            CHECK (origem <> destino),

            FOREIGN KEY (id_usuario)
                REFERENCES usuarios(id),

            FOREIGN KEY (id_motorista)
                REFERENCES motoristas(id)
        )
    """)


    # ==========================================
    # PAGAMENTOS
    # ==========================================

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS pagamentos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,

            id_corrida INTEGER NOT NULL,

            forma_pagamento TEXT NOT NULL

                CHECK (
                    forma_pagamento IN (
                        'Pix',
                        'Dinheiro',
                        'Cartão'
                    )
                ),

            valor DECIMAL(10, 2) NOT NULL
                CHECK (valor >= 0),

            status TEXT NOT NULL
                DEFAULT 'Pendente'

                CHECK (
                    status IN (
                        'Pendente',
                        'Pago',
                        'Cancelado'
                    )
                ),

            data_pagamento TIMESTAMP NOT NULL
                DEFAULT CURRENT_TIMESTAMP,

            FOREIGN KEY (id_corrida)
                REFERENCES corridas(id)
        )
    """)


    # ==========================================
    # AVALIAÇÕES
    # ==========================================

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS avaliacoes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,

            id_corrida INTEGER NOT NULL,

            nota INTEGER NOT NULL
                CHECK (nota BETWEEN 1 AND 5),

            comentario TEXT,

            data_avaliacao TIMESTAMP NOT NULL
                DEFAULT CURRENT_TIMESTAMP,

            FOREIGN KEY (id_corrida)
                REFERENCES corridas(id)
        )
    """)


    # ==========================================
    # HISTÓRICO DAS CORRIDAS
    # ==========================================

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS historico_corridas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,

            id_corrida INTEGER NOT NULL,

            status_anterior TEXT NOT NULL,
            novo_status TEXT NOT NULL,

            data_alteracao TIMESTAMP NOT NULL
                DEFAULT CURRENT_TIMESTAMP,

            FOREIGN KEY (id_corrida)
                REFERENCES corridas(id)
        )
    """)


    conexao.commit()
    conexao.close()

    print("Banco de dados e tabelas criados com sucesso!")


if __name__ == "__main__":
    criar_tabelas()