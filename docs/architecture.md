# 🏗️ Arquitetura Backend-Lycosidae

## 📋 **Visão Geral**

O Backend-Lycosidae foi **completamente refatorado** seguindo princípios de **Clean Architecture** e boas práticas de desenvolvimento. A estrutura modular facilita manutenção, testes e escalabilidade.

## 📁 **Nova Estrutura de Pastas**

```
app/
├── 🏗️ core/                    # Núcleo da aplicação
│   ├── __init__.py
│   └── dependencies.py         # Dependency Injection
├── 🔐 security/                # Módulos de segurança
│   ├── __init__.py
│   ├── auth.py                 # JWT & Tokens
│   ├── password.py             # Hash & Validação de senhas
│   ├── validation.py           # Validações de entrada
│   └── utils.py                # IP, User-Agent, etc.
├── 📊 schemas/                 # Schemas organizados por entidade
│   ├── __init__.py
│   ├── user.py                 # User DTOs
│   ├── competition.py          # Competition DTOs
│   ├── exercise.py             # Exercise DTOs
│   ├── team.py                 # Team DTOs
│   ├── tag.py                  # Tag DTOs
│   ├── container.py            # Container DTOs
│   ├── relationships.py        # Relationship DTOs
│   └── system.py               # System DTOs
├── ⚠️ exceptions/              # Sistema de exceções
│   ├── __init__.py
│   ├── custom.py               # Exceções personalizadas
│   ├── handlers.py             # Exception handlers
│   ├── responses.py            # Respostas de erro
│   └── logger.py               # Logger de erros
├── 🛣️ routers/                 # Rotas modularizadas
│   ├── __init__.py
│   ├── users.py                # User endpoints
│   ├── competitions.py         # Competition endpoints
│   ├── exercises.py            # Exercise endpoints
│   ├── teams.py                # Team endpoints
│   ├── tags.py                 # Tag endpoints
│   ├── containers.py           # Container endpoints
│   ├── relationships.py        # Relationship endpoints
│   └── system.py               # System endpoints
├── config.py                   # Configurações
├── logger.py                   # Sistema de logs
├── middleware.py               # Middlewares customizados
├── rate_limiter.py             # Rate limiting
├── interpreter_client.py       # Cliente do interpretador
└── main.py                     # Aplicação principal
```

## 🔧 **Principais Melhorias Implementadas**

### 1. **🔐 Modularização de Segurança**

**Antes**: 1 arquivo de 268 linhas (`security.py`)  
**Depois**: 4 módulos especializados

- **`auth.py`**: JWT tokens, autenticação
- **`password.py`**: Hash, validação de senhas, tokens seguros  
- **`validation.py`**: Validações de entrada, sanitização
- **`utils.py`**: IP, User-Agent, rate limiting

### 2. **📊 Schemas por Entidade**

**Antes**: 1 arquivo de 178 linhas (`schemas.py`)  
**Depois**: 8 arquivos organizados por domínio

Cada entidade possui seu próprio arquivo com validações específicas.

### 3. **⚠️ Sistema de Exceções Robusto**

**Antes**: 1 arquivo de 280 linhas (`exceptions.py`)  
**Depois**: 4 módulos especializados

- **`custom.py`**: Exceções personalizadas por tipo
- **`handlers.py`**: Handlers para cada tipo de erro
- **`responses.py`**: Respostas padronizadas
- **`logger.py`**: Logging estruturado de erros

### 4. **🏗️ Dependency Injection**

Novo sistema centralizado de dependências:

```python
# Antes
@app.post("/route")
async def endpoint(request: Request):
    user = verify_token(request.headers.get("Authorization"))
    # ...

# Depois  
@app.post("/route")
async def endpoint(
    user: dict = Depends(get_current_user),
    client: InterpreterClient = Depends(get_interpreter_client)
):
    # ...
```

## 🚀 **Benefícios da Nova Arquitetura**

### ✅ **Organização**
- Arquivos menores (50-100 linhas cada)
- Responsabilidades claras
- Fácil localização de código

### ✅ **Manutenibilidade**  
- Mudanças isoladas por módulo
- Imports específicos
- Debugging simplificado

### ✅ **Testabilidade**
- Dependencies injetáveis
- Mocks mais fáceis
- Testes unitários isolados

### ✅ **Escalabilidade**
- Adição de funcionalidades sem afetar outras
- Estrutura preparada para crescimento
- Padrões enterprise-ready

## 🔍 **Como Usar as Novas Dependencies**

### **Autenticação Básica**
```python
from fastapi import Depends
from app.core.dependencies import get_current_user

@router.get("/profile")
async def get_profile(user: dict = Depends(get_current_user)):
    return {"user_id": user["user_id"], "username": user["username"]}
```

### **Autorização por Permissão**
```python
from app.core.dependencies import require_permission

@router.post("/admin-action")
async def admin_action(user: dict = Depends(require_permission("admin"))):
    # Apenas usuários com permissão "admin" acessam
    pass
```

### **Validação de Proprietário**
```python
from app.core.dependencies import require_owner_or_admin

@router.put("/teams/{team_id}")
async def update_team(
    team_data: dict,
    user: dict = Depends(require_owner_or_admin("creator_id"))
):
    # Apenas o criador do time ou admin pode modificar
    pass
```

### **Injeção de Serviços**
```python
from app.core.dependencies import get_interpreter_client, get_rate_limiter

@router.post("/data")
async def create_data(
    client: InterpreterClient = Depends(get_interpreter_client),
    rate_limiter: RateLimiter = Depends(get_rate_limiter)
):
    # Serviços injetados automaticamente
    pass
```

## 📈 **Comparação: Antes vs Depois**

| Aspecto | Antes | Depois |
|---------|-------|--------|
| **Arquivos Grandes** | 3 arquivos (268, 178, 280 linhas) | 20+ arquivos (50-100 linhas) |
| **Imports** | `from .security import SecurityUtils` | `from .security.auth import SecurityUtils` |
| **Dependencies** | Manual em cada rota | Sistema centralizado |
| **Testes** | Complexos, muitas dependências | Isolados, dependencies mockáveis |
| **Debugging** | Difícil localizar problemas | Módulos específicos |
| **Adição de Features** | Afeta arquivos grandes | Novos módulos independentes |

## 🧪 **Próximos Passos Recomendados**

### **Fase 1: Testes** ✅
- [x] Verificar sintaxe dos módulos
- [x] Validar imports
- [x] Testar endpoints básicos

### **Fase 2: Cache & Performance** 🔄
- [ ] Implementar Redis para cache
- [ ] Otimizar queries do interpretador
- [ ] Adicionar métricas Prometheus

### **Fase 3: Observabilidade** 📊
- [ ] Logs estruturados (structlog)
- [ ] Tracing distribuído
- [ ] Dashboard de monitoramento

### **Fase 4: Infraestrutura** 🐳
- [ ] Docker multi-stage builds
- [ ] CI/CD pipeline
- [ ] Deploy automatizado

## 🛡️ **Segurança Mantida**

Todas as práticas de segurança foram **preservadas e melhoradas**:

- ✅ Validação de entrada rigorosa
- ✅ Rate limiting por endpoint
- ✅ JWT com expiração
- ✅ Sanitização de dados
- ✅ Headers de segurança
- ✅ Logs de auditoria
- ✅ CORS configurado
- ✅ Middleware de segurança

## 📚 **Documentação Relacionada**

- [API Documentation](./API_DOCUMENTATION.md)
- [Routers Architecture](./routers-architecture.md)
- [Docker Deployment](./deployment/docker.md)
- [Frontend Integration](./examples/frontend-integration.md)

---

**Resultado**: Backend moderno, escalável e maintível! 🚀

> **Observação**: Esta refatoração mantém 100% da funcionalidade existente, apenas organizando melhor o código para facilitar desenvolvimento futuro.
