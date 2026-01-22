import httpx
import os
from fastapi import HTTPException

ORCHESTER_URL = os.getenv("ORCHESTER_URL", "http://orchester:8000")

class OrchesterClient:
    def __init__(self):
        self.base_url = ORCHESTER_URL

    async def start_container(self, payload: dict):
        async with httpx.AsyncClient(base_url=self.base_url, timeout=30.0) as client:
            try:
                response = await client.post("/orchester/start", json=payload)
                response.raise_for_status()
                return response.json()
            except httpx.HTTPStatusError as e:
                detail = e.response.json().get("detail", "Erro no Orchester")
                raise HTTPException(status_code=e.response.status_code, detail=detail)
            except Exception as e:
                raise HTTPException(status_code=503, detail=f"Orchester indisponível: {str(e)}")

    async def get_container_status(self, docker_id: str):
        async with httpx.AsyncClient(base_url=self.base_url, timeout=10.0) as client:
            try:
                response = await client.get(f"/orchester/status/{docker_id}")
                if response.status_code == 200:
                    return response.json()
                return {"running": False}
            except Exception:
                return {"running": False}

orchester = OrchesterClient()