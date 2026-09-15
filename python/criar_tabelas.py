from conexao import conectar

def criar_tabelas():
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            telefone TEXT NOT NULL,
            senha TEXT NOT NULL,
            data_cadastro TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
        )
    """)

    cursor.execute("""
            CREATE TABLE IF NOT EXISTS enderecos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                rua TEXT NOT NULL,
                numero TEXT NOT NULL,
                bairro TEXT NOT NULL,
                cidade TEXT NOT NULL,
                estado TEXT NOT NULL,
                cep TEXT NOT NULL
            )
    """)

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

    cursor.execute("""
            CREATE TABLE IF NOT EXISTS corridas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                id_usuario INTEGER NOT NULL,
                id_motorista INTEGER,
                id_origem INTEGER NOT NULL,
                id_destino INTEGER NOT NULL,
                data_hora TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                valor REAL NOT NULL CHECK (valor >= 0),

                status TEXT NOT NULL DEFAULT 'Solicitada'
                    CHECK (
                        status IN (
                            'Solicitada',
                            'Aceita',
                            'Em andamento',
                            'Finalizada',
                            'Cancelada'
                        )
                    ),

                FOREIGN KEY (id_usuario)
                    REFERENCES usuarios(id),

                FOREIGN KEY (id_motorista)
                    REFERENCES motoristas(id),

                FOREIGN KEY (id_origem)
                    REFERENCES enderecos(id),

                FOREIGN KEY (id_destino)
                    REFERENCES enderecos(id),

                CHECK (id_origem <> id_destino)
            )
    """)

    cursor.execute("""
            CREATE TABLE IF NOT EXISTS pagamentos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                id_corrida INTEGER NOT NULL UNIQUE,

                forma_pagamento TEXT NOT NULL
                    CHECK (
                        forma_pagamento IN (
                            'Pix',
                            'Dinheiro',
                            'Cartão'
                        )
                    ),

                valor REAL NOT NULL CHECK (valor >= 0),

                status TEXT NOT NULL DEFAULT 'Pendente'
                    CHECK (
                        status IN (
                            'Pendente',
                            'Pago',
                            'Cancelado'
                        )
                    ),

                data_pagamento TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,

                FOREIGN KEY (id_corrida)
                    REFERENCES corridas(id)
            )
    """)

    cursor.execute("""
            CREATE TABLE IF NOT EXISTS avaliacoes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                id_corrida INTEGER NOT NULL UNIQUE,
                nota INTEGER NOT NULL CHECK (nota BETWEEN 1 AND 5),
                comentario TEXT,
                data_avaliacao TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,

                FOREIGN KEY (id_corrida)
                    REFERENCES corridas(id)
            )
    """)

    cursor.execute("""
            CREATE TABLE IF NOT EXISTS historico_corridas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                id_corrida INTEGER NOT NULL,

                status_anterior TEXT
                    CHECK (
                        status_anterior IS NULL OR
                        status_anterior IN (
                            'Solicitada',
                            'Aceita',
                            'Em andamento',
                            'Finalizada',
                            'Cancelada'
                        )
                    ),

                novo_status TEXT NOT NULL
                    CHECK (
                        novo_status IN (
                            'Solicitada',
                            'Aceita',
                            'Em andamento',
                            'Finalizada',
                            'Cancelada'
                        )
                    ),

                data_alteracao TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,

                FOREIGN KEY (id_corrida)
                    REFERENCES corridas(id),

                CHECK (
                    status_anterior IS NULL OR
                    status_anterior <> novo_status
                )
            )
        """)

    conexao.commit()
    conexao.close()

    print("Tabelas criadas com sucesso!")


criar_tabelas()