import importlib
import inspect
from functools import wraps

from sqlalchemy.ext.asyncio import AsyncSession


def validator(name):
    def decorator(func):
        module_name = "app.api.validators"
        module = importlib.import_module(module_name)
        validation_func = getattr(module, name, None)
        if validation_func is None or not inspect.isfunction(validation_func):
            raise AttributeError(f"Validator '{name}' not found")

        @wraps(func)
        def wrapper(*args, **kwargs):
            validation_error = validation_func(*args, **kwargs)
            if validation_error:
                return {"error": validation_error}
            return func(*args, **kwargs)

        return wrapper

    return decorator


async def is_task_author(
    task_id: int,
    user: int,
    session: AsyncSession,
) -> None:
    pass
