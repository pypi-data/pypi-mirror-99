"""Introspection tools and helpers for the Sym API."""

from typing import Optional

from sym.sdk.user import User


def debug(message: str, *, user: Optional[User] = None):
    """Send a debug message.

    This method takes a message and sends it to a :class:`~sym.sdk.user.User`
    via an appropriate channel (e.g. Slack).

    It can be helpful to debug the output of various Integrations.

    Args:
        user: The :class:`~sym.sdk.user.User` to send the message to. Defaults to the Implementer of this Flow.
    """
