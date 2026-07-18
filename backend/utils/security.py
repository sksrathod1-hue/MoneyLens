import hashlib
import uuid

def generate_uuid() -> str:
    """Generate a secure unique identifier."""
    return str(uuid.uuid4())

def hash_sha256(text: str) -> str:
    """Returns the SHA-256 hash of a string."""
    return hashlib.sha256(text.encode("utf-8")).hexdigest()
