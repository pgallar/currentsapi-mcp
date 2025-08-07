# News MCP

Servidor MCP para la API de Currents News con Server-Sent Events (SSE).

## Descripción

Este proyecto implementa un servidor MCP (Model-Controller-Presenter) para interactuar con la API de Currents News, que proporciona acceso a noticias de todo el mundo en diferentes idiomas y categorías. Utiliza Server-Sent Events (SSE) para proporcionar actualizaciones en tiempo real.

## Endpoints implementados

### Endpoints SSE (Server-Sent Events)
- **Stream de búsqueda de noticias**: Proporciona actualizaciones en tiempo real de las noticias según los criterios de búsqueda especificados.
- **Stream de últimas noticias**: Envía actualizaciones periódicas de las últimas noticias disponibles.

### Endpoints auxiliares
- **Idiomas disponibles**: Lista los idiomas soportados por la API.
- **Regiones disponibles**: Lista las regiones/países disponibles para filtrar noticias.
- **Categorías disponibles**: Lista las categorías de noticias disponibles.

## Requisitos

- Python 3.8+
- FastAPI
- FastMCP
- HTTPX
- Pydantic
- Python-dotenv

## Configuración

El servidor MCP espera que la variable de entorno `CURRENTS_API_KEY` esté configurada. Puedes configurarla de dos maneras:

1. **Variables de entorno del sistema**: Configura la variable directamente en el sistema:
   ```
   export CURRENTS_API_KEY=tu_api_key_aquí
   ```

2. **Archivo .env**: Alternativamente, puedes crear un archivo `.env` en la raíz del proyecto:
   ```
   CURRENTS_API_KEY=tu_api_key_aquí
   ```

## Instalación

### Con Python local

1. Crea un entorno virtual e instala las dependencias:
   ```
   python -m venv venv
   source venv/bin/activate  # En Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

2. Inicia el servidor:
   ```
   ./start-server.sh  # En Windows: python -m src.main
   ```

### Con Docker

1. Construye e inicia el contenedor:
   ```
   docker-compose up -d
   ```

## Uso

Una vez iniciado el servidor, puedes acceder a la API en:

- Lista de herramientas: http://localhost:8004/api/v1/tools
- Endpoint SSE: http://localhost:8004/sse/

## Ejemplos de uso

### Consumir stream de búsqueda de noticias sobre tecnología en inglés

```javascript
// Ejemplo en JavaScript
const eventSource = new EventSource('http://localhost:8004/api/v1/tools/stream_search_news?language=en&category=technology&keywords=AI');

eventSource.addEventListener('search_news', function(event) {
    const data = JSON.parse(event.data);
    console.log('Noticias de tecnología recibidas:', data);
});
```

### Consumir eventos SSE para últimas noticias

```javascript
// Ejemplo en JavaScript
const eventSource = new EventSource('http://localhost:8004/api/v1/tools/stream_latest_news?language=es');

eventSource.addEventListener('latest_news', function(event) {
    const data = JSON.parse(event.data);
    console.log('Nuevas noticias recibidas:', data);
});

eventSource.addEventListener('error', function(event) {
    console.error('Error en el stream:', JSON.parse(event.data));
});

eventSource.addEventListener('close', function(event) {
    console.log('Stream cerrado:', JSON.parse(event.data));
    eventSource.close();
});
```

```python
# Ejemplo en Python con aiohttp
import aiohttp
import asyncio
import json

async def consume_news_sse():
    async with aiohttp.ClientSession() as session:
        async with session.get('http://localhost:8004/api/v1/tools/stream_latest_news?language=es') as response:
            async for line in response.content:
                if line.startswith(b'data:'):
                    data = json.loads(line.decode('utf-8')[5:])
                    print(f"Nuevas noticias recibidas: {data}")
```

## Licencia

Este proyecto está licenciado bajo la Licencia MIT.