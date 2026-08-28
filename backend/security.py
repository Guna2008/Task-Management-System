from passlib.context import CryptContext
from jose import jwt
from fastapi.security import OAuth2PasswordBearer

pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated ="auto"
)

SECRET_KEY="my-super-secret-key"
ALGORITHM="HS256"

oauth2_scheme= OAuth2PasswordBearer(tokenUrl="login")

def hash_password(password:str):
    return pwd_context.hash(password)

def verify_password(password:str, hashed_password:str):
    return pwd_context.verify(password,hashed_password)

def create_access_token(data:dict):
    return jwt.encode(data,SECRET_KEY,algorithm=ALGORITHM)
0212.

