# 🚗 Uber 2

Sistema de gerenciamento de corridas desenvolvido em **Python** utilizando **SQLite**.

O projeto simula o funcionamento básico de uma plataforma de transporte, permitindo o gerenciamento de usuários, motoristas, veículos, corridas, pagamentos e avaliações.

---

## 📌 Sobre o projeto

O **Uber 2** foi desenvolvido como um projeto acadêmico com o objetivo de aplicar conceitos de:

* Python;
* Programação modular;
* Banco de dados relacional;
* SQLite;
* Chaves primárias e estrangeiras;
* Validações;
* Consultas SQL;
* Relacionamentos entre tabelas;
* Menus interativos no terminal.

O sistema possui três tipos de acesso:

* 👤 Usuário;
* 🚗 Motorista;
* 🔐 Administrador.

---

## 🛠️ Tecnologias utilizadas

* **Python 3**
* **SQLite**
* Biblioteca `sqlite3`
* Módulos
* SQL

Não são necessárias bibliotecas externas para executar o projeto.

---

## 📁 Estrutura do projeto

```text
uber2-projeto/
│
├── der/
|   └── der.png
│
├── python/
|   ├── principal.py
|   |
|   ├── banco/
│   |   ├── conexao.py
│   |   └── criar_banco.py
│   |
|   ├── usuarios/
│   |   └── usuarios.py
│   |
|   ├── motoristas/
│   |   └── motoristas.py
│   |
|   ├── veiculos/
│   |   └── veiculos.py
│   |
|   ├── corridas/
│   |   └── corridas.py
│   |
|   ├── pagamentos/
│   |   └── pagamentos.py
│   |
|   ├── avaliacoes/
│   |   └── avaliacoes.py
│   |
|   ├── historico/
│   |   └── historico.py
│   |
|   └── consultas/
|       └── consultas.py
|
├── sql/
|   ├── create-table.sql
|   ├── insert-data.sql
|   └── query.sql
```

O banco de dados `uber2.db` é criado na pasta principal do projeto.

---

## 🗄️ Banco de dados

O sistema utiliza **7 tabelas**:

### `usuarios`

Armazena os dados dos usuários.

Principais informações:

* ID;
* Nome;
* E-mail;
* Telefone;
* Senha;
* Data de cadastro.

### `motoristas`

Armazena os dados dos motoristas.

Principais informações:

* ID;
* Nome;
* CPF;
* Telefone;
* CNH;
* Status.

O status pode ser:

* `Ativo`
* `Inativo`

### `veiculos`

Armazena os veículos associados aos motoristas.

Informações:

* ID;
* Motorista;
* Modelo;
* Marca;
* Placa;
* Ano;
* Cor.

### `corridas`

Armazena as corridas realizadas no sistema.

Informações:

* ID;
* Usuário;
* Motorista;
* Origem;
* Destino;
* Data e hora;
* Valor;
* Status.

Os status possíveis são:

* `Solicitada`
* `Aceita`
* `Em andamento`
* `Finalizada`
* `Cancelada`

### `pagamentos`

Armazena os pagamentos das corridas.

Formas de pagamento:

* `Pix`
* `Dinheiro`
* `Cartão`

Status:

* `Pendente`
* `Pago`
* `Cancelado`

No fluxo atual do sistema, quando o usuário cadastra um pagamento, ele é registrado automaticamente como **Pago**.

### `avaliacoes`

Armazena as avaliações das corridas.

Cada avaliação possui:

* ID;
* Corrida;
* Nota;
* Comentário;
* Data da avaliação.

A nota deve estar entre **1 e 5**.

### `historico_corridas`

Registra as alterações de status das corridas.

São armazenados:

* ID do registro;
* ID da corrida;
* Status anterior;
* Novo status;
* Data da alteração.

---

## 👤 Funcionalidades do usuário

O usuário pode:

### Cadastro

* Criar uma conta;
* Informar nome, e-mail, telefone e senha.

### Login

O acesso é realizado utilizando:

* E-mail;
* Senha.

### Corridas

O usuário pode:

* Solicitar uma corrida;
* Informar origem e destino;
* Visualizar suas próprias corridas.

O sistema não permite que origem e destino sejam iguais.

### Pagamentos

O usuário pode:

* Cadastrar pagamento de uma corrida finalizada;
* Escolher entre Pix, dinheiro ou cartão;
* Consultar seus pagamentos.

O sistema impede o cadastro de mais de um pagamento para a mesma corrida.

### Avaliações

Após uma corrida ser finalizada, o usuário pode:

* Avaliar a corrida;
* Informar uma nota de 1 a 5;
* Adicionar um comentário.

Uma corrida não pode receber mais de uma avaliação do mesmo sistema.

### Dados da conta

O usuário pode:

* Editar seus dados;
* Excluir sua própria conta.

---

## 🚗 Funcionalidades do motorista

O motorista realiza login utilizando seu **CPF**.

Para entrar no sistema, o motorista precisa estar com status `Ativo`.

### Corridas

O motorista pode:

* Visualizar corridas disponíveis;
* Aceitar uma corrida;
* Atualizar o status de uma corrida.

O fluxo de status é:

```text
Solicitada
     ↓
Aceita
     ↓
Em andamento
     ↓
Finalizada
```

Também é possível cancelar uma corrida em determinadas etapas do fluxo.

### Veículos

O motorista pode:

* Cadastrar veículo;
* Listar seus veículos;
* Editar seus veículos;
* Excluir seus veículos.

### Histórico

O motorista pode consultar o histórico das alterações de status das corridas associadas a ele.

### Dados pessoais

O motorista pode editar seus próprios dados.

---

## 🔐 Funcionalidades do administrador

O administrador possui acesso às áreas de gerenciamento do sistema.

### Gerenciamento de usuários

Pode:

* Listar usuários;
* Editar usuários;
* Excluir usuários.

### Gerenciamento de motoristas

Pode:

* Cadastrar motoristas;
* Listar motoristas;
* Editar motoristas;
* Alterar status;
* Excluir motoristas.

### Gerenciamento de veículos

Pode:

* Listar todos os veículos;
* Editar veículos;
* Excluir veículos.

### Gerenciamento de corridas

Pode:

* Listar todas as corridas;
* Editar corridas;
* Excluir corridas;
* Consultar o histórico de uma corrida.

### Gerenciamento de pagamentos

Pode:

* Listar pagamentos;
* Editar pagamentos;
* Excluir pagamentos.

### Gerenciamento de avaliações

Pode:

* Listar avaliações;
* Editar avaliações;
* Excluir avaliações.

---

## 📊 Consultas e relatórios

O sistema possui **9 consultas SQL**:

### 1. Cinco corridas mais caras

Exibe as cinco corridas com maior valor.

### 2. Motorista com mais corridas

Identifica os motoristas com maior quantidade de corridas.

### 3. Forma de pagamento mais utilizada

Mostra a forma de pagamento mais utilizada pelos usuários.

### 4. Usuários com mais corridas

Exibe os usuários que possuem maior quantidade de corridas.

### 5. Motoristas disponíveis

Lista os motoristas que estão com status `Ativo`.

### 6. Histórico de determinada corrida

Permite consultar todas as alterações de status de uma corrida específica.

### 7. Arrecadação por período

Permite informar uma data inicial e uma data final para consultar:

* Quantidade de pagamentos;
* Valor total arrecadado.

São considerados os pagamentos com status `Pago`.

### 8. Média de avaliação dos motoristas

Apresenta a quantidade de avaliações e a média de notas recebidas por cada motorista.

### 9. Média geral dos motoristas

Apresenta a média geral das avaliações dos motoristas.

---

## 🔄 Fluxo principal do sistema

Um exemplo de utilização do sistema:

```text
Cadastro do usuário
        ↓
Login
        ↓
Solicitação de corrida
        ↓
Motorista visualiza corrida
        ↓
Motorista aceita
        ↓
Corrida em andamento
        ↓
Corrida finalizada
        ↓
Pagamento
        ↓
Avaliação
        ↓
Histórico e consultas
```

---

## 📝 Regras importantes

O sistema possui diversas validações para manter a integridade dos dados.

Entre elas:

* E-mail de usuário não pode ser duplicado;
* CPF de motorista não pode ser duplicado;
* CNH não pode ser duplicada;
* Placa de veículo não pode ser duplicada;
* Origem e destino de uma corrida não podem ser iguais;
* Valor da corrida não pode ser negativo;
* Nota de avaliação deve estar entre 1 e 5;
* Uma corrida não pode possuir mais de um pagamento;
* Uma corrida não pode possuir mais de uma avaliação;
* Pagamento só pode ser cadastrado para corrida finalizada;
* Avaliação só pode ser realizada para corrida finalizada;
* Motorista precisa estar ativo para realizar login;
* O motorista só pode gerenciar seus próprios veículos;
* O motorista só pode atualizar corridas associadas a ele;
* O usuário só pode visualizar suas próprias corridas e pagamentos.

---

## ▶️ Como executar

### 1. Clone ou baixe o projeto

Coloque o projeto em uma pasta de sua preferência.

### 2. Abra o terminal na pasta do projeto

Exemplo:

```bash
cd uber2-projeto
```

### 3. Crie o banco de dados

Execute:

```bash
python python/banco/criar_banco.py
```

Isso criará o arquivo:

```text
uber2.db
```

### 4. Execute o sistema

```bash
python python/principal.py
```

O menu principal será exibido:

```text
===================================
             UBER 2
===================================
1 - Login
2 - Cadastrar usuário
0 - Sair
```

---

## 🔑 Acessos

### Usuário

O usuário deve primeiro realizar o cadastro e depois entrar utilizando:

```text
E-mail
Senha
```

### Motorista

O motorista é cadastrado pelo administrador e realiza login utilizando:

```text
CPF
```

O motorista precisa estar com status `Ativo`.

### Administrador

O acesso administrativo utiliza uma senha definida no arquivo `principal.py`.

```python
SENHA_ADMIN = "OInimigoEoTransito"
```

> Para um sistema real, a senha administrativa não deveria ficar diretamente no código. Neste projeto, ela é utilizada dessa forma para fins acadêmicos.

---

## 🧪 Testes realizados

Durante o desenvolvimento, foram testados os principais fluxos do sistema:

* Cadastro de usuário;
* Login de usuário;
* Login de administrador;
* Cadastro de motorista;
* Login de motorista;
* Cadastro de veículo;
* Solicitação de corrida;
* Aceite de corrida;
* Alteração de status;
* Finalização de corrida;
* Cadastro de pagamento;
* Cadastro de avaliação;
* Registro de histórico;
* Consultas e relatórios.

Também foi testado o fluxo completo de uma corrida:

```text
Solicitada → Aceita → Em andamento → Finalizada
```

E o histórico registrou corretamente cada alteração.

---

## 📚 Objetivos acadêmicos

O projeto busca demonstrar conhecimentos de:

* Desenvolvimento em Python;
* Organização de projetos em módulos;
* Funções;
* Estruturas condicionais;
* Laços de repetição;
* Entrada e saída de dados;
* Tratamento de informações;
* SQL;
* SQLite;
* CRUD;
* Relacionamentos entre tabelas;
* Chaves estrangeiras;
* Integridade de dados;
* Consultas com `JOIN`;
* Agregações como `COUNT`, `SUM` e `AVG`.

---

## 👨‍💻 Projeto acadêmico

**Projeto:** Uber 2
**Tecnologia principal:** Python
**Banco de dados:** SQLite
**Tipo:** Sistema de gerenciamento de corridas