"""
Esquemas para autenticación
"""
from schemas.base import BaseSchema

class TokenResponse(BaseSchema):
    """Respuesta del token de acceso"""
    access_token: str
    token_type: str

class LoginRequest(BaseSchema):
    """Datos de login"""
    username: str
    password: str
