"""
Servidor de desarrollo
"""
import uvicorn
from core.settings import get_settings

settings = get_settings()

def run_server(host: str = "0.0.0.0", port: int = 6060, reload: bool = None):
    """Ejecuta el servidor de desarrollo"""
    if reload is None:
        reload = settings.DEBUG
    
    uvicorn.run(
        "core.app:app",
        host=host,
        port=port,
        reload=reload,
        log_level="info" if settings.DEBUG else "warning"
    )
