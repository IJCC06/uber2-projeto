# Uber 2.0.0 — Arquitetura

## Objetivo

A versão 2.0.0 evolui o projeto acadêmico Uber 2, originalmente desenvolvido como aplicação de terminal em Python com SQLite, para uma aplicação web com Flask e PostgreSQL. A versão anterior é preservada na branch v1.0.0.

A prioridade da v2 é manter uma estrutura simples, modular e adequada ao desenvolvimento incremental.

## Tecnologias

- Python 3
- Flask — aplicação web e rotas HTTP
- PostgreSQL — banco de dados relacional
- psycopg2-binary — conexão entre Python e PostgreSQL
- fpdf2 — geração de relatórios PDF por perfil
- Bootstrap 5.3.9 — grid e componentes utilizados inicialmente no painel administrativo
- Google reCAPTCHA v2 — validação anti-bot server-side nos formulários de login
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
│   ├── logins.py
│   └── pdf_export.py
├── tests/
│   ├── test_admin_navigation.py
│   ├── test_admin_pages.py
│   ├── test_conexao.py
│   ├── test_driver_dashboard.py
│   ├── test_driver_history.py
│   ├── test_driver_profile_pages.py
│   ├── test_login_templates.py
│   ├── test_pdf_export.py
│   ├── test_postgres_acceptance.py
│   ├── test_registration_error_templates.py
│   ├── test_user_dashboard.py
│   ├── test_user_profile_pages.py
│   └── test_user_driver_navigation.py
├── templates/
│   ├── admins/
│   ├── logins/
│   ├── motoristas/
│   └── usuarios/
└── public/
    └── static/
        ├── css/
        ├── js/
        └── vendor/
            └── bootstrap/
                ├── bootstrap.min.css
                └── LICENSE
```

A pasta python ainda contém módulos herdados da versão de terminal/SQLite. O módulo python/logins.py é utilizado atualmente por app.py; os demais módulos antigos ainda precisam ser avaliados antes de uma reorganização. A estrutura poderá ser simplificada conforme as funcionalidades web forem implementadas.

## Responsabilidade dos arquivos principais

- app.py: instancia a aplicação Flask, configura Flask-Login e registra os Blueprints.
- blueprints/: separa autenticação, operações de usuários, motoristas e administração.
- conexao.py: centraliza a criação de conexões com o PostgreSQL usando Psycopg2.
- python/logins.py: contém as funções de validação de login chamadas atualmente pelas rotas.
- python/pdf_export.py: centraliza a formatação, paginação e resposta HTTP dos relatórios PDF.
- tests/: contém testes unitários dos PDFs e teste de aceitação com banco PostgreSQL isolado.
- templates/: reúne os arquivos HTML renderizados pelo Flask.
- public/static/: reúne os arquivos estáticos publicados pela Vercel, como CSS e JavaScript.
- public/static/vendor/bootstrap/: contém a folha de estilos local e a licença MIT do Bootstrap 5.3.9.
- sql/: contém os scripts SQL e utilitários de dados de teste versionados.

## Configuração do banco de dados

A aplicação carrega as variáveis locais com python-dotenv. O arquivo .env deve permanecer local e não deve ser enviado ao Git.

Variáveis utilizadas atualmente:

```env
DB_HOST=localhost
DB_NAME=uber2_v2
DB_USER=seu_usuario
DB_PASSWORD=sua_senha
SECRET_KEY=chave_forte_gerada_localmente
RECAPTCHA_SITE_KEY=chave_publica_do_recaptcha
RECAPTCHA_SECRET_KEY=chave_secreta_do_recaptcha
```

A função `criar_conexao()`, em `conexao.py`, utiliza as quatro variáveis do banco para abrir a conexão com PostgreSQL por meio de psycopg2. `app.py` carrega `SECRET_KEY` do mesmo `.env`; a chave deve ser forte, privada e estável para manter a validade das sessões entre reinicializações. Gere-a localmente com `python -c "import secrets; print(secrets.token_hex(32))"`.

O arquivo `.env` está no `.gitignore` e não deve ser compartilhado nem enviado ao Git.

Os logins de usuário, motorista e administrador usam Google reCAPTCHA v2 do tipo caixa de seleção. Configure as chaves pública e secreta no console do Google para cada domínio usado. O servidor envia o token ao endpoint de verificação do Google com timeout; token ausente, rejeitado, indisponibilidade do serviço ou chaves não configuradas bloqueiam a autenticação. A chave secreta deve ser mantida fora do código e do Git.

O banco deve ser criado no PostgreSQL antes de executar os scripts SQL. Os scripts disponíveis estão em sql/ e devem ser revisados antes da execução. Em especial, insert-date.sql contém comandos de limpeza e não deve ser executado em um banco com dados que precisem ser preservados. Para bancos já criados, adicionar-distancia-corridas.sql inclui a coluna de distância sem remover os registros existentes.

## Instalação e execução

1. Instale Python 3 e PostgreSQL.
2. Crie e ative um ambiente virtual na pasta do projeto.
3. Instale as dependências listadas em requirements.txt.
4. Configure DB_HOST, DB_NAME, DB_USER, DB_PASSWORD, SECRET_KEY, RECAPTCHA_SITE_KEY e RECAPTCHA_SECRET_KEY em um arquivo local `.env`. Gere `SECRET_KEY` localmente com o comando Python documentado acima.
5. Crie o banco configurado no PostgreSQL.
6. Execute os scripts SQL necessários, após revisar seu conteúdo.
7. Inicie a aplicação:

```bash
python app.py
```

O arquivo app.py inicia o servidor Flask em modo de depuração quando executado diretamente. O modo de depuração é destinado ao desenvolvimento local, não à produção.

## Testes e aceitação

A suíte usa `unittest` da biblioteca padrão e pode ser executada com `python -m unittest discover -s tests -v`. O teste de aceitação do PostgreSQL é opt-in com `UBER2_TEST_POSTGRES=1`; ele cria um schema temporário, valida o fluxo ponta a ponta e remove o schema ao final, sem alterar tabelas existentes.

## Estado atual da versão 2

O fluxo web principal está implementado: cadastro e autenticação por perfil, aprovação e disponibilidade de motoristas, gestão de veículos, solicitação e ciclo de vida de corridas, pagamentos registrados como pendentes, avaliações, históricos, gerenciamento de contas e consultas administrativas. As listagens administrativas de usuários e motoristas permitem pesquisar por nome. Erros HTTP comuns usam páginas personalizadas mantendo o status original da resposta. O teste de aceitação executa o fluxo completo em PostgreSQL isolado e verifica também entradas inválidas, transições recusadas, duplicatas, autorização por perfil e páginas de erro.

O projeto continua sendo um protótipo acadêmico. Integração com gateway de pagamento, mapas/geolocalização e implantação de produção estão fora do escopo atual; a aplicação não deve ser tratada como pronta para uso comercial.

As exportações PDF são oferecidas nos históricos e pagamentos do usuário, nos históricos, veículos e avaliações recebidas pelo motorista e nas consultas administrativas. Cada rota de exportação exige login, confere o perfil e restringe os dados pessoais às próprias contas; os relatórios administrativos preservam os filtros da consulta. A biblioteca fpdf2 gera os arquivos em memória, sem gravá-los no servidor.

A migração visual para Bootstrap está concluída em toda a aplicação. Os perfis usuário, motorista e administrador, login, cadastros e páginas de erro usam o Bootstrap 5.3.9 local. Painéis, históricos, solicitações, pagamentos, veículos, contas, usuários, motoristas, corridas e avaliações usam grid, cards, badges, tabelas e formulários responsivos. Os estilos locais restantes complementam identidade visual e elementos específicos das telas.

## Regras de negócio implementadas

As principais regras implementadas no backend incluem:

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
