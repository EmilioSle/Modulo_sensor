"""
Router de autenticación
"""
from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm

from auth.security import auth_manager
from schemas.auth import TokenResponse

router = APIRouter()

@router.post("/login", response_model=TokenResponse)
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    """Endpoint de login"""
    
    # Autenticar usuario
    if not auth_manager.authenticate_user(form_data.username, form_data.password):
        raise HTTPException(
            status_code=401,
            detail="Credenciales inválidas"
        )
    
    # Crear token
    access_token = auth_manager.create_access_token(
        data={"sub": form_data.username}
    )
    
    return TokenResponse(access_token=access_token, token_type="bearer")
