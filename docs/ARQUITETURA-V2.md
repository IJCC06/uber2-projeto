# Uber 2.0.0 — Arquitetura inicial

## Objetivo

Evoluir o Uber 2 de uma aplicação Python/SQLite de terminal para uma aplicação web com Flask e PostgreSQL.

## Estilo arquitetural

Monólito modular com separação entre:
- **Routes:** recebe requisições HTTP e devolve respostas.
- **Services:** implementa regras de negócio e coordena operações.
- **Models:** representa entidades e relacionamentos persistidos pelo SQLAlchemy.
- **Templates e static:** interface HTML, CSS e JavaScript.

## Stack

- Python
- Flask
- Flask-SQLAlchemy
- Flask-Migrate
- Flask-Login
- PostgreSQL com Psycopg 3
- Bootstrap, HTML, CSS e JavaScript
- pytest

## Entidades previstas

Usuário, Motorista, Veículo, Corrida, Pagamento, Avaliação e Histórico de Corridas.

## Regras importantes a preservar e melhorar

- Ciclo da corrida: Solicitada → Aceita → Em andamento → Finalizada; também pode ser Cancelada conforme as regras de transição.
- Pagamento apenas para corrida finalizada.
- No máximo um pagamento por corrida.
- No máximo uma avaliação por corrida.
- Nota de avaliação entre 1 e 5.
- Toda mudança de status da corrida deve gerar histórico na mesma transação do banco.
- Disponibilidade do motorista deve ser separada do estado da conta.
- Senhas devem ser armazenadas com hash seguro; nunca em texto puro.
- Ações administrativas devem exigir autorização explícita.

## Configuração local

1. Criar e ativar um ambiente virtual.
2. Instalar as dependências de requirements.txt.
3. Copiar .env.example para .env e ajustar as credenciais.
4. Criar o banco PostgreSQL uber2_v2.
5. Inicializar migrações com Flask-Migrate.
6. Executar flask --app run.py run --debug.

## Primeira verificação

A rota GET /health confirma que o servidor Flask está ativo. Ela não confirma, por si só, a disponibilidade do PostgreSQL.
