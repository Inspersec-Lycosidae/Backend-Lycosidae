# 🐳 Deploy com Docker

## 📋 Pré-requisitos

- Docker instalado
- Docker Compose (opcional)
- Arquivo `.env` configurado

## 🚀 Build da Imagem

```bash
# Build simples
docker build -t backend-lycosidae .

# Build com tag específica
docker build -t backend-lycosidae:v1.0.0 .
```

## ▶️ Execução

### Execução Simples
```bash
docker run -p 8000:8000 --env-file .env backend-lycosidae
```

### Execução com Volume
```bash
docker run -p 8000:8000 \
  --env-file .env \
  -v $(pwd)/logs:/app/logs \
  backend-lycosidae
```

## 🐙 Docker Compose

### Arquivo `docker-compose.yml`
```yaml
version: '3.8'

services:
  backend:
    build: .
    ports:
      - "8000:8000"
    environment:
      - DEBUG=false
      - JWT_SECRET=${JWT_SECRET}
      - SECRET_KEY=${SECRET_KEY}
      - INTERPRETER_URL=http://interpreter:8001
    depends_on:
      - interpreter
    volumes:
      - ./logs:/app/logs
    restart: unless-stopped

  interpreter:
    image: lycosidae-interpreter:latest
    ports:
      - "8001:8001"
    restart: unless-stopped

  redis:
    image: redis:alpine
    ports:
      - "6379:6379"
    restart: unless-stopped
```

### Execução com Compose
```bash
# Subir todos os serviços
docker-compose up -d

# Ver logs
docker-compose logs -f backend

# Parar serviços
docker-compose down
```

## 🔧 Configurações Específicas do Docker

### Variáveis de Ambiente
```env
# .env para Docker
DEBUG=false
LOG_LEVEL=INFO
INTERPRETER_URL=http://interpreter:8001
REDIS_URL=redis://redis:6379
```

### Health Check
```dockerfile
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:8000/system/health || exit 1
```

## 📊 Monitoramento

### Logs
```bash
# Ver logs em tempo real
docker logs -f backend-lycosidae

# Últimas 100 linhas
docker logs --tail 100 backend-lycosidae
```

### Métricas
```bash
# Status dos containers
docker ps

# Uso de recursos
docker stats backend-lycosidae
```

## 🚨 Troubleshooting

### Problema: Container não inicia
```bash
# Verificar logs
docker logs backend-lycosidae

# Executar em modo interativo
docker run -it --entrypoint /bin/bash backend-lycosidae
```

### Problema: Não consegue conectar no interpretador
- Verificar se o serviço interpreter está rodando
- Verificar a rede Docker
- Confirmar a URL no `.env`

## 🔐 Produção

### Configurações de Segurança
```bash
# Executar como usuário não-root
docker run --user 1000:1000 backend-lycosidae

# Limitar recursos
docker run --memory=512m --cpus=1 backend-lycosidae
```

### Backup
```bash
# Backup de logs
docker cp backend-lycosidae:/app/logs ./backup-logs

# Backup de configurações
cp .env backup.env
```
