# Uber 2 — Versão 2.0.0

Projeto acadêmico de gerenciamento de corridas. A versão 2.0.0 está em desenvolvimento e tem como objetivo transformar a aplicação original de terminal em uma aplicação web.

- **Branch desta versão:** v2.0.0
- **Versão anterior:** preservada na branch v1.0.0
- **Backend:** Python + Flask
- **Banco de dados:** PostgreSQL
- **Interface:** HTML, CSS e JavaScript

## Sobre o projeto

O Uber 2 começou como um sistema de terminal em Python e SQLite, com funcionalidades relacionadas a usuários, motoristas, veículos, corridas, pagamentos, avaliações e histórico.

Na versão 2.0.0, a aplicação web usa Flask e PostgreSQL para oferecer o fluxo principal de contas, corridas, pagamentos pendentes, avaliações e gestão administrativa. Ela é um protótipo acadêmico; nem todas as funcionalidades da antiga aplicação de terminal fazem parte do escopo web.

## Tecnologias escolhidas

- **Python 3**
- **Flask** — servidor web e rotas
- **PostgreSQL** — banco de dados
- **psycopg2-binary** — driver de conexão com PostgreSQL
- **python-dotenv** — carregamento das configurações locais
- **Flask-Login** — autenticação e gerenciamento de sessões
- **HTML, CSS e JavaScript** — frontend

## O que já foi desenvolvido na v2

Até o momento, o repositório contém:

- estrutura inicial de uma aplicação Flask;
- conexão com PostgreSQL centralizada em conexao.py;
- leitura de configurações por variáveis de ambiente;
- tela de login renderizada pelo Flask;
- rotas para tentativa de login de usuário, motorista e administrador;
- cadastro público de motoristas, com contas inicialmente inativas até ativação administrativa;
- rota para exibir a página inicial do usuário;
- templates HTML e diretórios de arquivos estáticos;
- scripts SQL para criação das tabelas, dados de exemplo e consultas;
- módulo de funções de login em python/logins.py, utilizado pelo app.py;
- solicitação de corridas por usuários e fluxo de aceite, início, cancelamento e finalização por motoristas;
- cadastro, consulta, edição e remoção dos veículos vinculados à conta do motorista;
- cálculo de tarifa de teste de R$ 2,50 por quilômetro informado pelo motorista;
- registro da forma de pagamento pelo usuário após a finalização, com status inicial pendente;
- avaliação de uma corrida finalizada pelo usuário, com nota de 1 a 5 e comentário opcional;
- edição dos dados pessoais e alteração de senha da própria conta de usuário;
- edição dos dados pessoais e alteração de senha pelo próprio motorista;
- edição dos dados pessoais e alteração de senha pelo próprio administrador;
- consulta administrativa de usuários, com pesquisa por nome e ativação/desativação de contas;
- consulta administrativa de motoristas, com pesquisa por nome e ativação/desativação preservando corridas já atribuídas;
- histórico administrativo completo de corridas, com filtro por status, pagamentos, avaliações e linha do tempo;
- consulta administrativa de pagamentos, com filtros por status e forma e resumo dos valores registrados;
- consulta administrativa de avaliações, com nota média, filtro por nota e comentários;
- exibição da média e das avaliações recentes recebidas pelo motorista;
- histórico de corridas finalizadas e canceladas do motorista, com resumo de valores brutos;
- painel administrativo com indicadores de usuários, motoristas, corridas e pagamentos, além das corridas recentes.

Motoristas podem cancelar uma corrida atribuída a eles enquanto estiver nos estados “Aceita” ou “Em andamento”. A transição fica registrada no histórico.
Usuários podem cancelar suas próprias solicitações enquanto o status ainda for “Solicitada”; o cancelamento também fica registrado no histórico.
Motoristas com conta ativa podem habilitar ou desabilitar o recebimento de novas solicitações, sem afetar as corridas que já aceitaram.

Essas funcionalidades compõem o escopo web implementado até aqui. Recursos de produção, como processamento real de pagamentos, mapas/geolocalização e implantação endurecida, não fazem parte deste protótipo.
Contas de usuário desativadas pela administração não podem iniciar uma sessão nem continuar usando uma sessão existente.
Contas de motorista desativadas também perdem o acesso; a desativação é bloqueada enquanto houver corridas aceitas ou em andamento.

## Estrutura atual

```text
uber2-projeto/
├── app.py
├── conexao.py
├── blueprints/
│   ├── auth.py
│   ├── usuarios.py
│   ├── motoristas.py
│   └── admins.py
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
├── tests/
│   └── test_postgres_acceptance.py
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

A aplicação utiliza PostgreSQL. Crie um arquivo `.env` na raiz do projeto com as configurações do banco e uma chave secreta para as sessões Flask:

```env
DB_HOST=localhost
DB_NAME=uber2_v2
DB_USER=seu_usuario
DB_PASSWORD=sua_senha
SECRET_KEY=cole_aqui_a_chave_gerada
```

Gere uma chave forte localmente, sem compartilhá-la:

```powershell
python -c "import secrets; print(secrets.token_hex(32))"
```

Copie o valor exibido para `SECRET_KEY`. A chave deve permanecer estável entre reinicializações para preservar as sessões existentes. **Não use uma chave de exemplo, não compartilhe nem envie o arquivo `.env` ao Git**; ele contém credenciais e um segredo de sessão. O `.env` já está listado no `.gitignore`.

A conexão é criada em `conexao.py` com psycopg2, lendo `DB_HOST`, `DB_NAME`, `DB_USER` e `DB_PASSWORD`. `app.py` carrega o mesmo arquivo para ler `SECRET_KEY`.

Os scripts de banco estão na pasta sql/:

- create-table.sql — cria as tabelas em um banco novo;
- adicionar-distancia-corridas.sql — adiciona a coluna de distância a um banco já criado, preservando os registros;
- gerar_dados_ficticios.py — insere dados de teste usando Faker;
- query.sql — consultas SQL.

Para um banco que já existe, execute `sql/adicionar-distancia-corridas.sql` uma vez antes de usar a finalização de corridas. O script `insert-date.sql` é legado: revise-o antes de executar, pois contém comandos que limpam tabelas e reiniciam identificadores.

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

Depois de configurar o PostgreSQL e todas as variáveis do arquivo `.env`, inicie a aplicação:

```bash
python app.py
```

O servidor Flask será iniciado em modo de depuração para desenvolvimento local.

## Verificação do protótipo

Execute a descoberta dos testes. O teste de aceitação é ignorado, a menos que seja habilitado explicitamente:

```powershell
python -m unittest discover -s tests -v
```

O teste de aceitação com banco real cria um schema temporário isolado no PostgreSQL configurado pelo `.env`, percorre o cadastro, aprovação e ciclo completo de uma corrida, e remove somente esse schema ao final. Habilite-o explicitamente no PowerShell:

```powershell
$env:UBER2_TEST_POSTGRES = "1"
python -m unittest discover -s tests -v
```

O teste requer permissão para criar e remover schemas no banco configurado. Ele não modifica as tabelas ou os dados existentes fora do schema temporário.

Além do fluxo de sucesso, a aceitação verifica endereços inválidos, ações fora da ordem permitida, disponibilidade inválida, distâncias malformadas ou fora dos limites, métodos de pagamento inválidos, notas fora do intervalo, operações duplicadas e tentativas não autorizadas. Para comparar a documentação com o comportamento do sistema, confira esses testes junto das rotas em `blueprints/`.

## Funcionalidades previstas para a aplicação web

A migração contempla os principais recursos do sistema original em diferentes estágios de implementação:

- cadastro e gerenciamento de usuários;
- autenticação e sessões para os diferentes perfis;
- cadastro e gerenciamento de motoristas e veículos;
- solicitação, aceite, atualização e cancelamento de corridas;
- pagamentos associados às corridas;
- gerenciamento e consulta de avaliações;
- histórico de alterações;
- área administrativa e consultas.

Alguns recursos dessa lista já estão disponíveis; outros ainda serão implementados ou ampliados.

## Regras de negócio de referência

A versão anterior já trabalha com regras como:

- origem e destino de uma corrida não podem ser iguais;
- valor de corrida não pode ser negativo;
- nota de avaliação deve estar entre 1 e 5;
- pagamento e avaliação dependem da finalização da corrida;
- no protótipo, o valor é calculado em R$ 2,50 por quilômetro informado pelo motorista ao finalizar a corrida;
- o registro de Pix, dinheiro ou cartão cria um pagamento pendente; não há integração com gateway nem confirmação real de cobrança;
- uma corrida não deve ter mais de um pagamento ou avaliação;
- motoristas precisam atender às condições de situação e disponibilidade;
- usuários e motoristas devem acessar somente os dados e operações permitidos para seus perfis.

As regras restantes serão reimplementadas e testadas no backend web durante a migração.

## Documentação

Para detalhes sobre a organização técnica, configuração e decisões de arquitetura, consulte [docs/ARQUITETURA-V2.md](docs/ARQUITETURA-V2.md).

## Projeto acadêmico

O projeto tem como objetivo praticar desenvolvimento web com Python, organização de aplicações, integração com banco de dados relacional, SQL, operações CRUD, autenticação e implementação de regras de negócio.
