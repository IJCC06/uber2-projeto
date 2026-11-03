# Uber 2.0.0 — Arquitetura simplificada

## Objetivo

Evoluir o Uber 2 de uma aplicação Python/SQLite de terminal para uma aplicação web Flask com PostgreSQL, mantendo a base pequena e explícita.

## Stack

- Python
- Flask
- python-dotenv
- PostgreSQL com Psycopg 3 (`psycopg[binary]`)
- HTML, CSS e JavaScript
- `unittest` da biblioteca padrão do Python

Não são usadas extensões de ORM, migrações, formulários ou autenticação.

## Estrutura

- `app.py`: cria a aplicação Flask e concentra as rotas enquanto o projeto é pequeno.
- `../conexao.py`: abre conexões Psycopg usando `DATABASE_URL`.
- `run.py`: ponto de entrada para iniciar o servidor.
- `sql/`: scripts SQL versionados, aplicados manualmente e em ordem.
- `templates/` e `static/`: páginas HTML, CSS e JavaScript.
- `tests/`: testes automatizados com `unittest`.

## Configuração local

1. Crie e ative um ambiente virtual.
2. Instale as dependências de `requirements.txt`.
3. Copie `.env.example` para `.env` e ajuste as credenciais.
4. Crie o banco PostgreSQL `uber2_v2`.
5. Execute `python -m flask --app run.py run --debug`.

`DATABASE_URL` usa o formato `postgresql://usuario:senha@host:porta/banco`.

## Regras de negócio

- Ciclo da corrida: Solicitada → Aceita → Em andamento → Finalizada; também pode ser Cancelada conforme as regras de transição.
- Pagamento apenas para corrida finalizada e no máximo um por corrida.
- No máximo uma avaliação por corrida, com nota entre 1 e 5.
- Mudanças de status geram histórico na mesma transação do banco.
- A disponibilidade do motorista é separada do estado da conta.
- Senhas usam hash seguro; nunca são armazenadas em texto puro.
- Ações administrativas exigem autorização explícita.
