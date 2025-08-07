from typing import Dict, Any, Optional, List, AsyncGenerator
from fastmcp import FastMCP
from pydantic import BaseModel, Field, field_validator, ConfigDict
from .base_routes import BaseRoutes
from .client import NewsClient

class NewsArticleModel(BaseModel):
    """Modelo para representar un artículo de noticias"""
    id: str = Field(description="ID único del artículo")
    title: str = Field(description="Título del artículo")
    description: str = Field(description="Descripción del artículo")
    url: str = Field(description="URL del artículo")
    author: str = Field(description="Autor del artículo")
    image: Optional[str] = Field(default=None, description="URL de la imagen del artículo")
    language: str = Field(description="Idioma del artículo")
    category: List[str] = Field(description="Categorías del artículo")
    published: str = Field(description="Fecha de publicación del artículo")
    
    model_config = ConfigDict(extra="ignore", validate_assignment=True)
    
    @field_validator('*', mode='before')
    @classmethod
    def empty_str_to_none(cls, v):
        if v == "":
            return None
        return v

class NewsResponseModel(BaseModel):
    """Modelo para representar la respuesta de la API de noticias"""
    status: str = Field(description="Estado de la respuesta")
    news: List[NewsArticleModel] = Field(description="Lista de artículos de noticias")
    
    model_config = ConfigDict(extra="ignore", validate_assignment=True)

class LanguagesResponseModel(BaseModel):
    """Modelo para representar la respuesta de idiomas disponibles"""
    languages: Dict[str, str] = Field(description="Idiomas disponibles")
    description: str = Field(description="Descripción de la respuesta")
    status: str = Field(description="Estado de la respuesta")
    
    model_config = ConfigDict(extra="ignore", validate_assignment=True)

class RegionsResponseModel(BaseModel):
    """Modelo para representar la respuesta de regiones disponibles"""
    regions: Dict[str, str] = Field(description="Regiones disponibles")
    description: str = Field(description="Descripción de la respuesta")
    status: str = Field(description="Estado de la respuesta")
    
    model_config = ConfigDict(extra="ignore", validate_assignment=True)

class CategoriesResponseModel(BaseModel):
    """Modelo para representar la respuesta de categorías disponibles"""
    categories: List[str] = Field(description="Categorías disponibles")
    description: str = Field(description="Descripción de la respuesta")
    status: str = Field(description="Estado de la respuesta")
    
    model_config = ConfigDict(extra="ignore", validate_assignment=True)

class NewsRoutes(BaseRoutes):
    """Rutas para la API de noticias"""
    
    def __init__(self):
        super().__init__()
        self.client = NewsClient()
    
    def register_tools(self, mcp: FastMCP):

                
        @mcp.tool(
            name="search_news",
            description="Búsqueda de noticias",
            tags=["news", "search"]
        )
        async def search_news(
            language: Optional[str] = Field(default=None, description="Código de idioma (ej: en, es, fr)"),
            keywords: Optional[str] = Field(default=None, description="Palabras clave para la búsqueda"),
            country: Optional[str] = Field(default=None, description="País para filtrar (ej: US, ES)"),
            category: Optional[str] = Field(default=None, description="Categoría para filtrar (ej: technology, business)")
        ) -> Dict[str, Any]:
            """
            Búsqueda de noticias
            
            Args:
                language: Código de idioma
                keywords: Palabras clave para la búsqueda
                country: País para filtrar
                category: Categoría para filtrar
            """
            import datetime
            
            try:
                # Obtener fecha actual para el inicio de la búsqueda
                now = datetime.datetime.utcnow()
                # Buscar noticias desde la última hora
                start_date = (now - datetime.timedelta(hours=1)).strftime("%Y-%m-%dT%H:%M:%S+00:00")
                
                result = await self.client.search_news(
                    language=language,
                    keywords=keywords,
                    country=country,
                    category=category,
                    start_date=start_date
                )
                
                return {
                    "success": True,
                    "search_params": {
                        "language": language,
                        "keywords": keywords,
                        "country": country,
                        "category": category,
                        "start_date": start_date
                    },
                    "result": result
                }
            except Exception as e:
                return {
                    "success": False,
                    "error": str(e)
                }
        

        
        @mcp.tool(
            name="get_latest_news",
            description="Obtener las últimas noticias",
            tags=["news", "latest"]
        )
        async def get_latest_news(
            language: Optional[str] = Field(default=None, description="Código de idioma (ej: en, es, fr)")
        ) -> Dict[str, Any]:
            """
            Obtener las últimas noticias
            
            Args:
                language: Código de idioma
            """
            try:
                result = await self.client.get_latest_news(language=language)
                
                return {
                    "success": True,
                    "language": language,
                    "result": result
                }
            except Exception as e:
                return {
                    "success": False,
                    "error": str(e)
                }
        
        @mcp.tool(
            name="get_available_languages",
            description="Obtener idiomas disponibles",
            tags=["news", "languages"]
        )
        async def get_available_languages() -> Dict[str, Any]:
            """
            Obtiene los idiomas disponibles
            """
            try:
                result = await self.client.get_available_languages()
                return {
                    "success": True,
                    "result": result
                }
            except Exception as e:
                return {"error": f"Error obteniendo idiomas disponibles: {str(e)}"}
        
        @mcp.tool(
            name="get_available_regions",
            description="Obtener regiones disponibles",
            tags=["news", "regions"]
        )
        async def get_available_regions() -> Dict[str, Any]:
            """
            Obtiene las regiones disponibles
            """
            try:
                result = await self.client.get_available_regions()
                return {
                    "success": True,
                    "result": result
                }
            except Exception as e:
                return {"error": f"Error obteniendo regiones disponibles: {str(e)}"}
        
        @mcp.tool(
            name="get_available_categories",
            description="Obtener categorías disponibles",
            tags=["news", "categories"]
        )
        async def get_available_categories() -> Dict[str, Any]:
            """
            Obtiene las categorías disponibles
            """
            try:
                result = await self.client.get_available_categories()
                return {
                    "success": True,
                    "result": result
                }
            except Exception as e:
                return {"error": f"Error obteniendo categorías disponibles: {str(e)}"}