import pytest

from sym.sdk import ApprovalTemplate
from sym.sdk._internal.annotations import get_extension, use_registry
from sym.sdk._internal.events import BaseEvent, BaseEventMeta, BasePayload
from sym.sdk._internal.flow import BaseFlow, BaseRun
from sym.sdk._internal.user import BaseUser, BaseUserIdentity
from sym.sdk.integrations.slack import SlackLookupType

from ..static.approvers_test_code import (
    SIMPLE_ALLOW_SELF_FALSE_CODE,
    SIMPLE_ALLOW_SELF_TRUE_CODE,
    SIMPLE_SLACK_CHANNEL_CODE,
    SIMPLE_SLACK_GROUP_CODE,
    SIMPLE_SLACK_USER_CODE,
    SIMPLE_SLACK_USER_ID_CODE,
    SLACK_GROUP_WITH_USERS_CODE,
)

TEST_SIMPLE_SLACK_CHANNELS_PARAMETERS = [
    (
        SIMPLE_SLACK_CHANNEL_CODE,
        {"lookup_type": SlackLookupType.CHANNEL, "lookup_keys": ["#managers"], "allow_self": False},
    ),
    (
        SIMPLE_SLACK_USER_CODE,
        {"lookup_type": SlackLookupType.USER, "lookup_keys": ["@David Ruiz"], "allow_self": False},
    ),
    (
        SIMPLE_SLACK_GROUP_CODE,
        {
            "lookup_type": SlackLookupType.GROUP,
            "lookup_keys": ["@David Ruiz", "@Jon Demo"],
            "allow_self": False,
        },
    ),
]


class TestSlackChannelsInterface:
    @pytest.fixture
    def event(self):
        return BaseEvent(
            meta=BaseEventMeta("sym:event-spec:approval:1.0.0:request"),
            template=ApprovalTemplate("sym:template:approval:1.0.0"),
            flow=BaseFlow("sym:flow:testing:latest"),
            run=BaseRun("sym:run:12345-123:latest"),
            payload=BasePayload(
                user=BaseUser(
                    username="test@symops.io",
                    email="test@symops.io",
                    identities=[BaseUserIdentity(provider_name="slack", user_id="U1234567890")],
                )
            ),
        )

    @pytest.mark.parametrize("code, expected_values", TEST_SIMPLE_SLACK_CHANNELS_PARAMETERS)
    def test_simple_slack_channels(self, code, expected_values):
        with use_registry():
            exec(code, globals())

            lookup = get_extension("reducers", "get_approvers")
            assert lookup is not None

            result = lookup(None)
            assert result.lookup_type == expected_values["lookup_type"]
            assert result.lookup_keys == expected_values["lookup_keys"]
            assert result.allow_self == expected_values["allow_self"]

    def test_slack_group_with_users(self, event):
        with use_registry():
            exec(SLACK_GROUP_WITH_USERS_CODE, globals())

            lookup = get_extension("reducers", "get_approvers")
            assert lookup is not None

            result = lookup(event)
            assert result.lookup_type == SlackLookupType.EMAIL
            assert result.lookup_keys == ["test@symops.io"]

    def test_slack_user_id_lookup(self, event):
        with use_registry():
            exec(SIMPLE_SLACK_USER_ID_CODE, globals())

            lookup = get_extension("reducers", "get_approvers")
            assert lookup is not None

            result = lookup(event)
            assert result.lookup_type == SlackLookupType.USER_ID
            assert result.lookup_keys == ["U1234567890"]
            assert result.allow_self is False

    def test_allow_self(self):
        with use_registry():
            exec(SIMPLE_ALLOW_SELF_FALSE_CODE, globals())

            lookup = get_extension("reducers", "get_approvers")
            assert lookup is not None

            result = lookup(None)
            assert result.lookup_type == SlackLookupType.CHANNEL
            assert result.lookup_keys == ["#break-glass"]
            assert result.allow_self is False

        with use_registry():
            exec(SIMPLE_ALLOW_SELF_TRUE_CODE, globals())

            lookup = get_extension("reducers", "get_approvers")
            assert lookup is not None

            result = lookup(None)
            assert result.lookup_type == SlackLookupType.CHANNEL
            assert result.lookup_keys == ["#break-glass"]
            assert result.allow_self is True
