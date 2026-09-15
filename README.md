# 🚗 Uber 2 — O inimigo agora é outro

> **Uber 2: O inimigo agora é outro.**

Sistema de transporte desenvolvido como **Atividade Integrada de Banco de Dados com Python**, com o objetivo de aplicar, na prática, conhecimentos de **Banco de Dados** e **Programação Web Backend**.

O projeto simula uma plataforma de transporte por aplicativo, permitindo o gerenciamento de usuários, motoristas, veículos, corridas, pagamentos, avaliações e endereços.

---

## 📌 Sobre o Projeto

O **Uber 2** foi desenvolvido para atender aos requisitos propostos na atividade integrada, utilizando **PostgreSQL** para a estrutura do banco de dados e **Python** para a implementação da aplicação.

A proposta é desenvolver um sistema de gerenciamento de corridas que permita cadastrar e consultar informações relacionadas aos passageiros, motoristas e viagens.

O banco de dados será composto por **7 tabelas**, conforme o requisito para equipes formadas por três integrantes.

---

## 🎯 Objetivos

* Desenvolver um banco de dados relacional utilizando PostgreSQL;
* Construir um **Diagrama Entidade-Relacionamento (DER)**;
* Criar as 7 tabelas do sistema;
* Criar scripts para criação e população do banco;
* Realizar consultas SQL que entreguem informações relevantes;
* Aplicar comandos `INSERT`, `UPDATE`, `DELETE` e `WHERE`;
* Desenvolver a aplicação utilizando Python;
* Utilizar funções, listas e dicionários;
* Organizar o projeto utilizando módulos;
* Trabalhar com SQLite utilizando Python, conforme solicitado na atividade.

---

## 🛠️ Tecnologias Utilizadas

### Banco de Dados

* **PostgreSQL**
* **SQLite**
* SQL

### Backend

* **Python**

### Conceitos Aplicados

* DER — Diagrama Entidade-Relacionamento;
* Chaves primárias e estrangeiras;
* Relacionamentos entre tabelas;
* `CREATE TABLE`;
* `INSERT`;
* `UPDATE`;
* `DELETE`;
* `SELECT`;
* `WHERE`;
* Funções;
* Listas;
* Dicionários;
* Módulos;
* Estruturas de decisão;
* Estruturas de repetição.

---

# 🗄️ Banco de Dados

O banco de dados do **Uber 2** será desenvolvido utilizando **PostgreSQL** e contará com **7 tabelas relacionadas entre si**.

As tabelas representam os principais elementos necessários para o funcionamento de uma plataforma de transporte.

## 📊 Tabelas

| Tabela       | Descrição                                          |
| ------------ | -------------------------------------------------- |
| `usuarios`   | Armazena os dados dos passageiros cadastrados      |
| `motoristas` | Armazena os dados dos motoristas                   |
| `veiculos`   | Contém informações dos veículos utilizados         |
| `corridas`   | Registra as corridas realizadas                    |
| `pagamentos` | Armazena os pagamentos das corridas                |
| `avaliacoes` | Registra as avaliações realizadas após as corridas |
| `enderecos`  | Armazena os endereços utilizados nas corridas      |

---

## 👤 1. Usuários

A tabela `usuarios` armazenará as informações dos passageiros que utilizam o sistema.

```text
usuarios
├── id_usuario
├── nome
├── email
├── telefone
├── senha
└── data_cadastro
```

---

## 🚗 2. Motoristas

A tabela `motoristas` armazenará os dados dos motoristas cadastrados na plataforma.

```text
motoristas
├── id_motorista
├── nome
├── cpf
├── telefone
├── cnh
└── status
```

O campo `status` poderá representar, por exemplo:

* Disponível;
* Indisponível;
* Em corrida.

---

## 🚘 3. Veículos

A tabela `veiculos` armazenará os veículos utilizados pelos motoristas.

```text
veiculos
├── id_veiculo
├── id_motorista
├── modelo
├── marca
├── placa
├── ano
└── cor
```

O campo `id_motorista` será utilizado para relacionar o veículo ao seu motorista.

---

## 🏁 4. Corridas

A tabela `corridas` será uma das principais tabelas do sistema e registrará as viagens solicitadas pelos usuários.

```text
corridas
├── id_corrida
├── id_usuario
├── id_motorista
├── id_origem
├── id_destino
├── data_hora
├── valor
└── status
```

O campo `status` poderá assumir valores como:

* Solicitada;
* Aceita;
* Em andamento;
* Finalizada;
* Cancelada.

---

## 💳 5. Pagamentos

A tabela `pagamentos` armazenará as informações referentes ao pagamento de cada corrida.

```text
pagamentos
├── id_pagamento
├── id_corrida
├── forma_pagamento
├── valor
├── status
└── data_pagamento
```

As formas de pagamento poderão incluir:

* Pix;
* Cartão;
* Dinheiro.

---

## ⭐ 6. Avaliações

A tabela `avaliacoes` armazenará a avaliação realizada após uma corrida.

```text
avaliacoes
├── id_avaliacao
├── id_corrida
├── nota
├── comentario
└── data_avaliacao
```

A nota poderá variar de **1 a 5**.

---

## 📍 7. Endereços

A tabela `enderecos` armazenará os locais utilizados como origem e destino das corridas.

```text
enderecos
├── id_endereco
├── rua
├── numero
├── bairro
├── cidade
├── estado
└── cep
```

Uma corrida possuirá um endereço de **origem** e um endereço de **destino**.

---

# 🔗 Relacionamentos

As principais relações entre as tabelas serão:

```text
USUARIOS
   │
   │ 1:N
   ▼
CORRIDAS
   │
   ├──────────────► MOTORISTAS
   │                    │
   │                    │ 1:N
   │                    ▼
   │                 VEICULOS
   │
   ├──────────────► PAGAMENTOS
   │
   ├──────────────► AVALIACOES
   │
   ├──────────────► ENDERECOS
   │                  │
   │                  ├── Origem
   │                  └── Destino
   │
   └────────────────────────
```

O **DER completo** será disponibilizado na pasta de documentação do projeto.

---

# 📝 Scripts SQL

Os scripts SQL serão separados de acordo com suas funções.

### Criação das tabelas

Será utilizado:

```sql
CREATE TABLE
```

para criar as sete tabelas e definir suas respectivas chaves primárias e estrangeiras.

### População

Os dados iniciais serão inseridos utilizando:

```sql
INSERT INTO
```

### Atualização

Para alterar informações:

```sql
UPDATE
```

### Exclusão

Para remover registros:

```sql
DELETE
```

### Consultas

As informações serão consultadas utilizando:

```sql
SELECT
WHERE
```

---

# 🔎 Consultas que Entregam Valor

O sistema contará com consultas que permitam extrair informações relevantes do banco de dados.

Alguns exemplos:

* Quais foram as 5 corridas mais caras?
* Qual motorista realizou mais corridas?
* Qual foi a média de avaliação de cada motorista?
* Qual forma de pagamento foi mais utilizada?
* Quais corridas foram canceladas?
* Quais usuários realizaram mais corridas?
* Quanto foi arrecadado em determinado período?
* Quais motoristas estão disponíveis?
* Qual veículo realizou determinada corrida?

Essas consultas têm como objetivo demonstrar a utilização prática dos dados armazenados.

---

# 🐍 Projeto Python

A aplicação será desenvolvida utilizando Python e deverá aplicar os conceitos trabalhados em sala de aula.

## Funções

As funcionalidades serão organizadas em funções.

Exemplo:

```python
def cadastrar_usuario():
    pass

def cadastrar_motorista():
    pass

def solicitar_corrida():
    pass

def listar_corridas():
    pass

def realizar_pagamento():
    pass
```

## Listas

Listas serão utilizadas para armazenar e manipular conjuntos de informações.

```python
corridas = []
```

## Dicionários

Dicionários poderão representar os dados de cada registro.

```python
usuario = {
    "nome": "João",
    "email": "joao@email.com",
    "telefone": "99999-9999"
}
```

## Módulos

O projeto será dividido em módulos para facilitar a organização, manutenção e reutilização do código.

---

# 📁 Estrutura do Projeto

```text
uber-2/
│
├── README.md
│
├── database/
│   ├── create_tables.sql
│   ├── insert_data.sql
│   └── queries.sql
│
├── der/
│   └── der.png
│
├── python/
│   ├── main.py
│   ├── usuarios.py
│   ├── motoristas.py
│   ├── veiculos.py
│   ├── corridas.py
│   ├── pagamentos.py
│   ├── avaliacoes.py
│   └── enderecos.py
```

---

# 🚕 Funcionalidades

O sistema terá funcionalidades relacionadas ao gerenciamento da plataforma, como:

* Cadastro de usuários;
* Cadastro de motoristas;
* Cadastro de veículos;
* Cadastro de endereços;
* Solicitação de corridas;
* Consulta de corridas;
* Atualização de informações;
* Exclusão de registros;
* Registro de pagamentos;
* Registro de avaliações;
* Consulta de informações utilizando filtros.

---

# 👥 Equipe

| Integrante           | Função          |
| -------------------- | --------------- |
| Gabriel M. Cassano   | Desenvolvimento |
| João Vitor Tezzaro   | Desenvolvimento |
| Ana L. do Nascimento | Desenvolvimento |

---

# 📚 Atividade Acadêmica

Projeto desenvolvido como parte da **Atividade Integrada — Banco de Dados com Python**, aplicando conhecimentos adquiridos nas disciplinas de **Banco de Dados** e **Programação Web Backend**.

### Banco de Dados

* Diagrama Entidade-Relacionamento;
* PostgreSQL;
* SQL;
* `CREATE TABLE`;
* `INSERT`;
* `UPDATE`;
* `DELETE`;
* `WHERE`.

### Python

* Sintaxe da linguagem;
* Estruturas de decisão;
* Estruturas de repetição;
* Listas;
* Dicionários;
* Funções;
* Módulos;
* SQLite com Python.

---

# 🎬 Slogan

> ## **Uber 2: O inimigo agora é outro.**

Um projeto acadêmico inspirado em aplicativos de transporte, desenvolvido para colocar em prática conhecimentos de **Python e Banco de Dados** — porque chamar uma corrida era fácil demais.
