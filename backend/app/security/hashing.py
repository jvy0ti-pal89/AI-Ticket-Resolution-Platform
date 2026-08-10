from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def _truncate_to_bytes(password: str) -> str:
    """Safely convert password to UTF-8 bytes and slice at 72 bytes max."""
    if not isinstance(password, str):
        password = str(password)
    # Encode to bytes, slice to 72 bytes, decode back safely ignoring trailing incomplete characters
    return password.encode("utf-8")[:72].decode("utf-8", errors="ignore")


def hash_password(password: str) -> str:
    safe_pwd = _truncate_to_bytes(password)
    return pwd_context.hash(safe_pwd)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    safe_pwd = _truncate_to_bytes(plain_password)
    return pwd_context.verify(safe_pwd, hashed_password)
