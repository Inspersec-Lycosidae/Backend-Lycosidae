# 🌐 Exemplos de Integração Frontend

## 🚀 Quick Start para Frontend

### 1. Configuração Base

```javascript
// config/api.js
const API_CONFIG = {
  baseURL: 'http://localhost:8000',
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json'
  }
};

class ApiClient {
  constructor() {
    this.baseURL = API_CONFIG.baseURL;
  }

  async request(endpoint, options = {}) {
    const url = `${this.baseURL}${endpoint}`;
    const response = await fetch(url, {
      ...API_CONFIG,
      ...options
    });

    if (!response.ok) {
      throw new Error(`HTTP ${response.status}: ${response.statusText}`);
    }

    return response.json();
  }
}

export const apiClient = new ApiClient();
```

### 2. Registro de Usuário

```javascript
// services/auth.js
import { apiClient } from '../config/api.js';

export const registerUser = async (userData) => {
  try {
    const response = await apiClient.request('/route/register', {
      method: 'POST',
      body: JSON.stringify({
        username: userData.username,
        email: userData.email,
        password: userData.password,
        phone_number: userData.phone || null
      })
    });

    console.log('Usuário registrado:', response);
    return response;
  } catch (error) {
    console.error('Erro no registro:', error);
    throw error;
  }
};

// Exemplo de uso
const handleRegister = async (formData) => {
  try {
    const user = await registerUser(formData);
    alert('Registro realizado com sucesso!');
    // Redirecionar para dashboard
    window.location.href = '/dashboard';
  } catch (error) {
    alert('Erro no registro: ' + error.message);
  }
};
```

### 3. Gestão de Competições

```javascript
// services/competitions.js
import { apiClient } from '../config/api.js';

export const competitionService = {
  // Criar competição
  async create(competitionData) {
    return apiClient.request('/route/competitions', {
      method: 'POST',
      body: JSON.stringify(competitionData)
    });
  },

  // Buscar competição
  async getById(id) {
    return apiClient.request(`/route/competitions/${id}`);
  },

  // Buscar por código de convite
  async getByInvite(code) {
    return apiClient.request(`/route/competitions/invite/${code}`);
  },

  // Atualizar competição
  async update(id, data) {
    return apiClient.request(`/route/competitions/${id}`, {
      method: 'PUT',
      body: JSON.stringify(data)
    });
  },

  // Deletar competição
  async delete(id) {
    return apiClient.request(`/route/competitions/${id}`, {
      method: 'DELETE'
    });
  }
};
```

### 4. React Hooks Personalizados

```javascript
// hooks/useApi.js
import { useState, useEffect } from 'react';

export const useApi = (apiCall, dependencies = []) => {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchData = async () => {
      try {
        setLoading(true);
        setError(null);
        const result = await apiCall();
        setData(result);
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, dependencies);

  return { data, loading, error };
};

// hooks/useCompetitions.js
import { useApi } from './useApi';
import { competitionService } from '../services/competitions';

export const useCompetition = (id) => {
  return useApi(() => competitionService.getById(id), [id]);
};

// Exemplo de uso em componente
const CompetitionDetails = ({ competitionId }) => {
  const { data: competition, loading, error } = useCompetition(competitionId);

  if (loading) return <div>Carregando...</div>;
  if (error) return <div>Erro: {error}</div>;

  return (
    <div>
      <h1>{competition.name}</h1>
      <p>Organizador: {competition.organizer}</p>
      <p>Código: {competition.invite_code}</p>
    </div>
  );
};
```

### 5. Tratamento de Rate Limiting

```javascript
// utils/rateLimiting.js
class RateLimitHandler {
  constructor() {
    this.retryAfter = 0;
  }

  async handleRequest(requestFn) {
    try {
      const response = await requestFn();
      
      // Verificar headers de rate limit
      const remaining = response.headers.get('X-RateLimit-Remaining');
      if (remaining && parseInt(remaining) < 5) {
        console.warn('⚠️ Próximo do limite de rate limit');
        this.showRateLimitWarning();
      }

      return response;
    } catch (error) {
      if (error.status === 429) {
        const retryAfter = error.headers.get('Retry-After');
        this.retryAfter = parseInt(retryAfter) || 60;
        this.handleRateLimit();
        throw new Error(`Rate limit excedido. Tente novamente em ${this.retryAfter}s`);
      }
      throw error;
    }
  }

  showRateLimitWarning() {
    // Mostrar notificação de aviso
    console.warn('Você está próximo do limite de requisições');
  }

  handleRateLimit() {
    // Implementar backoff ou retry automático
    console.error(`Rate limit atingido. Retry em ${this.retryAfter}s`);
  }
}

export const rateLimitHandler = new RateLimitHandler();
```

### 6. Sistema de Notificações

```javascript
// utils/notifications.js
class NotificationSystem {
  show(message, type = 'info', duration = 5000) {
    const notification = this.createElement(message, type);
    document.body.appendChild(notification);
    
    setTimeout(() => {
      this.remove(notification);
    }, duration);
  }

  createElement(message, type) {
    const div = document.createElement('div');
    div.className = `notification notification-${type}`;
    div.innerHTML = `
      <span>${message}</span>
      <button onclick="this.parentElement.remove()">×</button>
    `;
    return div;
  }

  remove(element) {
    if (element.parentElement) {
      element.parentElement.removeChild(element);
    }
  }

  success(message) { this.show(message, 'success'); }
  error(message) { this.show(message, 'error'); }
  warning(message) { this.show(message, 'warning'); }
  info(message) { this.show(message, 'info'); }
}

export const notifications = new NotificationSystem();
```

### 7. Formulário de Registro Completo

```javascript
// components/RegisterForm.js
import { useState } from 'react';
import { registerUser } from '../services/auth';
import { notifications } from '../utils/notifications';

const RegisterForm = () => {
  const [formData, setFormData] = useState({
    username: '',
    email: '',
    password: '',
    phone: ''
  });
  const [loading, setLoading] = useState(false);

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);

    try {
      await registerUser(formData);
      notifications.success('Registro realizado com sucesso!');
      // Redirecionar ou limpar formulário
    } catch (error) {
      notifications.error(`Erro no registro: ${error.message}`);
    } finally {
      setLoading(false);
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <input
        type="text"
        name="username"
        placeholder="Username"
        value={formData.username}
        onChange={handleChange}
        required
      />
      <input
        type="email"
        name="email"
        placeholder="Email"
        value={formData.email}
        onChange={handleChange}
        required
      />
      <input
        type="password"
        name="password"
        placeholder="Password"
        value={formData.password}
        onChange={handleChange}
        required
      />
      <input
        type="tel"
        name="phone"
        placeholder="Telefone (opcional)"
        value={formData.phone}
        onChange={handleChange}
      />
      <button type="submit" disabled={loading}>
        {loading ? 'Registrando...' : 'Registrar'}
      </button>
    </form>
  );
};

export default RegisterForm;
```

## 🎨 Estilização CSS

```css
/* styles/notifications.css */
.notification {
  position: fixed;
  top: 20px;
  right: 20px;
  padding: 15px 20px;
  border-radius: 5px;
  color: white;
  font-weight: 500;
  z-index: 1000;
  min-width: 300px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.notification-success { background-color: #4caf50; }
.notification-error { background-color: #f44336; }
.notification-warning { background-color: #ff9800; }
.notification-info { background-color: #2196f3; }

.notification button {
  background: none;
  border: none;
  color: white;
  font-size: 18px;
  cursor: pointer;
  margin-left: 10px;
}
```

Estes exemplos fornecem uma base sólida para integrar qualquer frontend com a API Backend-Lycosidae!
