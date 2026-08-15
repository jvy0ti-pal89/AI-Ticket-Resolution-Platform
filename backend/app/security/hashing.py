import hashlib
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def _prepare_password(password: str) -> str:
    # Always SHA-256 hash first to produce a fixed 64-character hex string (well under 72 bytes)
    return hashlib.sha256(password.encode("utf-8")).hexdigest()


def hash_password(password: str) -> str:
    prepared = _prepare_password(password)
    return pwd_context.hash(prepared)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    prepared = _prepare_password(plain_password)
    return pwd_context.verify(prepared, hashed_password)
