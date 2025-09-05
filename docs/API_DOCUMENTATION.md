# 📚 Backend-Lycosidae API Documentation

## 🌐 Informações Gerais

**Base URL:** `http://localhost:8000`

**Prefixo das Rotas:** `/route` (exceto sistema)

**Rate Limiting:** Implementado em todas as rotas

**Autenticação:** JWT (recomendado implementar)

---

## 📖 Índice de Rotas

### 🏠 [Sistema](#sistema)
- [GET /](#get-) - Root endpoint
- [GET /system/health](#get-systemhealth) - Health check
- [GET /system/rate-limit/info](#get-systemrate-limitinfo) - Rate limit info

### 👤 [Usuários](#usuários)
- [POST /route/register](#post-routeregister) - Registro de usuário

### 🏆 [Competições](#competições)
- [POST /route/competitions](#post-routecompetitions) - Criar competição
- [GET /route/competitions/{id}](#get-routecompetitionsid) - Buscar competição
- [PUT /route/competitions/{id}](#put-routecompetitionsid) - Atualizar competição
- [DELETE /route/competitions/{id}](#delete-routecompetitionsid) - Deletar competição
- [GET /route/competitions/invite/{code}](#get-routecompetitionsinvitecode) - Buscar por convite

### 💪 [Exercícios](#exercícios)
- [POST /route/exercises](#post-routeexercises) - Criar exercício
- [GET /route/exercises/{id}](#get-routeexercisesid) - Buscar exercício
- [PUT /route/exercises/{id}](#put-routeexercisesid) - Atualizar exercício
- [DELETE /route/exercises/{id}](#delete-routeexercisesid) - Deletar exercício

### 🏷️ [Tags](#tags)
- [POST /route/tags](#post-routetags) - Criar tag
- [GET /route/tags/{id}](#get-routetagsid) - Buscar tag
- [PUT /route/tags/{id}](#put-routetagsid) - Atualizar tag
- [DELETE /route/tags/{id}](#delete-routetagsid) - Deletar tag
- [GET /route/tags/type/{type}](#get-routetagstypetype) - Buscar por tipo

### 👥 [Times](#times)
- [POST /route/teams](#post-routeteams) - Criar time
- [GET /route/teams/{id}](#get-routeteamsid) - Buscar time
- [PUT /route/teams/{id}](#put-routeteamsid) - Atualizar time
- [DELETE /route/teams/{id}](#delete-routeteamsid) - Deletar time

### 🐳 [Containers](#containers)
- [POST /route/containers](#post-routecontainers) - Criar container
- [GET /route/containers/{id}](#get-routecontainersid) - Buscar container
- [PUT /route/containers/{id}](#put-routecontainersid) - Atualizar container
- [DELETE /route/containers/{id}](#delete-routecontainersid) - Deletar container

### 🔗 [Relacionamentos](#relacionamentos)
- [Usuário-Competição](#usuário-competição)
- [Usuário-Time](#usuário-time)
- [Time-Competição](#time-competição)
- [Exercício-Tag](#exercício-tag)
- [Exercício-Competição](#exercício-competição)
- [Container-Competição](#container-competição)

---

## 🏠 Sistema

### GET /

**Descrição:** Endpoint raiz da API

**Rate Limit:** 100 requests/minuto

**Resposta:**
```json
{
  "message": "Backend-Lycosidae API is running"
}
```

**Implementação Frontend:**
```javascript
const checkAPI = async () => {
  try {
    const response = await fetch('http://localhost:8000/');
    const data = await response.json();
    console.log(data.message);
  } catch (error) {
    console.error('API indisponível:', error);
  }
};
```

### GET /system/health

**Descrição:** Verifica status de saúde da API e serviços

**Rate Limit:** 60 requests/minuto

**Resposta:**
```json
{
  "status": "healthy",
  "message": "Backend is running properly",
  "service": "Backend-Lycosidae",
  "timestamp": "2024-01-01T12:00:00Z",
  "version": "1.0.0",
  "database_status": "success"
}
```

**Implementação Frontend:**
```javascript
const healthCheck = async () => {
  try {
    const response = await fetch('http://localhost:8000/system/health');
    const health = await response.json();
    
    // Atualizar indicador de status na UI
    const statusIndicator = document.getElementById('api-status');
    statusIndicator.className = health.status === 'healthy' ? 'status-ok' : 'status-error';
    statusIndicator.textContent = health.message;
  } catch (error) {
    console.error('Health check failed:', error);
  }
};
```

### GET /system/rate-limit/info

**Descrição:** Informações sobre rate limiting

**Resposta:**
```json
{
  "limit": 100,
  "remaining": 95,
  "reset_time": 1640995200,
  "retry_after": 45
}
```

---

## 👤 Usuários

### POST /route/register

**Descrição:** Registra um novo usuário

**Rate Limit:** 5 requests/minuto

**Payload:**
```json
{
  "username": "usuario123",
  "email": "usuario@gmail.com",
  "password": "MinhaSenh@123",
  "phone_number": "+5511999999999"
}
```

**Validações:**
- **Username:** 3-50 chars, apenas letras, números, _ e -
- **Email:** Formato válido, domínios permitidos
- **Password:** Mín. 8 chars, maiúscula, minúscula, número, especial
- **Phone:** Opcional, formato internacional

**Resposta (201):**
```json
{
  "id": "user_123",
  "username": "usuario123",
  "email": "usuario@gmail.com",
  "phone_number": "+5511999999999"
}
```

**Implementação Frontend:**
```javascript
const registerUser = async (userData) => {
  try {
    const response = await fetch('http://localhost:8000/route/register', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(userData)
    });

    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.message || 'Erro no registro');
    }

    const user = await response.json();
    
    // Salvar dados do usuário
    localStorage.setItem('user', JSON.stringify(user));
    
    // Redirecionar para dashboard
    window.location.href = '/dashboard';
    
    return user;
  } catch (error) {
    console.error('Erro no registro:', error);
    
    // Mostrar erro na UI
    const errorDiv = document.getElementById('registration-error');
    errorDiv.textContent = error.message;
    errorDiv.style.display = 'block';
  }
};

// Exemplo de uso com formulário
document.getElementById('register-form').addEventListener('submit', async (e) => {
  e.preventDefault();
  
  const formData = new FormData(e.target);
  const userData = {
    username: formData.get('username'),
    email: formData.get('email'),
    password: formData.get('password'),
    phone_number: formData.get('phone') || null
  };
  
  await registerUser(userData);
});
```

---

## 🏆 Competições

### POST /route/competitions

**Descrição:** Cria uma nova competição

**Rate Limit:** 10 requests/minuto

**Payload:**
```json
{
  "name": "CTF 2024",
  "organizer": "Insper",
  "invite_code": "CTF2024",
  "start_date": "2024-06-01T08:00:00Z",
  "end_date": "2024-06-02T18:00:00Z"
}
```

**Resposta (201):**
```json
{
  "id": "comp_123",
  "name": "CTF 2024",
  "organizer": "Insper", 
  "invite_code": "CTF2024",
  "start_date": "2024-06-01T08:00:00Z",
  "end_date": "2024-06-02T18:00:00Z"
}
```

**Implementação Frontend:**
```javascript
const createCompetition = async (competitionData) => {
  try {
    const response = await fetch('http://localhost:8000/route/competitions', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        // 'Authorization': `Bearer ${getAuthToken()}` // Quando implementar JWT
      },
      body: JSON.stringify(competitionData)
    });

    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.message);
    }

    const competition = await response.json();
    
    // Adicionar à lista de competições
    addCompetitionToUI(competition);
    
    // Fechar modal/formulário
    closeCreateCompetitionModal();
    
    return competition;
  } catch (error) {
    showNotification('Erro ao criar competição: ' + error.message, 'error');
  }
};
```

### GET /route/competitions/{competition_id}

**Descrição:** Busca competição por ID

**Rate Limit:** 60 requests/minuto

**Resposta (200):**
```json
{
  "id": "comp_123",
  "name": "CTF 2024",
  "organizer": "Insper",
  "invite_code": "CTF2024", 
  "start_date": "2024-06-01T08:00:00Z",
  "end_date": "2024-06-02T18:00:00Z"
}
```

**Implementação Frontend:**
```javascript
const getCompetition = async (competitionId) => {
  try {
    const response = await fetch(`http://localhost:8000/route/competitions/${competitionId}`);
    
    if (!response.ok) {
      throw new Error('Competição não encontrada');
    }
    
    const competition = await response.json();
    
    // Preencher dados na página de competição
    document.getElementById('comp-name').textContent = competition.name;
    document.getElementById('comp-organizer').textContent = competition.organizer;
    document.getElementById('comp-dates').textContent = 
      `${formatDate(competition.start_date)} - ${formatDate(competition.end_date)}`;
    
    return competition;
  } catch (error) {
    console.error('Erro ao buscar competição:', error);
    showNotification('Competição não encontrada', 'error');
  }
};
```

### PUT /route/competitions/{competition_id}

**Descrição:** Atualiza uma competição

**Rate Limit:** 20 requests/minuto

**Payload:** Mesmo formato do POST

**Resposta (200):**
```json
{
  "message": "Competition updated successfully"
}
```

### DELETE /route/competitions/{competition_id}

**Descrição:** Deleta uma competição

**Rate Limit:** 10 requests/minuto

**Resposta (200):**
```json
{
  "message": "Competition deleted successfully"
}
```

**Implementação Frontend:**
```javascript
const deleteCompetition = async (competitionId) => {
  if (!confirm('Tem certeza que deseja deletar esta competição?')) {
    return;
  }
  
  try {
    const response = await fetch(`http://localhost:8000/route/competitions/${competitionId}`, {
      method: 'DELETE'
    });
    
    if (!response.ok) {
      throw new Error('Erro ao deletar competição');
    }
    
    // Remover da UI
    document.getElementById(`competition-${competitionId}`).remove();
    
    showNotification('Competição deletada com sucesso', 'success');
  } catch (error) {
    showNotification('Erro ao deletar: ' + error.message, 'error');
  }
};
```

### GET /route/competitions/invite/{invite_code}

**Descrição:** Busca competição por código de convite

**Rate Limit:** 60 requests/minuto

**Implementação Frontend:**
```javascript
const joinCompetitionByCode = async (inviteCode) => {
  try {
    const response = await fetch(`http://localhost:8000/route/competitions/invite/${inviteCode}`);
    
    if (!response.ok) {
      throw new Error('Código de convite inválido');
    }
    
    const competition = await response.json();
    
    // Mostrar modal de confirmação para entrar
    showJoinCompetitionModal(competition);
    
    return competition;
  } catch (error) {
    showNotification('Código inválido: ' + error.message, 'error');
  }
};
```

---

## 💪 Exercícios

### POST /route/exercises

**Descrição:** Cria um novo exercício

**Rate Limit:** 10 requests/minuto

**Payload:**
```json
{
  "link": "https://example.com/challenge",
  "name": "Buffer Overflow Básico",
  "score": 100,
  "difficulty": "Easy",
  "port": 8080
}
```

**Resposta (201):**
```json
{
  "id": "ex_123",
  "link": "https://example.com/challenge",
  "name": "Buffer Overflow Básico",
  "score": 100,
  "difficulty": "Easy",
  "port": 8080
}
```

**Implementação Frontend:**
```javascript
const createExercise = async (exerciseData) => {
  try {
    const response = await fetch('http://localhost:8000/route/exercises', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(exerciseData)
    });

    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.message);
    }

    const exercise = await response.json();
    
    // Adicionar à lista de exercícios
    addExerciseCard(exercise);
    
    return exercise;
  } catch (error) {
    showNotification('Erro ao criar exercício: ' + error.message, 'error');
  }
};

// Helper para criar card do exercício
const addExerciseCard = (exercise) => {
  const exercisesList = document.getElementById('exercises-list');
  const card = document.createElement('div');
  card.className = 'exercise-card';
  card.innerHTML = `
    <div class="exercise-header">
      <h3>${exercise.name}</h3>
      <span class="difficulty ${exercise.difficulty.toLowerCase()}">${exercise.difficulty}</span>
    </div>
    <div class="exercise-body">
      <p>Pontuação: ${exercise.score}</p>
      <p>Porta: ${exercise.port}</p>
      <a href="${exercise.link}" target="_blank" class="exercise-link">Acessar Exercício</a>
    </div>
  `;
  exercisesList.appendChild(card);
};
```

### GET /route/exercises/{exercise_id}

**Implementação Frontend:**
```javascript
const getExercise = async (exerciseId) => {
  try {
    const response = await fetch(`http://localhost:8000/route/exercises/${exerciseId}`);
    
    if (!response.ok) {
      throw new Error('Exercício não encontrado');
    }
    
    const exercise = await response.json();
    
    // Preencher página do exercício
    document.getElementById('exercise-title').textContent = exercise.name;
    document.getElementById('exercise-difficulty').textContent = exercise.difficulty;
    document.getElementById('exercise-score').textContent = exercise.score;
    document.getElementById('exercise-link').href = exercise.link;
    
    return exercise;
  } catch (error) {
    showNotification('Exercício não encontrado', 'error');
  }
};
```

---

## 🏷️ Tags

### POST /route/tags

**Payload:**
```json
{
  "type": "Web Security"
}
```

**Implementação Frontend:**
```javascript
const createTag = async (tagData) => {
  try {
    const response = await fetch('http://localhost:8000/route/tags', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(tagData)
    });

    const tag = await response.json();
    
    // Adicionar à lista de tags disponíveis
    addTagToSelector(tag);
    
    return tag;
  } catch (error) {
    console.error('Erro ao criar tag:', error);
  }
};
```

---

## 👥 Times

### POST /route/teams

**Payload:**
```json
{
  "name": "Team Alpha",
  "competition": "CTF 2024",
  "creator": "user_123",
  "score": 0
}
```

**Implementação Frontend:**
```javascript
const createTeam = async (teamData) => {
  try {
    const response = await fetch('http://localhost:8000/route/teams', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(teamData)
    });

    const team = await response.json();
    
    // Redirecionar para página do time
    window.location.href = `/teams/${team.id}`;
    
    return team;
  } catch (error) {
    showNotification('Erro ao criar time: ' + error.message, 'error');
  }
};
```

---

## 🐳 Containers

### POST /route/containers

**Payload:**
```json
{
  "deadline": "2024-12-31T23:59:59Z"
}
```

---

## 🔗 Relacionamentos

### Usuário-Competição

**POST /route/user-competitions**
```json
{
  "user_id": "user_123",
  "competition_id": "comp_456"
}
```

**Implementação:**
```javascript
const joinCompetition = async (userId, competitionId) => {
  try {
    const response = await fetch('http://localhost:8000/route/user-competitions', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        user_id: userId,
        competition_id: competitionId
      })
    });

    if (response.ok) {
      showNotification('Inscrição realizada com sucesso!', 'success');
      updateUserCompetitions();
    }
  } catch (error) {
    showNotification('Erro na inscrição', 'error');
  }
};
```

### Usuário-Time

**POST /route/user-teams**
```json
{
  "user_id": "user_123", 
  "team_id": "team_456"
}
```

### Time-Competição

**POST /route/team-competitions**
```json
{
  "team_id": "team_123",
  "competition_id": "comp_456"
}
```

### Exercício-Tag

**POST /route/exercise-tags**
```json
{
  "exercise_id": "ex_123",
  "tag_id": "tag_456"
}
```

### Exercício-Competição

**POST /route/exercise-competitions**
```json
{
  "exercise_id": "ex_123",
  "competition_id": "comp_456"
}
```

### Container-Competição

**POST /route/container-competitions**
```json
{
  "container_id": "cont_123",
  "competition_id": "comp_456"
}
```

---

## 🛠️ Implementação Geral Frontend

### Configuração Base

```javascript
// config/api.js
const API_BASE_URL = 'http://localhost:8000';

class APIClient {
  constructor() {
    this.baseURL = API_BASE_URL;
  }

  async request(endpoint, options = {}) {
    const url = `${this.baseURL}${endpoint}`;
    
    const config = {
      headers: {
        'Content-Type': 'application/json',
        ...options.headers
      },
      ...options
    };

    try {
      const response = await fetch(url, config);
      
      // Verificar rate limiting
      const rateLimitRemaining = response.headers.get('X-RateLimit-Remaining');
      if (rateLimitRemaining && parseInt(rateLimitRemaining) < 5) {
        this.showRateLimitWarning();
      }
      
      if (!response.ok) {
        const error = await response.json();
        throw new Error(error.message || `HTTP ${response.status}`);
      }
      
      return await response.json();
    } catch (error) {
      console.error('API Error:', error);
      this.handleError(error);
      throw error;
    }
  }

  showRateLimitWarning() {
    showNotification('Você está próximo do limite de requisições', 'warning');
  }

  handleError(error) {
    // Log erro, mostrar notificação, etc.
    showNotification(`Erro: ${error.message}`, 'error');
  }
}

const apiClient = new APIClient();
```

### Sistema de Notificações

```javascript
// utils/notifications.js
const showNotification = (message, type = 'info') => {
  const notification = document.createElement('div');
  notification.className = `notification notification-${type}`;
  notification.textContent = message;
  
  document.body.appendChild(notification);
  
  // Auto remover após 5 segundos
  setTimeout(() => {
    notification.remove();
  }, 5000);
};
```

### Gerenciamento de Estado

```javascript
// store/app.js
class AppStore {
  constructor() {
    this.user = null;
    this.competitions = [];
    this.exercises = [];
    this.teams = [];
  }

  setUser(user) {
    this.user = user;
    localStorage.setItem('user', JSON.stringify(user));
  }

  getUser() {
    if (!this.user) {
      const stored = localStorage.getItem('user');
      this.user = stored ? JSON.parse(stored) : null;
    }
    return this.user;
  }

  addCompetition(competition) {
    this.competitions.push(competition);
    this.renderCompetitions();
  }

  renderCompetitions() {
    const container = document.getElementById('competitions-list');
    if (!container) return;
    
    container.innerHTML = '';
    this.competitions.forEach(comp => {
      const card = this.createCompetitionCard(comp);
      container.appendChild(card);
    });
  }

  createCompetitionCard(competition) {
    const card = document.createElement('div');
    card.className = 'competition-card';
    card.innerHTML = `
      <h3>${competition.name}</h3>
      <p>Organizador: ${competition.organizer}</p>
      <p>Código: ${competition.invite_code}</p>
      <div class="competition-dates">
        <span>Início: ${formatDate(competition.start_date)}</span>
        <span>Fim: ${formatDate(competition.end_date)}</span>
      </div>
      <div class="competition-actions">
        <button onclick="joinCompetition('${competition.id}')">Participar</button>
        <button onclick="viewCompetition('${competition.id}')">Ver Detalhes</button>
      </div>
    `;
    return card;
  }
}

const appStore = new AppStore();
```

### Utilitários

```javascript
// utils/helpers.js
const formatDate = (dateString) => {
  return new Date(dateString).toLocaleDateString('pt-BR', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit'
  });
};

const validateForm = (formData, rules) => {
  const errors = {};
  
  for (const [field, value] of Object.entries(formData)) {
    const rule = rules[field];
    if (!rule) continue;
    
    if (rule.required && (!value || value.trim() === '')) {
      errors[field] = `${field} é obrigatório`;
    }
    
    if (rule.minLength && value.length < rule.minLength) {
      errors[field] = `${field} deve ter pelo menos ${rule.minLength} caracteres`;
    }
    
    if (rule.pattern && !rule.pattern.test(value)) {
      errors[field] = rule.message || `${field} inválido`;
    }
  }
  
  return errors;
};
```

---

## 🔧 Rate Limiting

Todas as rotas possuem rate limiting. Monitore os headers:

- `X-RateLimit-Limit`: Limite total
- `X-RateLimit-Remaining`: Requisições restantes
- `X-RateLimit-Reset`: Timestamp do reset

```javascript
const checkRateLimit = (response) => {
  const limit = response.headers.get('X-RateLimit-Limit');
  const remaining = response.headers.get('X-RateLimit-Remaining');
  const reset = response.headers.get('X-RateLimit-Reset');
  
  if (remaining && parseInt(remaining) < 5) {
    showNotification(`⚠️ Apenas ${remaining} requisições restantes`, 'warning');
  }
};
```

---

## 🚨 Tratamento de Erros

```javascript
const handleAPIError = (error, context) => {
  console.error(`Erro em ${context}:`, error);
  
  switch (error.status) {
    case 400:
      showNotification('Dados inválidos', 'error');
      break;
    case 401:
      showNotification('Não autorizado', 'error');
      // Redirecionar para login
      break;
    case 403:
      showNotification('Acesso negado', 'error');
      break;
    case 404:
      showNotification('Recurso não encontrado', 'error');
      break;
    case 429:
      showNotification('Muitas requisições. Tente novamente em alguns minutos.', 'error');
      break;
    case 500:
      showNotification('Erro interno do servidor', 'error');
      break;
    default:
      showNotification('Erro inesperado', 'error');
  }
};
```

---

## 📱 Responsividade e UX

### Loading States
```javascript
const showLoading = (element) => {
  element.classList.add('loading');
  element.disabled = true;
};

const hideLoading = (element) => {
  element.classList.remove('loading');
  element.disabled = false;
};
```

### Confirmações
```javascript
const confirmAction = (message, callback) => {
  const modal = document.createElement('div');
  modal.className = 'confirm-modal';
  modal.innerHTML = `
    <div class="confirm-content">
      <p>${message}</p>
      <div class="confirm-actions">
        <button class="btn-cancel">Cancelar</button>
        <button class="btn-confirm">Confirmar</button>
      </div>
    </div>
  `;
  
  modal.querySelector('.btn-confirm').onclick = () => {
    callback();
    modal.remove();
  };
  
  modal.querySelector('.btn-cancel').onclick = () => {
    modal.remove();
  };
  
  document.body.appendChild(modal);
};
```

---

Este documento fornece uma base completa para implementar o frontend que consome a API Backend-Lycosidae. Adapte os exemplos conforme sua stack tecnológica (React, Vue, Angular, etc.).
