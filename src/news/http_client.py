from typing import Dict, Any, Optional
import os
import aiohttp
from dotenv import load_dotenv

load_dotenv()

class CurrentsAPIClient:
    """Cliente para la API de Currents"""
    
    BASE_URL = "https://api.currentsapi.services/v1"
    
    def __init__(self):
        self.api_key = os.getenv("CURRENTS_API_KEY", "")
        if not self.api_key:
            raise ValueError("CURRENTS_API_KEY no está configurada en las variables de entorno")
    
    def get_auth_headers(self) -> Dict[str, str]:
        """Obtiene los headers de autenticación para la API"""
        return {"Authorization": self.api_key}
    
    async def _make_request(
        self,
        method: str,
        endpoint: str,
        params: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Realiza una petición a la API de Currents
        
        Args:
            method: Método HTTP (GET, POST, etc)
            endpoint: Endpoint de la API
            params: Parámetros de la petición
            
        Returns:
            Dict[str, Any]: Respuesta de la API
        """
        url = f"{self.BASE_URL}{endpoint}"
        headers = self.get_auth_headers()
        
        # Asegurarse de que params es un diccionario
        if params is None:
            params = {}
        
        async with aiohttp.ClientSession() as session:
            if method.upper() == "GET":
                async with session.get(url, params=params, headers=headers) as response:
                    # Manejar errores de la API
                    if response.status == 401:
                        raise Exception("Error de autenticación: API key inválida o expirada")
                    elif response.status == 429:
                        raise Exception("Límite de peticiones alcanzado")
                    elif response.status != 200:
                        text = await response.text()
                        raise Exception(f"Error en la petición: {response.status} - {text}")
                    
                    return await response.json()
            else:
                raise ValueError(f"Método HTTP no soportado: {method}")
    
    async def get(self, endpoint: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Realiza una petición GET a la API"""
        return await self._make_request("GET", endpoint, params)