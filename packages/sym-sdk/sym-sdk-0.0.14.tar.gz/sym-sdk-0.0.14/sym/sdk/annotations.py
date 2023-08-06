"""Function annotations to implement `Handlers <https://docs.symops.com/docs/handlers>`_."""

from sym.sdk._internal.annotations import _Implementations

__all__ = ["reducer", "hook", "action"]

_reducer = _Implementations.annotation("reducers")
_hook = _Implementations.annotation("hooks")
_action = _Implementations.annotation("actions")


def reducer(function):
    """Reducers take in an Event and return a single value.py

    Reducer names are always prefixed with ``get_``."""
    return _reducer(function)


def hook(function):
    """Hooks allow you to alter control flow by overriding default implementations of Template steps.py

    Hook names are always prefixed with ``on_``."""
    return _hook(function)


def action(function):
    """Actions allow you to subscribe to Events so as to enact various side-effects.

    Action names are always prefixed with ``after_``."""
    return _action(function)
