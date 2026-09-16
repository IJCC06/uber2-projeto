BEGIN;

-- =========================================================
-- LIMPAR DADOS EXISTENTES
-- =========================================================

TRUNCATE TABLE
    historico_corridas,
    avaliacoes,
    pagamentos,
    corridas,
    veiculos,
    motoristas,
    usuarios
RESTART IDENTITY CASCADE;


-- =========================================================
-- USUÁRIOS
-- 30 registros
-- =========================================================

INSERT INTO usuarios
    (nome, email, telefone, senha, data_cadastro)
VALUES
    ('João Silva', 'joao@email.com', '(19) 99901-0001', '123456', '2026-01-05 08:10:00'),
    ('Maria Oliveira', 'maria@email.com', '(19) 99901-0002', '123456', '2026-01-06 09:20:00'),
    ('Carlos Souza', 'carlos@email.com', '(19) 99901-0003', '123456', '2026-01-07 10:30:00'),
    ('Ana Santos', 'ana@email.com', '(19) 99901-0004', '123456', '2026-01-08 11:40:00'),
    ('Pedro Costa', 'pedro@email.com', '(19) 99901-0005', '123456', '2026-01-09 12:50:00'),
    ('Juliana Almeida', 'juliana@email.com', '(19) 99901-0006', '123456', '2026-01-10 13:00:00'),
    ('Lucas Pereira', 'lucas@email.com', '(19) 99901-0007', '123456', '2026-01-11 14:10:00'),
    ('Beatriz Lima', 'beatriz@email.com', '(19) 99901-0008', '123456', '2026-01-12 15:20:00'),
    ('Rafael Gomes', 'rafael@email.com', '(19) 99901-0009', '123456', '2026-01-13 16:30:00'),
    ('Camila Martins', 'camila@email.com', '(19) 99901-0010', '123456', '2026-01-14 17:40:00'),

    ('Felipe Rodrigues', 'felipe@email.com', '(19) 99901-0011', '123456', '2026-01-15 08:15:00'),
    ('Larissa Ferreira', 'larissa@email.com', '(19) 99901-0012', '123456', '2026-01-16 09:25:00'),
    ('Gustavo Barbosa', 'gustavo@email.com', '(19) 99901-0013', '123456', '2026-01-17 10:35:00'),
    ('Amanda Ribeiro', 'amanda@email.com', '(19) 99901-0014', '123456', '2026-01-18 11:45:00'),
    ('Bruno Carvalho', 'bruno@email.com', '(19) 99901-0015', '123456', '2026-01-19 12:55:00'),
    ('Fernanda Rocha', 'fernanda@email.com', '(19) 99901-0016', '123456', '2026-01-20 13:05:00'),
    ('Diego Martins', 'diego@email.com', '(19) 99901-0017', '123456', '2026-01-21 14:15:00'),
    ('Patricia Dias', 'patricia@email.com', '(19) 99901-0018', '123456', '2026-01-22 15:25:00'),
    ('Thiago Mendes', 'thiago@email.com', '(19) 99901-0019', '123456', '2026-01-23 16:35:00'),
    ('Isabela Teixeira', 'isabela@email.com', '(19) 99901-0020', '123456', '2026-01-24 17:45:00'),

    ('Renato Moreira', 'renato@email.com', '(19) 99901-0021', '123456', '2026-01-25 08:20:00'),
    ('Mariana Nunes', 'mariana@email.com', '(19) 99901-0022', '123456', '2026-01-26 09:30:00'),
    ('Eduardo Castro', 'eduardo@email.com', '(19) 99901-0023', '123456', '2026-01-27 10:40:00'),
    ('Bianca Cardoso', 'bianca@email.com', '(19) 99901-0024', '123456', '2026-01-28 11:50:00'),
    ('André Vieira', 'andre@email.com', '(19) 99901-0025', '123456', '2026-01-29 12:00:00'),
    ('Sofia Monteiro', 'sofia@email.com', '(19) 99901-0026', '123456', '2026-01-30 13:10:00'),
    ('Henrique Ramos', 'henrique@email.com', '(19) 99901-0027', '123456', '2026-02-01 14:20:00'),
    ('Clara Farias', 'clara@email.com', '(19) 99901-0028', '123456', '2026-02-02 15:30:00'),
    ('Marcelo Duarte', 'marcelo@email.com', '(19) 99901-0029', '123456', '2026-02-03 16:40:00'),
    ('Laura Freitas', 'laura@email.com', '(19) 99901-0030', '123456', '2026-02-04 17:50:00');


-- =========================================================
-- MOTORISTAS
-- 20 registros
-- =========================================================

INSERT INTO motoristas
    (nome, cpf, telefone, cnh, status)
VALUES
    ('Carlos Motorista', '100.000.001-01', '(19) 98801-0001', '10000000001', 'Ativo'),
    ('Roberto Lima', '100.000.002-02', '(19) 98801-0002', '10000000002', 'Ativo'),
    ('Marcos Souza', '100.000.003-03', '(19) 98801-0003', '10000000003', 'Ativo'),
    ('Eduardo Santos', '100.000.004-04', '(19) 98801-0004', '10000000004', 'Ativo'),
    ('Fernando Costa', '100.000.005-05', '(19) 98801-0005', '10000000005', 'Ativo'),
    ('Ricardo Almeida', '100.000.006-06', '(19) 98801-0006', '10000000006', 'Ativo'),
    ('Anderson Pereira', '100.000.007-07', '(19) 98801-0007', '10000000007', 'Ativo'),
    ('Daniel Gomes', '100.000.008-08', '(19) 98801-0008', '10000000008', 'Ativo'),
    ('Marcelo Martins', '100.000.009-09', '(19) 98801-0009', '10000000009', 'Ativo'),
    ('Alex Rodrigues', '100.000.010-10', '(19) 98801-0010', '10000000010', 'Ativo'),

    ('Paulo Ferreira', '100.000.011-11', '(19) 98801-0011', '10000000011', 'Ativo'),
    ('Rogério Barbosa', '100.000.012-12', '(19) 98801-0012', '10000000012', 'Ativo'),
    ('Leandro Ribeiro', '100.000.013-13', '(19) 98801-0013', '10000000013', 'Ativo'),
    ('Fábio Carvalho', '100.000.014-14', '(19) 98801-0014', '10000000014', 'Ativo'),
    ('Guilherme Rocha', '100.000.015-15', '(19) 98801-0015', '10000000015', 'Ativo'),
    ('Vinícius Dias', '100.000.016-16', '(19) 98801-0016', '10000000016', 'Inativo'),
    ('Wagner Mendes', '100.000.017-17', '(19) 98801-0017', '10000000017', 'Inativo'),
    ('Samuel Teixeira', '100.000.018-18', '(19) 98801-0018', '10000000018', 'Ativo'),
    ('Igor Moreira', '100.000.019-19', '(19) 98801-0019', '10000000019', 'Ativo'),
    ('Diego Nunes', '100.000.020-20', '(19) 98801-0020', '10000000020', 'Ativo');


-- =========================================================
-- VEÍCULOS
-- =========================================================

INSERT INTO veiculos
    (id_motorista, modelo, marca, placa, ano, cor)
VALUES
    (1, 'Onix', 'Chevrolet', 'ABC-1001', 2022, 'Prata'),
    (2, 'HB20', 'Hyundai', 'ABC-1002', 2023, 'Branco'),
    (3, 'Argo', 'Fiat', 'ABC-1003', 2021, 'Preto'),
    (4, 'Mobi', 'Fiat', 'ABC-1004', 2022, 'Vermelho'),
    (5, 'Cronos', 'Fiat', 'ABC-1005', 2023, 'Cinza'),
    (6, 'Gol', 'Volkswagen', 'ABC-1006', 2020, 'Branco'),
    (7, 'Polo', 'Volkswagen', 'ABC-1007', 2022, 'Prata'),
    (8, 'Virtus', 'Volkswagen', 'ABC-1008', 2023, 'Preto'),
    (9, 'Ka', 'Ford', 'ABC-1009', 2020, 'Azul'),
    (10, 'Fiesta', 'Ford', 'ABC-1010', 2019, 'Branco'),
    (11, 'City', 'Honda', 'ABC-1011', 2022, 'Cinza'),
    (12, 'Civic', 'Honda', 'ABC-1012', 2021, 'Preto'),
    (13, 'Yaris', 'Toyota', 'ABC-1013', 2023, 'Branco'),
    (14, 'Corolla', 'Toyota', 'ABC-1014', 2022, 'Prata'),
    (15, 'Kwid', 'Renault', 'ABC-1015', 2023, 'Vermelho'),
    (16, 'Sandero', 'Renault', 'ABC-1016', 2020, 'Branco'),
    (17, 'Logan', 'Renault', 'ABC-1017', 2021, 'Cinza'),
    (18, 'Tracker', 'Chevrolet', 'ABC-1018', 2023, 'Preto'),
    (19, 'T-Cross', 'Volkswagen', 'ABC-1019', 2022, 'Azul'),
    (20, 'Creta', 'Hyundai', 'ABC-1020', 2023, 'Prata');


-- =========================================================
-- CORRIDAS
-- 100 registros
-- =========================================================

INSERT INTO corridas
    (id_usuario, id_motorista, origem, destino, data_hora, valor, status)
SELECT
    ((n - 1) % 30) + 1,
    ((n - 1) % 15) + 1,

    CASE ((n - 1) % 10)
        WHEN 0 THEN 'Rua Central, 100'
        WHEN 1 THEN 'Avenida Brasil, 200'
        WHEN 2 THEN 'Rua das Flores, 300'
        WHEN 3 THEN 'Avenida Paulista, 400'
        WHEN 4 THEN 'Rua São Paulo, 500'
        WHEN 5 THEN 'Avenida Independência, 600'
        WHEN 6 THEN 'Rua XV de Novembro, 700'
        WHEN 7 THEN 'Avenida das Nações, 800'
        WHEN 8 THEN 'Rua do Comércio, 900'
        ELSE 'Rua das Palmeiras, 1000'
    END,

    CASE ((n - 1) % 10)
        WHEN 0 THEN 'Avenida Brasil, 200'
        WHEN 1 THEN 'Rua das Flores, 300'
        WHEN 2 THEN 'Avenida Paulista, 400'
        WHEN 3 THEN 'Rua São Paulo, 500'
        WHEN 4 THEN 'Avenida Independência, 600'
        WHEN 5 THEN 'Rua XV de Novembro, 700'
        WHEN 6 THEN 'Avenida das Nações, 800'
        WHEN 7 THEN 'Rua do Comércio, 900'
        WHEN 8 THEN 'Rua das Palmeiras, 1000'
        ELSE 'Rua Central, 100'
    END,

    TIMESTAMP '2026-01-01 08:00:00'
        + ((n - 1) * INTERVAL '1 day'),

    (15 + ((n * 7) % 86))::DECIMAL(10,2),

    CASE
        WHEN n <= 70 THEN 'Finalizada'::status_corrida
        WHEN n <= 80 THEN 'Em andamento'::status_corrida
        WHEN n <= 90 THEN 'Aceita'::status_corrida
        WHEN n <= 95 THEN 'Solicitada'::status_corrida
        ELSE 'Cancelada'::status_corrida
    END

FROM generate_series(1, 100) AS n;


-- =========================================================
-- PAGAMENTOS
-- 70 pagamentos para as 70 corridas finalizadas
-- =========================================================

INSERT INTO pagamentos
    (id_corrida, forma_pagamento, valor, status, data_pagamento)
SELECT
    id,

    CASE (id % 3)
        WHEN 0 THEN 'Pix'::form_de_pag
        WHEN 1 THEN 'Cartão'::form_de_pag
        ELSE 'Dinheiro'::form_de_pag
    END,

    valor,

    'Pago'::status_pag,

    data_hora + INTERVAL '30 minutes'

FROM corridas
WHERE status = 'Finalizada';


-- =========================================================
-- AVALIAÇÕES
-- 70 avaliações
-- =========================================================

INSERT INTO avaliacoes
    (id_corrida, nota, comentario, data_avaliacao)
SELECT
    id,

    CASE (id % 5)
        WHEN 0 THEN 5
        WHEN 1 THEN 4
        WHEN 2 THEN 3
        WHEN 3 THEN 5
        ELSE 4
    END,

    CASE (id % 5)
        WHEN 0 THEN 'Excelente corrida.'
        WHEN 1 THEN 'Boa experiência.'
        WHEN 2 THEN 'Corrida satisfatória.'
        WHEN 3 THEN 'Motorista muito bom.'
        ELSE 'Tudo ocorreu bem.'
    END,

    data_hora + INTERVAL '1 hour'

FROM corridas
WHERE status = 'Finalizada';


-- =========================================================
-- HISTÓRICO - CORRIDAS FINALIZADAS
-- =========================================================

INSERT INTO historico_corridas
    (id_corrida, status_anterior, novo_status, data_alteracao)
SELECT
    id,
    'Solicitada'::status_corrida,
    'Aceita'::status_corrida,
    data_hora
FROM corridas
WHERE status = 'Finalizada';


INSERT INTO historico_corridas
    (id_corrida, status_anterior, novo_status, data_alteracao)
SELECT
    id,
    'Aceita'::status_corrida,
    'Em andamento'::status_corrida,
    data_hora + INTERVAL '5 minutes'
FROM corridas
WHERE status = 'Finalizada';


INSERT INTO historico_corridas
    (id_corrida, status_anterior, novo_status, data_alteracao)
SELECT
    id,
    'Em andamento'::status_corrida,
    'Finalizada'::status_corrida,
    data_hora + INTERVAL '20 minutes'
FROM corridas
WHERE status = 'Finalizada';


-- =========================================================
-- HISTÓRICO - CORRIDAS EM ANDAMENTO
-- =========================================================

INSERT INTO historico_corridas
    (id_corrida, status_anterior, novo_status, data_alteracao)
SELECT
    id,
    'Solicitada'::status_corrida,
    'Aceita'::status_corrida,
    data_hora
FROM corridas
WHERE status = 'Em andamento';


INSERT INTO historico_corridas
    (id_corrida, status_anterior, novo_status, data_alteracao)
SELECT
    id,
    'Aceita'::status_corrida,
    'Em andamento'::status_corrida,
    data_hora + INTERVAL '5 minutes'
FROM corridas
WHERE status = 'Em andamento';


-- =========================================================
-- HISTÓRICO - CORRIDAS ACEITAS
-- =========================================================

INSERT INTO historico_corridas
    (id_corrida, status_anterior, novo_status, data_alteracao)
SELECT
    id,
    'Solicitada'::status_corrida,
    'Aceita'::status_corrida,
    data_hora
FROM corridas
WHERE status = 'Aceita';


-- =========================================================
-- HISTÓRICO - CORRIDAS CANCELADAS
-- =========================================================

INSERT INTO historico_corridas
    (id_corrida, status_anterior, novo_status, data_alteracao)
SELECT
    id,
    'Solicitada'::status_corrida,
    'Cancelada'::status_corrida,
    data_hora
FROM corridas
WHERE status = 'Cancelada';


-- =========================================================
-- FINALIZAR
-- =========================================================

COMMIT;


-- =========================================================
-- CONFERÊNCIA DOS DADOS
-- =========================================================

SELECT 'usuarios' AS tabela, COUNT(*) AS quantidade
FROM usuarios

UNION ALL

SELECT 'motoristas', COUNT(*)
FROM motoristas

UNION ALL

SELECT 'veiculos', COUNT(*)
FROM veiculos

UNION ALL

SELECT 'corridas', COUNT(*)
FROM corridas

UNION ALL

SELECT 'pagamentos', COUNT(*)
FROM pagamentos

UNION ALL

SELECT 'avaliacoes', COUNT(*)
FROM avaliacoes

UNION ALL

SELECT 'historico_corridas', COUNT(*)
FROM historico_corridas;