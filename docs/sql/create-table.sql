-- Active: 1788283797601@@127.0.0.1@5432@uber2
CREATE TABLE usuarios (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    email VARCHAR(150) NOT NULL UNIQUE,
    telefone VARCHAR(20) NOT NULL,
    senha VARCHAR(255) NOT NULL,
    data_cadastro TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TYPE status_motorista AS ENUM (
    'Ativo',
    'Inativo'
);

CREATE TABLE motoristas (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    cpf VARCHAR(14) NOT NULL,
    telefone VARCHAR(20) NOT NULL,
    cnh VARCHAR(20) NOT NULL,
    status status_motorista DEFAULT 'Ativo'
);

CREATE TABLE veiculos (
    id SERIAL PRIMARY KEY,
    id_motorista INTEGER NOT NULL,
    modelo VARCHAR(50) NOT NULL,
    marca VARCHAR(50) NOT NULL,
    placa VARCHAR(10) NOT NULL,
    ano INTEGER NOT NULL,
    cor VARCHAR(30),

    CONSTRAINT fk_veiculo_motorista
        FOREIGN KEY (id_motorista)
        REFERENCES motoristas(id)
);

CREATE TYPE status_corrida AS ENUM (
    'Solicitada',
    'Aceita',
    'Em andamento',
    'Finalizada',
    'Cancelada'
);

CREATE TABLE corridas (
    id SERIAL PRIMARY KEY,
    id_usuario INTEGER NOT NULL,
    id_motorista INTEGER NOT NULL,
    origem VARCHAR(100) NOT NULL,
    destino VARCHAR(100) NOT NULL,
    data_hora TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    valor DECIMAL(10, 2) CHECK(valor >= 0),
    status status_corrida DEFAULT 'Solicitada',

    CONSTRAINT fk_corrida_usuario
        FOREIGN KEY (id_usuario)
        REFERENCES usuarios(id),

    CONSTRAINT fk_corrida_motorista
        FOREIGN KEY (id_motorista)
        REFERENCES motoristas(id),

    CONSTRAINT ck_origem_destino
        CHECK (origem <> destino)
);

CREATE TABLE avaliacoes (
    id SERIAL PRIMARY KEY,
    id_corrida INTEGER NOT NULL,
    nota INTEGER NOT NULL CHECK(nota BETWEEN 1 AND 5),
    comentario TEXT,
    data_avaliacao TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_avaliacao_corrida
        FOREIGN KEY (id_corrida)
        REFERENCES corridas(id)
);

CREATE TYPE form_de_pag AS ENUM (
    'Pix',
    'Dinheiro',
    'Cartão'
);

CREATE TYPE status_pag AS ENUM (
    'Pendente',
    'Pago',
    'Cancelado'
);

CREATE TABLE pagamentos (
    id SERIAL PRIMARY KEY,
    id_corrida INTEGER NOT NULL,
    forma_pagamento form_de_pag NOT NULL,
    valor DECIMAL(10, 2) CHECK(valor >= 0),
    status status_pag DEFAULT 'Pendente',
    data_pagamento TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_pagamento_corrida
        FOREIGN KEY (id_corrida)
        REFERENCES corridas(id)
);

CREATE TABLE historico_corridas (
    id SERIAL PRIMARY KEY,
    id_corrida INTEGER NOT NULL,
    status_anterior status_corrida,
    novo_status status_corrida NOT NULL,
    data_alteracao TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_historico_corrida
        FOREIGN KEY (id_corrida)
        REFERENCES corridas(id)
);

ALTER TABLE corridas
ALTER COLUMN id_motorista DROP NOT NULL;