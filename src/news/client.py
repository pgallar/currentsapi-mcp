from typing import Dict, Any, Optional, List
from .http_client import CurrentsAPIClient

class NewsClient(CurrentsAPIClient):
    """Cliente para los endpoints de noticias de la API de Currents"""
    
    async def search_news(
        self,
        language: Optional[str] = None,
        keywords: Optional[str] = None,
        country: Optional[str] = None,
        category: Optional[str] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Busca noticias según los filtros especificados
        
        Args:
            language: Código de idioma
            keywords: Palabras clave para la búsqueda
            country: País para filtrar
            category: Categoría para filtrar
            start_date: Fecha de inicio (formato: YYYY-MM-DDTHH:MM:SS+00:00)
            end_date: Fecha de fin (formato: YYYY-MM-DDTHH:MM:SS+00:00)
            
        Returns:
            Dict[str, Any]: Resultados de la búsqueda
        """
        params = {}
        
        if language:
            params["language"] = language
        if keywords:
            params["keywords"] = keywords
        if country:
            params["country"] = country
        if category:
            params["category"] = category
        if start_date:
            params["start_date"] = start_date
        if end_date:
            params["end_date"] = end_date
            
        return await self.get("/search", params)
    
    async def get_latest_news(self, language: Optional[str] = None) -> Dict[str, Any]:
        """
        Obtiene las últimas noticias por idioma
        
        Args:
            language: Código de idioma
            
        Returns:
            Dict[str, Any]: Últimas noticias
        """
        params = {}
        
        if language:
            params["language"] = language
            
        return await self.get("/latest-news", params)
    
    async def get_available_languages(self) -> Dict[str, Any]:
        """
        Obtiene los idiomas disponibles
        
        Returns:
            Dict[str, Any]: Idiomas disponibles
        """
        return await self.get("/available/languages")
    
    async def get_available_regions(self) -> Dict[str, Any]:
        """
        Obtiene las regiones disponibles
        
        Returns:
            Dict[str, Any]: Regiones disponibles
        """
        return await self.get("/available/regions")
    
    async def get_available_categories(self) -> Dict[str, Any]:
        """
        Obtiene las categorías disponibles
        
        Returns:
            Dict[str, Any]: Categorías disponibles
        """
        return await self.get("/available/category")