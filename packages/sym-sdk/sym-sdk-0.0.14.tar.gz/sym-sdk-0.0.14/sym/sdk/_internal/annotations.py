from abc import ABC, abstractmethod
from contextlib import contextmanager
from typing import Any, Callable, Dict, List, Literal, TypedDict, TypeVar, overload

ConfigType = Any
Event = Any  # TODO: type as runtime.event
RegistryKey = Literal["hooks", "actions", "reducers", "handlers"]

F = TypeVar("F", bound=Callable)


class Registry(TypedDict):
    hooks: Dict[str, Callable[[Event], None]]
    actions: Dict[str, Callable[[Event], None]]
    reducers: Dict[str, Callable[[Any], Any]]
    handlers: Dict[str, Callable[[ConfigType, Event], Any]]

    @classmethod
    def create_registry(cls):
        return Registry(hooks={}, actions={}, reducers={}, handlers={})


class SymAnnotationValidator(ABC):
    def __init__(self, name: str):
        self.name = name

    @abstractmethod
    def validate_reducer(self, reducer):
        pass

    @abstractmethod
    def test_reducer(self, reducer):
        pass


class CallableSource(ABC):
    @abstractmethod
    def get_reducers(self) -> List[callable]:
        pass


class SingletonMeta(type):
    def __new__(cls, name, bases, attrs):
        attrs["_instance"] = None
        return super().__new__(cls, name, bases, attrs)

    def __call__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__call__(*args, **kwargs)
        return cls._instance


class _Implementations(metaclass=SingletonMeta):
    """Stack of context-dependent registries.  A local context will push_registry and
    pop_registry to add/remove its receptacle for registered functions.
    """

    registries = [Registry.create_registry()]
    validators = {}

    @classmethod
    def register_validator(cls, validator: SymAnnotationValidator):
        cls.validators[validator.name] = validator

    @classmethod
    def _push_registry(cls, registry: Registry):
        cls.registries.append(registry)

    @classmethod
    def _pop_registry(cls):
        return cls.registries.pop()

    @classmethod
    def get_registry(cls, seek_from_global: bool = False):
        """Single entry point for clients to obtain the active registry.

        Params:
            seek_from_global: Whether to pull out the Global or Local Registry
        """
        if seek_from_global:
            offset = 0
        else:
            offset = -1

        return cls.registries[offset]

    @classmethod
    def register(cls, key: RegistryKey, name: str, value: Callable):
        cls.get_registry()[key][name] = value

    @classmethod
    def fetch(cls, key: RegistryKey, name: str) -> Callable:
        return cls.get_registry()[key][name]

    @classmethod
    def annotation(cls, key: RegistryKey):
        def decorator_factory(name: str) -> Callable[[F], F]:
            def decorator(fn: F) -> F:
                cls.register(key, name, fn)
                return fn

            return decorator

        @overload
        def decorator_wrapper(name_or_fn: F) -> F:
            ...

        @overload
        def decorator_wrapper(name_or_fn: str) -> Callable[[F], F]:
            ...

        def decorator_wrapper(name_or_fn):
            if callable(name_or_fn):
                return decorator_factory(name_or_fn.__name__)(name_or_fn)
            elif hasattr(name_or_fn, "__func__"):
                # Covers the case of a Class Static method with @staticmethod below
                # the Sym decorator
                return decorator_factory(name_or_fn.__func__.__name__)(name_or_fn.__func__)
            else:
                return decorator_factory(name_or_fn)

        return decorator_wrapper

    @classmethod
    def validate(cls, callable_source: CallableSource):
        for validator in cls.validators:
            for reducer in callable_source.get_reducers():
                validator.validate_reducer(reducer)

    @classmethod
    def test(cls, callable_source: CallableSource):
        for validator in cls.validators:
            for reducer in callable_source.get_reducers():
                validator.test_reducer(reducer)


@contextmanager
def use_registry(local_registry: Registry = None):
    """Wraps registration of a local registry inside a using statement.

    Params:
        local_registry: Registry instance, with a new instance created on None
    """
    registry = local_registry
    if registry is None:
        registry = Registry.create_registry()

    _Implementations._push_registry(registry)
    try:
        yield registry
    finally:
        _Implementations._pop_registry()


validate = _Implementations.validate


def fetch_extension(category: str, extension_name: str, seek_from_global: bool = False):
    """Lookup method intended to pull registered extensions from the active Registry.

    Params:
        category: Desired type of extension, one of "action", "hook", or "reducer"
        extension_name: Name of the function to fetch
        seek_from_global: Whether to restrict to the top-level registered Registry

    Returns:
        Function object if registered.

    Raises:
        KeyError: if the extension requested could not be found
    """

    registry = _Implementations.get_registry(seek_from_global)
    return registry[category][extension_name]


def get_extension(
    category: str,
    extension_name: str,
    seek_from_global: bool = False,
    default_value=None,
):
    """Safe method to seek a given extension function, returning default_value if no such
    function is registered.

    Params:
        category: Desired type of extension, one of "action", "hook", or "reducer"
        extension_name: Name of the function to fetch
        seek_from_global: Whether to restrict to the top-level registered Registry
        default_value: Value to return if requested extension is not registered

    Returns:
        Function object if registered, otherwise default_value
    """
    registry = _Implementations.get_registry(seek_from_global)
    return registry[category].get(extension_name, default_value)
