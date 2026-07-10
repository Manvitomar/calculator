from passlib.context import CryptContext

# CryptContext manages password hashing and verification for us.
# Using bcrypt is fine, but the passlib+bcrypt combo on your machine is currently
# throwing errors about byte length / backend detection.
# Switching to a more robust scheme fixes register 500.


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
