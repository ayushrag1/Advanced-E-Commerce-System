import functools
from typing import Callable, Type


def logging_entry_exit(func: Callable) -> Callable:
    """
    A simple, reliable decorator for logging method entry and exit.
    Safe to use with Django/DRF methods.
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # Get instance class name if available
        instance = args[0] if args else None
        class_name = instance.__class__.__name__ if instance and hasattr(instance, '__class__') else 'Function'
        method_name = func.__name__

        # Log entry
        print("*" * 50, f"Entering {class_name}.{method_name}", "*" * 50)

        # Execute method
        result = func(*args, **kwargs)

        # Log exit
        print("#" * 50, f"Exiting {class_name}.{method_name}", "#" * 50)
        return result

    return wrapper


def for_all_methods(exclude_methods=None):
    """
    Class decorator that safely logs all methods except those specified.

    Args:
        exclude_methods (set): Set of method names to exclude from logging
    """
    if exclude_methods is None:
        exclude_methods = {'__init__', '__new__', '__str__', '__repr__'}

    def decorator(cls: Type) -> Type:
        for attr_name, attr_value in cls.__dict__.items():
            # Only decorate regular methods that aren't excluded
            if (
                callable(attr_value)
                and not attr_name.startswith('__')
                and attr_name not in exclude_methods
                and not isinstance(attr_value, (classmethod, staticmethod, property))
            ):
                setattr(cls, attr_name, logging_entry_exit(attr_value))
        return cls
    return decorator
