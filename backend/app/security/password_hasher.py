from passlib.context import CryptContext


pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")

def hash(password: str):
    return pwd_context.hash(password)

def verify(password: str, password_hash: str,):
    return pwd_context.verify(password,password_hash)

