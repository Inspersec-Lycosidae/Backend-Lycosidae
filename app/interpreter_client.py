"""
Cliente para comunicação com o interpretador
"""
import httpx
import asyncio
from typing import Dict, Any, Optional
from datetime import datetime

try:
    from .config import settings
    from .logger import get_logger
    from .exceptions import ExternalServiceException
except ImportError:
    from config import settings
    from logger import get_logger
    from exceptions import ExternalServiceException

logger = get_logger(__name__)

class InterpreterClient:
    """Cliente para comunicação com o interpretador"""
    
    def __init__(self, base_url: str = None, timeout: int = 30):
        self.base_url = base_url or settings.interpreter_url
        self.timeout = timeout
        self.client = httpx.AsyncClient(timeout=timeout)
    
    async def __aenter__(self):
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.client.aclose()
    
    async def _make_request(self, method: str, endpoint: str, data: Dict[str, Any] = None) -> Dict[str, Any]:
        """Faz uma requisição para o interpretador"""
        url = f"{self.base_url}{endpoint}"
        
        try:
            logger.debug(f"Making {method} request to {url}")
            
            if method.upper() == "GET":
                response = await self.client.get(url)
            elif method.upper() == "POST":
                response = await self.client.post(url, json=data)
            elif method.upper() == "PUT":
                response = await self.client.put(url, json=data)
            elif method.upper() == "DELETE":
                response = await self.client.delete(url)
            else:
                raise ValueError(f"Unsupported HTTP method: {method}")
            
            response.raise_for_status()
            return response.json()
            
        except httpx.TimeoutException:
            logger.error(f"Timeout when calling interpreter: {url}")
            raise ExternalServiceException("Interpreter service timeout", "interpreter")
        except httpx.HTTPStatusError as e:
            logger.error(f"HTTP error when calling interpreter: {e.response.status_code} - {e.response.text}")
            raise ExternalServiceException(f"Interpreter service error: {e.response.status_code}", "interpreter")
        except Exception as e:
            logger.error(f"Unexpected error when calling interpreter: {str(e)}")
            raise ExternalServiceException(f"Interpreter communication error: {str(e)}", "interpreter")
    
    # Métodos para usuários
    async def create_user(self, user_data: Dict[str, Any]) -> Dict[str, Any]:
        """Cria um usuário via interpretador"""
        return await self._make_request("POST", "/users", user_data)
    
    async def get_user(self, user_id: str) -> Dict[str, Any]:
        """Busca um usuário via interpretador"""
        return await self._make_request("GET", f"/users/{user_id}")
    
    async def update_user(self, user_id: str, user_data: Dict[str, Any]) -> Dict[str, Any]:
        """Atualiza um usuário via interpretador"""
        return await self._make_request("PUT", f"/users/{user_id}", user_data)
    
    async def delete_user(self, user_id: str) -> Dict[str, Any]:
        """Deleta um usuário via interpretador"""
        return await self._make_request("DELETE", f"/users/{user_id}")
    
    # Métodos para competições
    async def create_competition(self, competition_data: Dict[str, Any]) -> Dict[str, Any]:
        """Cria uma competição via interpretador"""
        return await self._make_request("POST", "/competitions", competition_data)
    
    async def get_competition(self, competition_id: str) -> Dict[str, Any]:
        """Busca uma competição via interpretador"""
        return await self._make_request("GET", f"/competitions/{competition_id}")
    
    async def get_competition_by_invite(self, invite_code: str) -> Dict[str, Any]:
        """Busca uma competição por código de convite via interpretador"""
        return await self._make_request("GET", f"/competitions/invite/{invite_code}")
    
    async def update_competition(self, competition_id: str, competition_data: Dict[str, Any]) -> Dict[str, Any]:
        """Atualiza uma competição via interpretador"""
        return await self._make_request("PUT", f"/competitions/{competition_id}", competition_data)
    
    async def delete_competition(self, competition_id: str) -> Dict[str, Any]:
        """Deleta uma competição via interpretador"""
        return await self._make_request("DELETE", f"/competitions/{competition_id}")
    
    # Métodos para exercícios
    async def create_exercise(self, exercise_data: Dict[str, Any]) -> Dict[str, Any]:
        """Cria um exercício via interpretador"""
        return await self._make_request("POST", "/exercises", exercise_data)
    
    async def get_exercise(self, exercise_id: str) -> Dict[str, Any]:
        """Busca um exercício via interpretador"""
        return await self._make_request("GET", f"/exercises/{exercise_id}")
    
    async def update_exercise(self, exercise_id: str, exercise_data: Dict[str, Any]) -> Dict[str, Any]:
        """Atualiza um exercício via interpretador"""
        return await self._make_request("PUT", f"/exercises/{exercise_id}", exercise_data)
    
    async def delete_exercise(self, exercise_id: str) -> Dict[str, Any]:
        """Deleta um exercício via interpretador"""
        return await self._make_request("DELETE", f"/exercises/{exercise_id}")
    
    # Métodos para tags
    async def create_tag(self, tag_data: Dict[str, Any]) -> Dict[str, Any]:
        """Cria uma tag via interpretador"""
        return await self._make_request("POST", "/tags", tag_data)
    
    async def get_tag(self, tag_id: str) -> Dict[str, Any]:
        """Busca uma tag via interpretador"""
        return await self._make_request("GET", f"/tags/{tag_id}")
    
    async def get_tag_by_type(self, tag_type: str) -> Dict[str, Any]:
        """Busca uma tag por tipo via interpretador"""
        return await self._make_request("GET", f"/tags/type/{tag_type}")
    
    async def update_tag(self, tag_id: str, tag_data: Dict[str, Any]) -> Dict[str, Any]:
        """Atualiza uma tag via interpretador"""
        return await self._make_request("PUT", f"/tags/{tag_id}", tag_data)
    
    async def delete_tag(self, tag_id: str) -> Dict[str, Any]:
        """Deleta uma tag via interpretador"""
        return await self._make_request("DELETE", f"/tags/{tag_id}")
    
    # Métodos para times
    async def create_team(self, team_data: Dict[str, Any]) -> Dict[str, Any]:
        """Cria um time via interpretador"""
        return await self._make_request("POST", "/teams", team_data)
    
    async def get_team(self, team_id: str) -> Dict[str, Any]:
        """Busca um time via interpretador"""
        return await self._make_request("GET", f"/teams/{team_id}")
    
    async def update_team(self, team_id: str, team_data: Dict[str, Any]) -> Dict[str, Any]:
        """Atualiza um time via interpretador"""
        return await self._make_request("PUT", f"/teams/{team_id}", team_data)
    
    async def delete_team(self, team_id: str) -> Dict[str, Any]:
        """Deleta um time via interpretador"""
        return await self._make_request("DELETE", f"/teams/{team_id}")
    
    # Métodos para containers
    async def create_container(self, container_data: Dict[str, Any]) -> Dict[str, Any]:
        """Cria um container via interpretador"""
        return await self._make_request("POST", "/containers", container_data)
    
    async def get_container(self, container_id: str) -> Dict[str, Any]:
        """Busca um container via interpretador"""
        return await self._make_request("GET", f"/containers/{container_id}")
    
    async def update_container(self, container_id: str, container_data: Dict[str, Any]) -> Dict[str, Any]:
        """Atualiza um container via interpretador"""
        return await self._make_request("PUT", f"/containers/{container_id}", container_data)
    
    async def delete_container(self, container_id: str) -> Dict[str, Any]:
        """Deleta um container via interpretador"""
        return await self._make_request("DELETE", f"/containers/{container_id}")
    
    # Métodos para relacionamentos
    async def create_user_competition(self, user_competition_data: Dict[str, Any]) -> Dict[str, Any]:
        """Cria relacionamento usuário-competição via interpretador"""
        return await self._make_request("POST", "/user-competitions", user_competition_data)
    
    async def delete_user_competition(self, user_id: str, competition_id: str) -> Dict[str, Any]:
        """Deleta relacionamento usuário-competição via interpretador"""
        return await self._make_request("DELETE", f"/user-competitions/{user_id}/{competition_id}")
    
    async def create_user_team(self, user_team_data: Dict[str, Any]) -> Dict[str, Any]:
        """Cria relacionamento usuário-time via interpretador"""
        return await self._make_request("POST", "/user-teams", user_team_data)
    
    async def delete_user_team(self, user_id: str, team_id: str) -> Dict[str, Any]:
        """Deleta relacionamento usuário-time via interpretador"""
        return await self._make_request("DELETE", f"/user-teams/{user_id}/{team_id}")
    
    async def create_team_competition(self, team_competition_data: Dict[str, Any]) -> Dict[str, Any]:
        """Cria relacionamento time-competição via interpretador"""
        return await self._make_request("POST", "/team-competitions", team_competition_data)
    
    async def delete_team_competition(self, team_id: str, competition_id: str) -> Dict[str, Any]:
        """Deleta relacionamento time-competição via interpretador"""
        return await self._make_request("DELETE", f"/team-competitions/{team_id}/{competition_id}")
    
    async def create_exercise_tag(self, exercise_tag_data: Dict[str, Any]) -> Dict[str, Any]:
        """Cria relacionamento exercício-tag via interpretador"""
        return await self._make_request("POST", "/exercise-tags", exercise_tag_data)
    
    async def delete_exercise_tag(self, exercise_id: str, tag_id: str) -> Dict[str, Any]:
        """Deleta relacionamento exercício-tag via interpretador"""
        return await self._make_request("DELETE", f"/exercise-tags/{exercise_id}/{tag_id}")
    
    async def create_exercise_competition(self, exercise_competition_data: Dict[str, Any]) -> Dict[str, Any]:
        """Cria relacionamento exercício-competição via interpretador"""
        return await self._make_request("POST", "/exercise-competitions", exercise_competition_data)
    
    async def delete_exercise_competition(self, exercise_id: str, competition_id: str) -> Dict[str, Any]:
        """Deleta relacionamento exercício-competição via interpretador"""
        return await self._make_request("DELETE", f"/exercise-competitions/{exercise_id}/{competition_id}")
    
    async def create_container_competition(self, container_competition_data: Dict[str, Any]) -> Dict[str, Any]:
        """Cria relacionamento container-competição via interpretador"""
        return await self._make_request("POST", "/container-competitions", container_competition_data)
    
    async def delete_container_competition(self, container_id: str, competition_id: str) -> Dict[str, Any]:
        """Deleta relacionamento container-competição via interpretador"""
        return await self._make_request("DELETE", f"/container-competitions/{container_id}/{competition_id}")
    
    # Método de health check
    async def health_check(self) -> Dict[str, Any]:
        """Verifica saúde do interpretador"""
        return await self._make_request("GET", "/health")

# Instância global do cliente
interpreter_client = InterpreterClient()
