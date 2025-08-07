import os
import logging
import uvicorn
from fastmcp import FastMCP
from news.routes import NewsRoutes

def setup_logging() -> None:
    """Configura el sistema de logging"""
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )

def get_server_config() -> dict:
    """Obtiene la configuración del servidor desde variables de entorno"""
    use_sse = os.getenv("USE_SSE", "true").lower() == "true"  # Por defecto usar SSE
    reload = os.getenv("RELOAD", "false").lower() == "true"
    
    return {
        "host": os.getenv("HOST", "0.0.0.0"),
        "port": int(os.getenv("PORT", "8000")),
        "log_level": os.getenv("LOG_LEVEL", "info"),
        "use_sse": use_sse,
        "reload": reload,
    }

def create_mcp_server(config: dict) -> FastMCP:
    """Crea y configura el servidor FastMCP"""
    # Configurar para usar SSE
    mcp = FastMCP("news")
    return mcp

def register_routers(mcp: FastMCP) -> None:
    """Registra las rutas en el servidor FastMCP"""
    # Registrar rutas de noticias
    news_routes = NewsRoutes()
    news_routes.register_tools(mcp)

async def run_sse_server(mcp: FastMCP, host: str, port: int) -> None:
    """Ejecuta el servidor SSE"""
    logging.info(f"Iniciando servidor SSE en {host}:{port}")
    
    # Agregar un delay para asegurar que el servidor esté completamente inicializado
    import asyncio
    await asyncio.sleep(1)
    logging.info("Inicialización del servidor completa, listo para aceptar conexiones")

    await mcp.run_async(transport="sse", host=host, port=port)

def main() -> None:
    """Función principal para iniciar el servidor"""
    setup_logging()
    config = get_server_config()
    
    # Mostrar configuración
    logging.info(f"Iniciando servidor con configuración:")
    logging.info(f"Host: {config['host']}")
    logging.info(f"Puerto: {config['port']}")
    logging.info(f"Transporte: SSE")
    
    try:
        mcp = create_mcp_server(config)
        register_routers(mcp)
        
        # Ejecutar servidor SSE
        import asyncio
        asyncio.run(run_sse_server(mcp, config["host"], config["port"]))
    except Exception as e:
        logging.critical(f"Error fatal: {str(e)}")
        import sys
        sys.exit(1)

if __name__ == "__main__":
    main()