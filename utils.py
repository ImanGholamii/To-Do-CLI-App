from functools import wraps
from time import perf_counter


def timeit_decor(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = perf_counter()
        result = func(*args, **kwargs)
        end = perf_counter()
        elapsed_time = end - start
        print(f"[timeit] {func.__name__} ran in {elapsed_time:.4f}s")
        return result

    return wrapper
