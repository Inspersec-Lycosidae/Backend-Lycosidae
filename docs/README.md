# 📚 Documentação Backend-Lycosidae

## 📋 Índice da Documentação

### 🚀 **Para Desenvolvedores Frontend**
- **[📖 API Documentation](./API_DOCUMENTATION.md)** - Guia completo de todas as rotas da API
  - 38 endpoints documentados
  - Exemplos de implementação em JavaScript
  - Schemas de entrada e saída
  - Rate limiting e tratamento de erros

### 🏗️ **Para Desenvolvedores Backend**
- **[🔧 Arquitetura de Routers](./routers-architecture.md)** - Estrutura modular do sistema
  - Organização dos 8 módulos de routers
  - Guia de manutenção e extensão
  - Padrões de desenvolvimento

### 📁 **Estrutura da Documentação**

```
docs/
├── README.md                    # Este índice
├── API_DOCUMENTATION.md         # Documentação completa da API
├── routers-architecture.md      # Arquitetura modular dos routers
├── deployment/                  # Guias de deploy e produção
│   └── docker.md               # Deploy com Docker/Docker Compose
└── examples/                    # Exemplos práticos
    └── frontend-integration.md  # Integração com frontend
```

### 🚀 **Para Deploy e Produção**
- **[🐳 Deploy com Docker](./deployment/docker.md)** - Guia completo de containerização
  - Build e execução com Docker
  - Docker Compose para múltiplos serviços
  - Configurações de produção

### 💡 **Exemplos Práticos**
- **[🌐 Integração Frontend](./examples/frontend-integration.md)** - Exemplos de código
  - Configuração de cliente API
  - React hooks personalizados
  - Tratamento de rate limiting
  - Sistema de notificações

## 🎯 **Quick Start**

### **Para Frontend Developers**
1. Leia a [API Documentation](./API_DOCUMENTATION.md)
2. Configure a base URL: `http://localhost:8000`
3. Implemente as rotas conforme os exemplos fornecidos

### **Para Backend Developers**
1. Entenda a [Arquitetura de Routers](./routers-architecture.md)
2. Para adicionar novas funcionalidades, siga os padrões estabelecidos
3. Cada módulo tem responsabilidade única

## 🔗 **Links Importantes**

- **Base URL da API**: `http://localhost:8000`
- **Documentação Interativa**: `http://localhost:8000/docs` (quando debug=true)
- **Health Check**: `http://localhost:8000/system/health`
- **Rate Limit Info**: `http://localhost:8000/system/rate-limit/info`

## 📊 **Estatísticas do Projeto**

| Métrica | Valor |
|---------|-------|
| **Total de Rotas** | 38 endpoints |
| **Módulos de Router** | 8 arquivos |
| **Rate Limiters** | 37 configurados |
| **Schemas** | 15+ DTOs |
| **Linhas de Código** | ~2.5k (organizado) |

## 🛠️ **Tecnologias Utilizadas**

- **FastAPI** - Framework web moderno
- **Pydantic** - Validação de dados
- **JWT** - Autenticação
- **Rate Limiting** - Controle de tráfego
- **Logging** - Monitoramento

## 📞 **Suporte**

Para dúvidas sobre:
- **API Usage**: Consulte `API_DOCUMENTATION.md`
- **Arquitetura**: Consulte `routers-architecture.md`
- **Implementação**: Revise o código nos módulos `app/routers/`

---

**Última atualização**: Janeiro 2024  
**Versão da API**: 1.0.0
