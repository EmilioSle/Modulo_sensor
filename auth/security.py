"""
Sistema de autenticación JWT
"""
from datetime import datetime, timedelta
from typing import Optional
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext

from core.settings import get_settings

settings = get_settings()

# Configuración de seguridad
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

class AuthManager:
    """Maneja la autenticación y autorización"""
    
    def __init__(self):
        self.settings = settings
    
    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """Verificar contraseña"""
        return pwd_context.verify(plain_password, hashed_password)
    
    def get_password_hash(self, password: str) -> str:
        """Generar hash de contraseña"""
        return pwd_context.hash(password)
    
    def create_access_token(self, data: dict) -> str:
        """Crear token JWT"""
        to_encode = data.copy()
        expire = datetime.utcnow() + timedelta(minutes=self.settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        to_encode.update({"exp": expire})
        
        return jwt.encode(to_encode, self.settings.SECRET_KEY, algorithm=self.settings.JWT_ALGORITHM)
    
    def verify_token(self, token: str) -> Optional[dict]:
        """Verificar y decodificar token"""
        try:
            payload = jwt.decode(token, self.settings.SECRET_KEY, algorithms=[self.settings.JWT_ALGORITHM])
            return payload
        except JWTError:
            return None
    
    def authenticate_user(self, username: str, password: str) -> bool:
        """Autenticar usuario (versión demo)"""
        # En producción esto consultaría la base de datos
        return (username == self.settings.DEMO_USERNAME and 
                password == self.settings.DEMO_PASSWORD)

# Instancia global
auth_manager = AuthManager()

def get_current_user(token: str = Depends(oauth2_scheme)) -> str:
    """Dependencia para obtener usuario actual desde token"""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Token inválido o expirado",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    payload = auth_manager.verify_token(token)
    if payload is None:
        raise credentials_exception
    
    username: str = payload.get("sub")
    if username is None:
        raise credentials_exception
    
    return username

def verify_token(token: str = Depends(oauth2_scheme)) -> dict:
    """Dependencia para verificar token y retornar payload"""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Token inválido o expirado",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    payload = auth_manager.verify_token(token)
    if payload is None:
        raise credentials_exception
    
    return payload
