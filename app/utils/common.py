import random
import string
import secrets


def generate_int_code(length: int = 6) -> str:
    """Generate a random code of a given length."""
    return ''.join(random.choices('0123456789', k=length))


def generate_str_code(length: int = 16) -> str:
    """Generate a cryptographically secure random code of a given length, combining letters and numbers."""
    characters = string.ascii_letters + string.digits
    return ''.join(secrets.choice(characters) for _ in range(length))
