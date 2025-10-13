from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import datetime, timedelta
from schemas.auth import TokenData


pwd_context = CryptContext(schemes=["argon2", "bcrypt"], deprecated="auto")


SECRET_KEY = "266c07dc372e45a7bb32ebd128fd8c1d56882ed3a6ae67af3a213441f8a44c87"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()

    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)

    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def decode_access_token(token: str) -> TokenData | None:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = str = payload.get("sub")

        if username is None:
            return None
        
        return TokenData(username=username)
    except JWTError:
        return None