-- Exibir todos os Dados
SELECT * FROM usuarios;
SELECT * FROM enderecos;
SELECT * FROM motoristas;
SELECT * FROM veiculos;
SELECT * FROM corridas;
SELECT * FROM avaliacoes;
SELECT * FROM pagamentos;


-- CONSULTAS RELEVANTES:

-- 1. Quais foram as 5 corridas mais caras?
SELECT
    c.id AS id_corrida,
    u.nome AS usuario,
    m.nome AS motorista,
    c.valor,
    c.status
FROM corridas c
JOIN usuarios u ON c.id_usuario = u.id
JOIN motoristas m ON c.id_motorista = m.id
ORDER BY c.valor DESC
LIMIT 5;

-- 2. Qual motorista realizou mais corridas?
SELECT
    m.id,
    m.nome,
    COUNT(c.id) AS quantidade_corridas
FROM motoristas m
JOIN corridas c
    ON c.id_motorista = m.id
GROUP BY m.id, m.nome
ORDER BY quantidade_corridas DESC;

-- 3. Qual forma de pagamento foi mais utilizada?
SELECT
    forma_pagamento,
    COUNT(*) AS quantidade_utilizada
FROM pagamentos
GROUP BY forma_pagamento
ORDER BY quantidade_utilizada DESC;

-- 4. Quais motoristas estão disponíveis?
SELECT
    id,
    nome,
    status
FROM motoristas
WHERE status = 'Ativo'
ORDER BY id ASC;

-- 5. Qual foi o histórico de status de determinada corrida?
SELECT
    h.id_corrida,
    h.status_anterior,
    h.novo_status,
    h.data_alteracao
FROM historico_corridas h
WHERE h.id_corrida = 1
ORDER BY h.data_alteracao;

-- 6. Quanto foi arrecadado em determinado período?
SELECT
    sum(valor) AS total_arrecadado
FROM pagamentos
WHERE status = 'Pago' AND data_pagamento BETWEEN '2026-01-01' AND '2026-12-31';

-- 7. Qual foi a média de avaliação de cada motorista?
SELECT
    m.id,
    m.nome,
    ROUND(AVG(a.nota), 2) AS media_avaliacao
FROM motoristas m
JOIN corridas c
    ON c.id_motorista = m.id
JOIN avaliacoes a
    ON a.id_corrida = c.id
GROUP BY m.id, m.nome
ORDER BY media_avaliacao DESC;

-- 8. Média Geral dos Motoristas
SELECT
    ROUND(AVG(nota), 2) AS media_geral_motoristas
FROM avaliacoes;