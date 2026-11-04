# Uber 2 — Versão 2.0.0

Projeto acadêmico de gerenciamento de corridas. A versão 2.0.0 está em desenvolvimento e tem como objetivo transformar a aplicação original de terminal em uma aplicação web.

- **Branch desta versão:** v2.0.0
- **Versão anterior:** preservada na branch v1.0.0
- **Backend:** Python + Flask
- **Banco de dados:** PostgreSQL
- **Interface:** HTML, CSS e JavaScript

## Sobre o projeto

O Uber 2 começou como um sistema de terminal em Python e SQLite, com funcionalidades relacionadas a usuários, motoristas, veículos, corridas, pagamentos, avaliações e histórico.

Na versão 2.0.0, a proposta é disponibilizar essas funcionalidades por uma interface web, utilizando Flask no backend e PostgreSQL como banco de dados. A migração está sendo feita gradualmente; portanto, nem todas as funcionalidades da versão anterior estão disponíveis na aplicação web ainda.

## Tecnologias escolhidas

- **Python 3**
- **Flask** — servidor web e rotas
- **PostgreSQL** — banco de dados
- **psycopg2-binary** — driver de conexão com PostgreSQL
- **python-dotenv** — carregamento das configurações locais
- **Flask-Login** — dependência mantida para implementação futura de autenticação e sessões
- **HTML, CSS e JavaScript** — frontend

O Flask-Login está mantido para uso futuro. A autenticação web com gerenciamento de sessão ainda não está concluída.

## O que já foi desenvolvido na v2

Até o momento, o repositório contém:

- estrutura inicial de uma aplicação Flask;
- conexão com PostgreSQL centralizada em conexao.py;
- leitura de configurações por variáveis de ambiente;
- tela de login renderizada pelo Flask;
- rotas para tentativa de login de usuário, motorista e administrador;
- rota para exibir a página inicial do usuário;
- templates HTML e diretórios de arquivos estáticos;
- scripts SQL para criação das tabelas, dados de exemplo e consultas;
- módulo de funções de login em python/logins.py, utilizado pelo app.py.

Esses itens representam a base inicial da aplicação. As demais funcionalidades do sistema original ainda serão migradas e integradas progressivamente.

## Estrutura atual

```text
uber2-projeto/
├── app.py
├── conexao.py
├── requirements.txt
├── README.md
├── .gitignore
├── docs/
│   ├── ARQUITETURA-V2.md
│   └── sql/
│       ├── create-table.sql
│       ├── insert-date.sql
│       └── query.sql
├── python/
│   └── logins.py
├── templates/
│   ├── admins/
│   ├── logins/
│   ├── motoristas/
│   └── usuarios/
└── static/
    ├── css/
    └── js/
```

A pasta python ainda possui código herdado da versão de terminal. O módulo python/logins.py é utilizado pela aplicação atual; os demais módulos antigos serão avaliados durante a reorganização, sem apagar a versão anterior preservada na branch v1.0.0.

## Banco de dados e configuração

A aplicação utiliza PostgreSQL. A conexão é criada em conexao.py com psycopg2, lendo as seguintes variáveis de ambiente:

```env
DB_HOST=localhost
DB_NAME=uber2_v2
DB_USER=seu_usuario
DB_PASSWORD=sua_senha
```

Crie um arquivo local chamado .env na raiz do projeto e configure os valores de acordo com seu PostgreSQL. **Não compartilhe nem envie o arquivo .env ao Git**, pois ele contém credenciais.

Os scripts SQL estão em docs/sql/:

- create-table.sql — criação das tabelas e estruturas do banco;
- insert-date.sql — dados de exemplo;
- query.sql — consultas SQL.

> Atenção: revise insert-date.sql antes de executá-lo. Ele contém comandos que limpam tabelas e reiniciam identificadores, podendo apagar dados existentes.

## Como preparar o ambiente

Na raiz do projeto, crie e ative um ambiente virtual:

```bash
python -m venv .venv
```

No Windows (PowerShell):

```powershell
.venv\Scripts\Activate.ps1
```

No Linux ou macOS:

```bash
source .venv/bin/activate
```

Instale as dependências:

```bash
pip install -r requirements.txt
```

Depois de configurar o PostgreSQL e o arquivo .env, inicie a aplicação:

```bash
python app.py
```

O servidor Flask será iniciado em modo de depuração para desenvolvimento local.

## Funcionalidades planejadas para a aplicação web

A migração pretende contemplar os principais recursos do sistema original:

- cadastro e gerenciamento de usuários;
- autenticação e sessões para os diferentes perfis;
- cadastro e gerenciamento de motoristas e veículos;
- solicitação, aceite, atualização e cancelamento de corridas;
- pagamentos associados às corridas;
- avaliações;
- histórico de alterações;
- área administrativa e consultas.

Essas funcionalidades são objetivos de desenvolvimento, não uma lista de recursos já concluídos na v2.

## Regras de negócio de referência

A versão anterior já trabalha com regras como:

- origem e destino de uma corrida não podem ser iguais;
- valor de corrida não pode ser negativo;
- nota de avaliação deve estar entre 1 e 5;
- pagamento e avaliação dependem da finalização da corrida;
- uma corrida não deve ter mais de um pagamento ou avaliação;
- motoristas precisam atender às condições de situação e disponibilidade;
- usuários e motoristas devem acessar somente os dados e operações permitidos para seus perfis.

As regras serão reimplementadas e testadas no backend web durante a migração.

## Documentação

Para detalhes sobre a organização técnica, configuração e decisões de arquitetura, consulte [docs/ARQUITETURA-V2.md](docs/ARQUITETURA-V2.md).

## Projeto acadêmico

O projeto tem como objetivo praticar desenvolvimento web com Python, organização de aplicações, integração com banco de dados relacional, SQL, operações CRUD, autenticação e implementação de regras de negócio.
