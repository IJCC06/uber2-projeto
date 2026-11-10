# Uber 2.0.0 — Arquitetura

## Objetivo

A versão 2.0.0 evolui o projeto acadêmico Uber 2, originalmente desenvolvido como aplicação de terminal em Python com SQLite, para uma aplicação web com Flask e PostgreSQL. A versão anterior é preservada na branch v1.0.0.

A prioridade da v2 é manter uma estrutura simples, modular e adequada ao desenvolvimento incremental.

## Tecnologias

- Python 3
- Flask — aplicação web e rotas HTTP
- PostgreSQL — banco de dados relacional
- psycopg2-binary — conexão entre Python e PostgreSQL
- python-dotenv — leitura das configurações locais em .env
- HTML, CSS e JavaScript — interface
- Flask-Login — autenticação web e gerenciamento de sessões

Não está previsto, neste momento, utilizar ORM ou ferramenta de migração de banco de dados. O acesso ao PostgreSQL é feito com SQL e Psycopg2.

## Estrutura atual do repositório

A estrutura abaixo representa os diretórios e arquivos relevantes já existentes na branch:

```text
uber2-projeto/
├── app.py
├── conexao.py
├── requirements.txt
├── README.md
├── .gitignore
├── docs/
│   └── ARQUITETURA-V2.md
├── sql/
│   ├── create-table.sql
│   ├── adicionar-distancia-corridas.sql
│   ├── gerar_dados_ficticios.py
│   ├── insert-date.sql
│   └── query.sql
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

A pasta python ainda contém módulos herdados da versão de terminal/SQLite. O módulo python/logins.py é utilizado atualmente por app.py; os demais módulos antigos ainda precisam ser avaliados antes de uma reorganização. A estrutura poderá ser simplificada conforme as funcionalidades web forem implementadas.

## Responsabilidade dos arquivos principais

- app.py: instancia a aplicação Flask, define as rotas e encaminha as requisições.
- conexao.py: centraliza a criação de conexões com o PostgreSQL usando Psycopg2.
- python/logins.py: contém as funções de validação de login chamadas atualmente pelas rotas.
- templates/: reúne os arquivos HTML renderizados pelo Flask.
- static/: reúne os arquivos estáticos, como CSS e JavaScript.
- sql/: contém os scripts SQL e utilitários de dados de teste versionados.

## Configuração do banco de dados

A aplicação carrega as variáveis locais com python-dotenv. O arquivo .env deve permanecer local e não deve ser enviado ao Git.

Variáveis utilizadas atualmente:

```env
DB_HOST=localhost
DB_NAME=uber2_v2
DB_USER=seu_usuario
DB_PASSWORD=sua_senha
```

A função criar_conexao(), em conexao.py, utiliza essas quatro variáveis para abrir a conexão com PostgreSQL por meio de psycopg2.

O banco deve ser criado no PostgreSQL antes de executar os scripts SQL. Os scripts disponíveis estão em sql/ e devem ser revisados antes da execução. Em especial, insert-date.sql contém comandos de limpeza e não deve ser executado em um banco com dados que precisem ser preservados. Para bancos já criados, adicionar-distancia-corridas.sql inclui a coluna de distância sem remover os registros existentes.

## Instalação e execução

1. Instale Python 3 e PostgreSQL.
2. Crie e ative um ambiente virtual na pasta do projeto.
3. Instale as dependências listadas em requirements.txt.
4. Configure DB_HOST, DB_NAME, DB_USER e DB_PASSWORD em um arquivo local .env.
5. Crie o banco configurado no PostgreSQL.
6. Execute os scripts SQL necessários, após revisar seu conteúdo.
7. Inicie a aplicação:

```bash
python app.py
```

O arquivo app.py inicia o servidor Flask em modo de depuração quando executado diretamente. O modo de depuração é destinado ao desenvolvimento local, não à produção.

## Estado atual da versão 2

Já estão presentes:

- aplicação Flask inicializada em app.py;
- conexão PostgreSQL centralizada em conexao.py, utilizando Psycopg2;
- carregamento de variáveis de ambiente com python-dotenv;
- rotas iniciais para exibir a tela de login;
- rotas POST para tentativa de login de usuário e motorista;
- rota de login administrativo;
- rota para exibir a página inicial do usuário;
- painel administrativo com indicadores agregados e lista das corridas recentes;
- cadastro, consulta, edição e remoção de veículos, sempre vinculados ao motorista autenticado;
- avaliação de uma corrida finalizada pelo usuário, com nota de 1 a 5 e comentário opcional;
- consulta pelo motorista da própria média e das avaliações recentes recebidas;
- edição dos dados pessoais e alteração de senha pelo usuário autenticado;
- edição dos dados pessoais e alteração de senha pelo motorista autenticado;
- edição dos dados pessoais e alteração de senha pelo administrador autenticado;
- consulta administrativa de usuários e ativação/desativação de contas;
- consulta administrativa de motoristas e ativação/desativação de contas, bloqueada enquanto houver corridas atribuídas em andamento;
- histórico do motorista com corridas finalizadas ou canceladas e soma bruta dos valores finalizados;
- integração das rotas com funções existentes em python/logins.py;
- templates HTML, arquivos estáticos e scripts SQL no repositório.

A v2 ainda está em desenvolvimento. A presença de uma rota ou tela não significa que todos os fluxos de negócio da versão anterior já foram migrados para a aplicação web.

## Próximas etapas previstas

- revisar e alinhar a estrutura de diretórios;
- atualizar as dependências para refletir a escolha de Psycopg2;
- migrar gradualmente as funcionalidades da versão de terminal para rotas web;
- revisar os scripts SQL, constraints e integridade das operações;
- criar testes automatizados para rotas e regras de negócio;
- atualizar a documentação conforme cada funcionalidade for concluída.

## Regras de negócio previstas

As regras funcionais da versão anterior servirão como referência para a migração, com validação e ajustes durante a implementação web. Entre elas:

- fluxo de corrida: Solicitada → Aceita → Em andamento → Finalizada, com possibilidade de cancelamento conforme as regras definidas;
- motoristas podem cancelar suas corridas nos estados Aceita ou Em andamento; o cancelamento é registrado no histórico;
- usuários podem cancelar suas próprias corridas enquanto estiverem no estado Solicitada; o cancelamento é registrado no histórico;
- motoristas com conta ativa podem habilitar ou desabilitar o recebimento de novas solicitações, sem alterar as corridas já atribuídas;
- valor da corrida calculado no protótipo por R$ 2,50 por quilômetro informado pelo motorista ao finalizar;
- pagamentos associados a corridas finalizadas, com método escolhido pelo usuário e status inicial Pendente;
- o registro de pagamento não processa nem confirma uma cobrança; integração com gateway permanece futura;
- avaliação de corridas finalizadas pelo usuário, com nota de 1 a 5, comentário opcional e limite de uma avaliação por corrida;
- no máximo um pagamento por corrida;
- no máximo uma avaliação por corrida, com nota de 1 a 5;
- registro do histórico de mudanças de status;
- separação entre situação da conta do motorista e disponibilidade para receber corridas;
- contas de usuário desativadas pela administração não podem iniciar sessão nem continuar usando sessão existente;
- motoristas desativados não podem iniciar sessão nem continuar usando sessão existente;
- autorização adequada para operações administrativas e para acesso aos dados de cada usuário.

As regras devem ser garantidas no backend e, quando aplicável, também por constraints no banco de dados.
