"""Helpers for interacting with a Slack workspace."""

from typing import List, Optional, Sequence, Union

from sym.sdk.errors import SlackError, SlackTimeoutError  # noqa
from sym.sdk.user import User


class SlackLookupType:
    USER = "user"
    USER_ID = "slack_user_id"
    CHANNEL = "channel_uuid"
    GROUP = "group"
    EMAIL = "email"


class SlackChannel:
    def __init__(
        self, lookup_type: str, lookup_keys: List[str], allow_self: Optional[bool] = False
    ):
        self.lookup_type = lookup_type
        self.lookup_keys = lookup_keys
        self.allow_self = allow_self


def user(identifier: Union[str, User]) -> SlackChannel:
    """A reference to a Slack user.

    Users can be specified with a Slack user ID, email,
    or Sym :class:`~sym.sdk.user.User` instance.
    """
    if isinstance(identifier, User):
        if (slack_identity := identifier.identity("slack")) :
            return SlackChannel(SlackLookupType.USER_ID, [slack_identity.user_id])
        return SlackChannel(SlackLookupType.EMAIL, [identifier.email])
    return SlackChannel(SlackLookupType.USER, [identifier])


def channel(name: str, allow_self: Optional[bool] = False) -> SlackChannel:
    """A reference to a Slack channel."""
    return SlackChannel(SlackLookupType.CHANNEL, [name], allow_self=allow_self)


def group(users: Sequence[Union[str, User]]) -> SlackChannel:
    """
    A reference to a Slack group.

    Args:
        users (Sequence[Union[str, User]]): A list of either Sym :class:`~sym.sdk.user.User` objects or emails.
    """
    if not users:
        raise SlackError("slack.group requires at least one user")
    user_emails = []
    have_user_objects = any(u for u in users if isinstance(u, User))
    if have_user_objects:
        for u in users:
            if isinstance(u, User):
                user_emails.append(u.email)
            else:
                user_emails.append(u)
        return SlackChannel(SlackLookupType.EMAIL, lookup_keys=list(set(user_emails)))
    return SlackChannel(SlackLookupType.GROUP, lookup_keys=users)
