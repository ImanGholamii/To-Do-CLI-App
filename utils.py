from functools import wraps
from time import perf_counter
from typing import Callable


def timeit_decor(func: Callable) -> Callable:
    """Decorator: print elapsed time when the function finishes."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = perf_counter()
        result = func(*args, **kwargs)
        end = perf_counter()
        elapsed_time = end - start
        print(f"[timeit] {func.__name__} ran in {elapsed_time:.4f}s")
        return result

    return wrapper


def confirm(prompt: str = "Are you sure? (y/N): ") -> bool:
    """Ask user for yes/no confirmation on the console."""
    try:
        answer = input(prompt).strip().lower()
    except (EOFError, KeyboardInterrupt):
        return False
    return answer in ("y", "yes")