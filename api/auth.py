from passlib.context import CryptContext
from jose import JWTError,jwt
# jwt:creates and verify jwt tokens
from datetime import datetime,timedelta
# timedelta:is used to add the time,basically it is used for token expiration...


# CryptContext manages password hashing and verification for us.
# Using bcrypt is fine, but the passlib+bcrypt combo on your machine is currently
# throwing errors about byte length / backend detection.
# Switching to a more robust scheme fixes register 500.


SECRET_KEY="my_super_secret_key"
ALGORITHM="HS256"
ACCESS_TOKEN_EXPIRE_MINUTES=30


# learn about it later in detail
pwd_context = CryptContext(
    schemes=["pbkdf2_sha256"],
    deprecated="auto",
)


def hash_password(password: str):
    if password is None:
        raise ValueError("password is required")
    return pwd_context.hash(password)


def verify_password(plain_pass:str,hashed_pass:str):
    return pwd_context.verify(plain_pass,hashed_pass)

def create_access_token(data:dict):
    to_encode=data.copy()
    expire=datetime.now+timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp":expire})

    encoded_jwt=jwt.encode(
        to_encode,
        SECRET_KEY,
        algorithm=ALGORITHM
    )
    return encoded_jwt