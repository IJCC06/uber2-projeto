-- População de Exemplo:
INSERT INTO usuarios (nome, email, telefone, senha)
VALUES
('João Silva', 'joao.silva@email.com', '11987654321', 'senha123'),
('Maria Santos', 'maria.santos@email.com', '11987654322', 'senha456'),
('Carlos Oliveira', 'carlos.oliveira@email.com', '11987654323', 'senha789'),
('Ana Souza', 'ana.souza@email.com', '11987654324', 'senha321'),
('Pedro Costa', 'pedro.costa@email.com', '11987654325', 'senha654'),
('Lucas Almeida', 'lucas.almeida@email.com', '11987654326', 'senha987'),
('Juliana Lima', 'juliana.lima@email.com', '11987654327', 'senha147'),
('Rafael Pereira', 'rafael.pereira@email.com', '11987654328', 'senha258'),
('Beatriz Rocha', 'beatriz.rocha@email.com', '11987654329', 'senha369'),
('Gabriel Martins', 'gabriel.martins@email.com', '11987654330', 'senha741'),
('Fernanda Alves', 'fernanda.alves@email.com', '11987654331', 'senha852'),
('Matheus Ribeiro', 'matheus.ribeiro@email.com', '11987654332', 'senha963'),
('Larissa Gomes', 'larissa.gomes@email.com', '11987654333', 'senha159'),
('Bruno Carvalho', 'bruno.carvalho@email.com', '11987654334', 'senha753'),
('Camila Barbosa', 'camila.barbosa@email.com', '11987654335', 'senha951'),
('Gustavo Ferreira', 'gustavo.ferreira@email.com', '11987654336', 'senha357'),
('Amanda Mendes', 'amanda.mendes@email.com', '11987654337', 'senha4567'),
('Thiago Nunes', 'thiago.nunes@email.com', '11987654338', 'senha6789'),
('Isabela Castro', 'isabela.castro@email.com', '11987654339', 'senha2345'),
('Diego Moreira', 'diego.moreira@email.com', '11987654340', 'senha8901');

INSERT INTO enderecos
(rua, numero, bairro, cidade, estado, cep)
VALUES
('Rua das Flores', '100', 'Centro', 'São Paulo', 'SP', '01001-000'),
('Avenida Paulista', '1500', 'Bela Vista', 'São Paulo', 'SP', '01310-100'),
('Rua Augusta', '850', 'Consolação', 'São Paulo', 'SP', '01305-000'),
('Avenida Ipiranga', '700', 'República', 'São Paulo', 'SP', '01046-010'),
('Rua Oscar Freire', '450', 'Pinheiros', 'São Paulo', 'SP', '01426-001'),
('Avenida Brasil', '1200', 'Jardim América', 'São Paulo', 'SP', '01430-000'),
('Rua Vergueiro', '900', 'Liberdade', 'São Paulo', 'SP', '01504-001'),
('Rua Haddock Lobo', '600', 'Cerqueira César', 'São Paulo', 'SP', '01414-001'),
('Avenida Faria Lima', '2000', 'Itaim Bibi', 'São Paulo', 'SP', '01451-000'),
('Rua Consolação', '1300', 'Consolação', 'São Paulo', 'SP', '01302-001'),
('Rua XV de Novembro', '300', 'Centro', 'Campinas', 'SP', '13015-000'),
('Avenida Anchieta', '500', 'Centro', 'Campinas', 'SP', '13015-904'),
('Rua Barão Geraldo', '750', 'Barão Geraldo', 'Campinas', 'SP', '13084-000'),
('Avenida Norte-Sul', '1100', 'Cambui', 'Campinas', 'SP', '13025-320'),
('Rua Coronel Quirino', '450', 'Cambui', 'Campinas', 'SP', '13025-001'),
('Rua Moraes Sales', '800', 'Centro', 'Campinas', 'SP', '13010-001'),
('Avenida Aquidabã', '1000', 'Vila Itapura', 'Campinas', 'SP', '13023-000'),
('Rua Dr. Quirino', '250', 'Centro', 'Campinas', 'SP', '13015-080'),
('Rua General Osório', '600', 'Centro', 'Campinas', 'SP', '13010-111'),
('Avenida Orosimbo Maia', '1500', 'Vila Itapura', 'Campinas', 'SP', '13023-001');

INSERT INTO motoristas
(nome, cpf, telefone, cnh, status)
VALUES
('André Martins', '111.111.111-01', '11990000001', 'SP1234567', 'Ativo'),
('Roberto Souza', '111.111.111-02', '11990000002', 'SP1234568', 'Ativo'),
('Marcos Lima', '111.111.111-03', '11990000003', 'SP1234569', 'Ativo'),
('Eduardo Costa', '111.111.111-04', '11990000004', 'SP1234570', 'Inativo'),
('Felipe Oliveira', '111.111.111-05', '11990000005', 'SP1234571', 'Ativo'),
('Ricardo Santos', '111.111.111-06', '11990000006', 'SP1234572', 'Ativo'),
('Alexandre Rocha', '111.111.111-07', '11990000007', 'SP1234573', 'Inativo'),
('Daniel Pereira', '111.111.111-08', '11990000008', 'SP1234574', 'Ativo'),
('Vinicius Alves', '111.111.111-09', '11990000009', 'SP1234575', 'Ativo'),
('Leonardo Ribeiro', '111.111.111-10', '11990000010', 'SP1234576', 'Ativo'),
('Henrique Gomes', '111.111.111-11', '11990000011', 'SP1234577', 'Inativo'),
('Samuel Carvalho', '111.111.111-12', '11990000012', 'SP1234578', 'Ativo'),
('Diego Barbosa', '111.111.111-13', '11990000013', 'SP1234579', 'Ativo'),
('Caio Ferreira', '111.111.111-14', '11900000014', 'SP1234580', 'Ativo'),
('Rafael Mendes', '111.111.111-15', '11990000015', 'SP1234581', 'Inativo'),
('Bruno Nunes', '111.111.111-16', '11990000016', 'SP1234582', 'Ativo'),
('Gustavo Castro', '111.111.111-17', '11990000017', 'SP1234583', 'Ativo'),
('Thiago Moreira', '111.111.111-18', '11990000018', 'SP1234584', 'Ativo'),
('Fernando Dias', '111.111.111-19', '11990000019', 'SP1234585', 'Inativo'),
('Marcelo Vieira', '111.111.111-20', '11990000020', 'SP1234586', 'Ativo');

INSERT INTO veiculos
(id_motorista, modelo, marca, placa, ano, cor)
VALUES
(1, 'Onix', 'Chevrolet', 'ABC1A01', 2022, 'Prata'),
(2, 'HB20', 'Hyundai', 'ABC1A02', 2021, 'Branco'),
(3, 'Corolla', 'Toyota', 'ABC1A03', 2023, 'Preto'),
(4, 'Ka', 'Ford', 'ABC1A04', 2020, 'Cinza'),
(5, 'T-Cross', 'Volkswagen', 'ABC1A05', 2022, 'Azul'),
(6, 'Argo', 'Fiat', 'ABC1A06', 2021, 'Vermelho'),
(7, 'Civic', 'Honda', 'ABC1A07', 2023, 'Preto'),
(8, 'Tracker', 'Chevrolet', 'ABC1A08', 2022, 'Branco'),
(9, 'Kicks', 'Nissan', 'ABC1A09', 2021, 'Cinza'),
(10, 'Virtus', 'Volkswagen', 'ABC1A10', 2023, 'Prata'),
(11, 'Cronos', 'Fiat', 'ABC1A11', 2020, 'Branco'),
(12, 'Creta', 'Hyundai', 'ABC1A12', 2022, 'Preto'),
(13, 'City', 'Honda', 'ABC1A13', 2023, 'Prata'),
(14, 'Renegade', 'Jeep', 'ABC1A14', 2021, 'Verde'),
(15, 'Sentra', 'Nissan', 'ABC1A15', 2022, 'Azul'),
(16, 'Mobi', 'Fiat', 'ABC1A16', 2020, 'Vermelho'),
(17, 'Nivus', 'Volkswagen', 'ABC1A17', 2023, 'Cinza'),
(18, 'C4 Cactus', 'Citroën', 'ABC1A18', 2022, 'Branco'),
(19, 'Yaris', 'Toyota', 'ABC1A19', 2021, 'Prata'),
(20, 'Pulse', 'Fiat', 'ABC1A20', 2023, 'Preto');

INSERT INTO corridas
(id_usuario, id_motorista, id_origem, id_destino, data_hora, valor, status)
VALUES
(1, 1, 1, 2, '2026-09-01 08:15:00', 25.50, 'Finalizada'),
(2, 2, 3, 4, '2026-09-01 09:30:00', 32.00, 'Finalizada'),
(3, 1, 5, 6, '2026-09-01 11:00:00', 18.75, 'Finalizada'),
(4, 5, 7, 8, '2026-09-02 14:20:00', 42.90, 'Finalizada'),
(5, 6, 9, 10, '2026-09-02 17:45:00', 27.40, 'Finalizada'),
(6, 8, 11, 12, '2026-09-03 07:50:00', 35.00, 'Finalizada'),
(7, 9, 13, 14, '2026-09-03 12:10:00', 22.50, 'Finalizada'),
(8, 10, 15, 16, '2026-09-04 18:30:00', 48.90, 'Finalizada'),
(9, 12, 17, 18, '2026-09-05 10:15:00', 19.90, 'Finalizada'),
(10, 13, 19, 20, '2026-09-05 16:40:00', 55.00, 'Finalizada'),
(11, 14, 2, 5, '2026-09-06 09:20:00', 31.50, 'Cancelada'),
(12, 16, 4, 7, '2026-09-06 13:00:00', 28.75, 'Finalizada'),
(13, 17, 6, 9, '2026-09-07 15:25:00', 44.20, 'Finalizada'),
(14, 18, 8, 11, '2026-09-08 08:45:00', 36.80, 'Finalizada'),
(15, 20, 10, 13, '2026-09-08 19:10:00', 29.90, 'Cancelada'),
(16, 1, 12, 15, '2026-09-09 07:30:00', 52.00, 'Finalizada'),
(17, 2, 14, 17, '2026-09-09 13:45:00', 24.60, 'Finalizada'),
(18, 3, 16, 19, '2026-09-10 17:20:00', 39.90, 'Finalizada'),
(19, 5, 18, 20, '2026-09-11 20:00:00', 61.50, 'Finalizada'),
(20, 6, 20, 1, '2026-09-12 10:30:00', 33.30, 'Finalizada');

INSERT INTO avaliacoes
(id_corrida, nota, comentario) VALUES
(1, 5, 'Motorista muito educado e viagem tranquila.'),
(2, 4, 'Boa corrida e motorista pontual.'),
(3, 5, 'Excelente atendimento.'),
(4, 5, 'Carro limpo e confortável.'),
(5, 4, 'Tudo ocorreu muito bem.'),
(6, 5, 'Motorista muito profissional.'),
(7, 3, 'A viagem foi boa, mas demorou um pouco.'),
(8, 5, 'Excelente experiência.'),
(9, 4, 'Boa viagem e motorista atencioso.'),
(10, 5, 'Muito rápido e seguro.'),
(11, 1, 'Corrida cancelada.'),
(12, 4, 'Boa experiência.'),
(13, 5, 'Motorista excelente.'),
(14, 4, 'Tudo certo durante a corrida.'),
(15, 1, 'Corrida cancelada.'),
(16, 5, 'Muito satisfeito com a viagem.'),
(17, 4, 'Motorista educado.'),
(18, 5, 'Viagem tranquila.'),
(19, 5, 'Ótimo motorista e carro.'),
(20, 4, 'Boa corrida.');

INSERT INTO pagamentos
(id_corrida, forma_pagamento, valor, status, data_pagamento) VALUES
(1, 'Pix', 25.50, 'Pago', '2026-09-01 08:45:00'),
(2, 'Cartão', 32.00, 'Pago', '2026-09-01 10:00:00'),
(3, 'Dinheiro', 18.75, 'Pago', '2026-09-01 11:30:00'),
(4, 'Pix', 42.90, 'Pago', '2026-09-02 14:55:00'),
(5, 'Cartão', 27.40, 'Pago', '2026-09-02 18:20:00'),
(6, 'Pix', 35.00, 'Pago', '2026-09-03 08:20:00'),
(7, 'Dinheiro', 22.50, 'Pago', '2026-09-03 12:40:00'),
(8, 'Cartão', 48.90, 'Pago', '2026-09-04 19:00:00'),
(9, 'Pix', 19.90, 'Pago', '2026-09-05 10:40:00'),
(10, 'Cartão', 55.00, 'Pago', '2026-09-05 17:05:00'),
(11, 'Pix', 31.50, 'Cancelado', '2026-09-06 09:25:00'),
(12, 'Dinheiro', 28.75, 'Pago', '2026-09-06 13:30:00'),
(13, 'Pix', 44.20, 'Pago', '2026-09-07 15:55:00'),
(14, 'Cartão', 36.80, 'Pago', '2026-09-08 09:15:00'),
(15, 'Dinheiro', 29.90, 'Cancelado', '2026-09-08 19:15:00'),
(16, 'Pix', 52.00, 'Pago', '2026-09-09 08:00:00'),
(17, 'Cartão', 24.60, 'Pago', '2026-09-09 14:20:00'),
(18, 'Pix', 39.90, 'Pago', '2026-09-10 17:55:00'),
(19, 'Cartão', 61.50, 'Pago', '2026-09-11 20:40:00'),
(20, 'Dinheiro', 33.30, 'Pago', '2026-09-12 11:10:00');

INSERT INTO historico_corridas
(id_corrida, status_anterior, novo_status, data_alteracao) VALUES
-- Corrida 1
(1, NULL, 'Solicitada', '2026-09-01 08:15:00'),
(1, 'Solicitada', 'Aceita', '2026-09-01 08:17:00'),
(1, 'Aceita', 'Em andamento', '2026-09-01 08:20:00'),
(1, 'Em andamento', 'Finalizada', '2026-09-01 08:42:00'),
-- Corrida 2
(2, NULL, 'Solicitada', '2026-09-01 09:30:00'),
(2, 'Solicitada', 'Aceita', '2026-09-01 09:32:00'),
(2, 'Aceita', 'Em andamento', '2026-09-01 09:35:00'),
(2, 'Em andamento', 'Finalizada', '2026-09-01 09:58:00'),
-- Corrida 3
(3, NULL, 'Solicitada', '2026-09-01 11:00:00'),
(3, 'Solicitada', 'Aceita', '2026-09-01 11:02:00'),
(3, 'Aceita', 'Em andamento', '2026-09-01 11:05:00'),
(3, 'Em andamento', 'Finalizada', '2026-09-01 11:28:00'),
-- Corrida 4
(4, NULL, 'Solicitada', '2026-09-02 14:20:00'),
(4, 'Solicitada', 'Aceita', '2026-09-02 14:23:00'),
(4, 'Aceita', 'Em andamento', '2026-09-02 14:27:00'),
(4, 'Em andamento', 'Finalizada', '2026-09-02 14:52:00'),
-- Corrida 11 cancelada
(11, NULL, 'Solicitada', '2026-09-06 09:20:00'),
(11, 'Solicitada', 'Cancelada', '2026-09-06 09:25:00'),
-- Corrida 15 cancelada
(15, NULL, 'Solicitada', '2026-09-08 19:10:00'),
(15, 'Solicitada', 'Cancelada', '2026-09-08 19:15:00');