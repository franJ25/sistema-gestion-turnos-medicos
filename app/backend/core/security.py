import os
from datetime import datetime, timedelta, timezone
from typing import Any, Union

from passlib.context import CryptContext
from jose import jwt, JWTError

# ----------------------------------------------------
# 1. CONFIGURACIÓN
# ----------------------------------------------------

# La clave secreta se carga desde una variable de entorno.
# En desarrollo local, se puede definir en un archivo .env
SECRET_KEY = os.getenv("BACKEND_SECRET_KEY", "dev-secret-key-change-in-production")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24 # Token válido por 24 horas

# Contexto para el hash de contraseñas (usando bcrypt)
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# ----------------------------------------------------
# 2. HASHING DE CONTRASEÑAS
# ----------------------------------------------------

def hash_password(password: str) -> str:
    """Genera el hash de una contraseña."""
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verifica si la contraseña plana coincide con el hash."""
    return pwd_context.verify(plain_password, hashed_password)


# ----------------------------------------------------
# 3. GENERACIÓN DE JWT
# ----------------------------------------------------

def create_access_token(data: dict, expires_delta: Union[timedelta, None] = None) -> str:
    """Crea un nuevo token JWT."""
    to_encode = data.copy()
    
    # Determinar tiempo de expiración
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        # Si no se especifica, usa la configuración por defecto (24h)
        expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    # Añadir los claims estándar 'exp' y 'sub' (subject/asunto)
    to_encode.update({"exp": expire, "sub": "access_token"})
    
    # Codificar el token
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


# ----------------------------------------------------
# 4. DECODIFICACIÓN DE JWT
# ----------------------------------------------------

def decode_access_token(token: str) -> dict[str, Any] | None:
    """Decodifica un token JWT y devuelve los datos (claims)."""
    try:
        # Decodificar el token
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        # Devuelve None si el token es inválido o ha expirado
        return None