import hashlib, secrets, bcrypt as _bcrypt
from datetime import datetime, timedelta, timezone
from jose import jwt, JWTError
from shared.config import settings


def hash_password(password: str) -> str:
    pw = password[:72].encode("utf-8")
    return _bcrypt.hashpw(pw, _bcrypt.gensalt()).decode("utf-8")


def verify_password(plain: str, hashed: str) -> bool:
    try:
        return _bcrypt.checkpw(plain[:72].encode("utf-8"), hashed.encode("utf-8"))
    except Exception:
        return False


def create_access_token(uid: int, email: str, expires_delta=None):
    expire = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=settings.JWT_ACCESS_EXPIRY // 60))
    return jwt.encode({"uid": uid, "email": email, "type": "access", "exp": expire}, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM)


def create_refresh_token(uid: int):
    expire = datetime.now(timezone.utc) + timedelta(seconds=settings.JWT_REFRESH_EXPIRY)
    return jwt.encode({"uid": uid, "type": "refresh", "exp": expire}, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM)


def decode_token(token: str):
    try:
        return jwt.decode(token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM])
    except JWTError:
        return None


def generate_token(length=32):
    return secrets.token_urlsafe(length)


def hash_token(token: str):
    return hashlib.sha256(token.encode()).hexdigest()
