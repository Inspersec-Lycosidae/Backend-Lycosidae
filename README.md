# Backend-Lycosidae

API segura para o projeto Lycosidae com autenticação JWT, rate limiting e validações robustas.

## 🚀 Características

- **Autenticação JWT** com refresh tokens
- **Rate Limiting** configurável por endpoint
- **Validação robusta** de entrada com Pydantic
- **Sanitização** de dados de entrada
- **Headers de segurança** automáticos
- **Logging estruturado** com cores
- **Tratamento de erros** padronizado
- **CORS configurável**
- **Documentação automática** com Swagger

## 📋 Pré-requisitos

- Python 3.8+
- Interpretador do Lycosidae (serviço separado)
- Redis (opcional, para cache)

## 🛠️ Instalação

1. **Clone o repositório**
```bash
git clone <repository-url>
cd Backend-Lycosidae
```

2. **Crie um ambiente virtual**
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate  # Windows
```

3. **Instale as dependências**
```bash
pip install -r requirements.txt
```

4. **Configure as variáveis de ambiente**
```bash
cp .env.example .env
# Edite o arquivo .env com suas configurações
```

## ⚙️ Configuração

Crie um arquivo `.env` baseado no `.env.example`:

```env
# Configurações do Interpretador
INTERPRETER_URL=http://localhost:8001

# Configurações JWT
JWT_SECRET=your-super-secret-jwt-key-here-change-this-in-production
JWT_EXPIRATION=3600
JWT_ALGORITHM=HS256

# Configurações de Segurança
SECRET_KEY=your-super-secret-key-here-change-this-in-production
ALLOWED_HOSTS=localhost,127.0.0.1,0.0.0.0
CORS_ORIGINS=http://localhost:3000,http://127.0.0.1:3000

# Configurações de Rate Limiting
RATE_LIMIT_REQUESTS=100
RATE_LIMIT_WINDOW=60

# Configurações de Log
LOG_LEVEL=INFO
```

## 🚀 Execução

### Desenvolvimento
```bash
python -m app.main
```

### Produção
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

### Com Docker
```bash
docker build -t backend-lycosidae .
docker run -p 8000:8000 --env-file .env backend-lycosidae
```

## 📚 Documentação

### 📖 **Documentação Completa**
Toda a documentação está organizada na pasta [`docs/`](./docs/):

- **[📋 Índice Geral](./docs/README.md)** - Visão geral de toda documentação
- **[🔗 API Documentation](./docs/API_DOCUMENTATION.md)** - Guia completo da API para frontend
- **[🏗️ Arquitetura de Routers](./docs/routers-architecture.md)** - Estrutura modular do backend

### 🌐 **Documentação Interativa**
Após iniciar o servidor, acesse:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **OpenAPI JSON**: http://localhost:8000/openapi.json

## 🔐 Endpoints Principais

### 🏠 Sistema
- `GET /` - Root endpoint
- `GET /system/health` - Health check
- `GET /system/rate-limit/info` - Informações de rate limiting

### 👤 Usuários
- `POST /route/register` - Registro de usuário

### 🏆 Competições
- `POST /route/competitions` - Criar competição
- `GET /route/competitions/{id}` - Buscar competição
- `GET /route/competitions/invite/{code}` - Buscar por convite

### 💪 Exercícios
- `POST /route/exercises` - Criar exercício
- `GET /route/exercises/{id}` - Buscar exercício

### 🏷️ Tags & 👥 Times & 🐳 Containers
- Endpoints CRUD completos para cada entidade
- Relacionamentos entre entidades

> **📖 Para documentação completa de todos os 38 endpoints, consulte [`docs/API_DOCUMENTATION.md`](./docs/API_DOCUMENTATION.md)**

## 🔒 Segurança

### Rate Limiting
- Endpoints de autenticação têm limites mais restritivos
- Headers `X-RateLimit-*` informam o status atual
- Limites configuráveis por endpoint

### Validação de Entrada
- Validação robusta com Pydantic
- Sanitização automática de dados
- Validação de força de senha
- Verificação de domínios de email

### Headers de Segurança
- `X-Content-Type-Options: nosniff`
- `X-Frame-Options: DENY`
- `X-XSS-Protection: 1; mode=block`
- `Referrer-Policy: strict-origin-when-cross-origin`

## 🧪 Testes

```bash
# Instalar dependências de teste
pip install pytest pytest-asyncio httpx

# Executar testes
pytest
```

## 📊 Monitoramento

### Logs
- Logs estruturados com cores
- Diferentes níveis de log configuráveis
- Logs de segurança e auditoria

### Métricas
- Tempo de processamento das requisições
- Rate limiting status
- Status de saúde dos serviços

## 🚨 Troubleshooting

### Erro de configuração
```
Configuration validation failed: Missing or invalid critical settings
```
**Solução**: Verifique se todas as variáveis obrigatórias estão definidas no `.env`

### Erro de interpretador
```
Interpreter connection test failed
```
**Solução**: Verifique se o interpretador está rodando e se a `INTERPRETER_URL` está correta

### Rate limit excedido
```
Rate limit exceeded
```
**Solução**: Aguarde o tempo de reset ou ajuste os limites no `.env`

 uma issue no repositório ou entre em contato com a equipe de desenvolvimento.
