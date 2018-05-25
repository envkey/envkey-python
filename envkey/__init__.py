from .loader import load
from .fetch import fetch_env

load(is_init=True)

__all__ = ['load', 'fetch_env']