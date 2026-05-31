# 🏦 Sistema Bancário Assíncrono - FastAPI

Este é um projeto de API robusta para um sistema bancário, desenvolvido com **Python** e **FastAPI**. O sistema foca em performance através de operações assíncronas e segurança rigorosa utilizando autenticação **JWT (JSON Web Tokens)**.

## 🚀 Funcionalidades

* **Gestão de Usuários**: Cadastro de utilizadores com armazenamento seguro de senhas (hashing com bcrypt).
* **Autenticação Segura**: Fluxo completo de login e geração de tokens de acesso com tempo de expiração.
* **Operações Financeiras**: 
    * Depósitos e saques com atualização automática de saldo.
    * Validação de saldo insuficiente para saques.
* **Segurança de Dados**: 
    * As operações de depósito e saque são protegidas; apenas o utilizador autenticado pode movimentar a sua própria conta.
    * Rotas personalizadas (`/me`) para consulta de dados e extratos do próprio utilizador.
* **Base de Dados**: Persistência de dados utilizando **SQLAlchemy 2.0** com suporte total a `async/await` e SQLite.

## 📋 Pré-requisitos

Antes de começar, você precisará ter as seguintes ferramentas instaladas em sua máquina:

* **Python 3.10 ou superior**: O projeto utiliza recursos modernos de tipagem e assincronismo.
* **Gerenciador de Pacotes**: 
    * **Poetry** (Recomendado): Para uma gestão de dependências mais isolada e segura.
    * **pip**: Caso prefira a instalação padrão do Python.
* **SQLite**: Já vem integrado ao Python, utilizado para o armazenamento local de dados.
* **Git**: Necessário para clonar o repositório.

## 🛠️ Tecnologias Utilizadas

* **FastAPI**: Framework moderno e de alta performance.
* **SQLAlchemy**: ORM para comunicação assíncrona com a base de dados.
* **Pydantic**: Validação de dados e criação de schemas.
* **JWT (Jose)**: Implementação de segurança e tokens.
* **Passlib**: Criptografia de senhas.


### Dependências Principais
O projeto depende das seguintes bibliotecas (que serão instaladas automaticamente no passo de instalação):
* **FastAPI**: Framework web.
* **SQLAlchemy & AIOSQLite**: Para persistência de dados assíncrona.
* **Python-Jose**: Para criptografia e geração de tokens JWT.
* **Passlib [Bcrypt]**: Para o hashing seguro de senhas.

## 📋 Como Executar o Projeto

1. **Clonar o repositório**:
  git clone [https://github.com/karensantostech-art/Projeto_Bancario_Async](https://github.com/karensantostech-art/Projeto_Bancario_Async)

  cd Projeto_Bancário_Async

3. ## 🛠️ Como Executar o Projeto

Siga os passos abaixo para configurar o ambiente e rodar a API localmente.

### 1. Instalação de Dependências

Este projeto utiliza o **Poetry** para gestão de pacotes e ambientes virtuais. Se você tiver o Poetry instalado, execute:

poetry install

Caso prefira usar o pip tradicional, certifique-se de ter um ambiente virtual ativo e instale as dependências necessárias:

pip install fastapi uvicorn sqlalchemy aiosqlite python-jose[cryptography] passlib[bcrypt]

### 2. Iniciação do Servidor

Para garantir que o servidor utilize as dependências instaladas no ambiente isolado do **Poetry**, utilize o comando abaixo na raiz do projeto:

poetry run uvicorn app.main:app --reload


### 3. Acesso a documentação:

[Swagger UI: http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
