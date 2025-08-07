from typing import Dict

class BaseRoutes:
    """Clase base para las rutas de la API"""
    
    def __init__(self):
        """Inicializa la clase base de rutas"""
        pass
    
    def register_tools(self, mcp):
        """
        Registra las herramientas en el servidor MCP
        
        Args:
            mcp: Instancia de FastMCP
        """
        pass
    
    def get_auth_headers(self) -> Dict[str, str]:
        """
        Obtiene los headers de autenticación para la API
        
        Returns:
            Dict[str, str]: Headers de autenticación
        """
        return {}