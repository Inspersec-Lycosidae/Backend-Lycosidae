# Lycosidae Backend API (Gateway)

O **Lycosidae Backend** atua como o **API Gateway** central da plataforma Lycosidae CTF. Ele é o ponto de entrada único para o Frontend, sendo responsável pela orquestração de serviços, validação de regras de negócio complexas e garantia da segurança via autenticação robusta.

Diferente de sistemas monolíticos, este serviço foi projetado para ser leve e focado em lógica, delegando a persistência de dados ao microserviço **Interpreter** através de comunicações assíncronas de alta performance.

## 🚀 Responsabilidades Principais

* **API Gateway**: Centraliza todas as rotas de sistema, desde gestão de usuários até o controle de competições.
* **Segurança e Autenticação**: Implementa o fluxo de segurança, controlando o acesso e expiração de sessões.
* **Orquestração de Negócio**: Valida permissões e estados de competições antes de processar submissões ou criar recursos.
* **Integração de Microserviços**: Utiliza um cliente HTTP assíncrono especializado para se comunicar com o **Interpreter** e o **Orchester**.

## 🛠️ Stack Tecnológica

* **Framework**: [FastAPI](https://fastapi.tiangolo.com/).
* **Comunicação Assíncrona**: [HTTPX](https://www.python-httpx.org/) (Cliente HTTP para integração entre microserviços).
* **Containerização**: Docker e Docker Compose.

## 🏗️ Arquitetura de Gateway

O Backend utiliza o padrão **Gateway**, onde:

1. Recebe a requisição do Frontend (TypeScript/Next.js).
2. Valida o a sessão e as permissões do usuário.
3. Processa a regra de negócio.
4. Realiza chamadas assíncronas ao `Interpreter-Lycosidae` para consultar ou salvar dados.
5. Retorna a resposta tratada ao cliente.

## 📦 Como Executar

### Via Docker (Recomendado)

O backend deve ser iniciado preferencialmente através do repositório principal de orquestração:

```bash
docker-compose up -d backend

```

O serviço será exposto na porta **8082** do host por padrão.

### Desenvolvimento Local

1. Instale as dependências:
```bash
pip install -r requirements.txt

```


2. Inicie o servidor em modo de recarregamento automático:
```bash
./uvicorn.sh

```

## 📖 Documentação da API

Uma vez que o serviço esteja rodando, você pode acessar a documentação interativa (Swagger UI) fornecida pelo FastAPI no endpoint:

* **URL**: `http://localhost:8082/docs`

## 🛡️ Licença

Este projeto está licenciado sob os termos da licença incluída no arquivo `LICENSE`.