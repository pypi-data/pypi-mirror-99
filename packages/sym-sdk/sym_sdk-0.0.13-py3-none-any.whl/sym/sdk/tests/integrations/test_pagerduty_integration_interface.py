from unittest.mock import patch

import pytest

from sym.sdk._internal.annotations import get_extension, use_registry
from sym.sdk._internal.events import BaseEvent, BaseEventMeta, BasePayload
from sym.sdk._internal.flow import BaseFlow, BaseRun
from sym.sdk._internal.integrations import IntegrationHandler, IntegrationType, PagerDutyHandler
from sym.sdk._internal.user import BaseUser, BaseUserIdentity
from sym.sdk.integrations.slack import SlackLookupType
from sym.sdk.templates import ApprovalTemplate

from ..static.approvers_test_code import (
    SIMPLE_PAGERDUTY_IS_ON_CALL_CODE,
    SIMPLE_PAGERDUTY_IS_ON_CALL_SCHEDULE_CODE,
    SIMPLE_PAGERDUTY_USERS_ON_CALL_CODE,
    SIMPLE_PAGERDUTY_USERS_ON_CALL_SCHEDULE_CODE,
)


class TestPagerdutyInterface:
    @pytest.fixture
    def pagerduty_event(self):
        return BaseEvent(
            meta=BaseEventMeta("sym:event-spec:approval:1.0.0:request"),
            template=ApprovalTemplate("sym:template:approval:1.0.0"),
            flow=BaseFlow("sym:flow:testing:latest"),
            run=BaseRun("sym:run:12345-123:latest"),
            payload=BasePayload(
                user=BaseUser(
                    username="test@symops.io",
                    email="test@symops.io",
                    identities=[BaseUserIdentity(provider_name="pagerduty", user_id="U1234567890")],
                )
            ),
        )

    @pytest.mark.parametrize(
        "code", [SIMPLE_PAGERDUTY_IS_ON_CALL_CODE, SIMPLE_PAGERDUTY_IS_ON_CALL_SCHEDULE_CODE]
    )
    def test_pagerduty_is_on_call(self, code, pagerduty_event):
        try:
            IntegrationHandler.register_handler(PagerDutyHandler)

            with use_registry():
                exec(code, globals())
                lookup = get_extension("reducers", "get_approvers")

                # stub PagerDutyHandler always returns False for is_on_call
                result = lookup(pagerduty_event)
                assert result.lookup_type == SlackLookupType.CHANNEL
                assert result.lookup_keys == ["#not-on-call"]
                assert result.allow_self is False
        finally:
            IntegrationHandler.deregister_handler(IntegrationType.PAGERDUTY)

    @pytest.mark.parametrize(
        "code", [SIMPLE_PAGERDUTY_USERS_ON_CALL_CODE, SIMPLE_PAGERDUTY_USERS_ON_CALL_SCHEDULE_CODE]
    )
    @patch(
        "sym.sdk._internal.integrations.pagerduty_handler.PagerDutyHandler._users_on_call",
        return_value=["U1234567890"],
    )
    def test_pagerduty_users_on_call(self, mock_users_on_call, code, pagerduty_event):
        try:
            IntegrationHandler.register_handler(PagerDutyHandler)

            with use_registry():
                exec(code, globals())
                lookup = get_extension("reducers", "get_approvers")

                # TODO: mock the API call
                result = lookup(pagerduty_event)
                assert len(result) == 1
                assert result[0].lookup_type == SlackLookupType.USER
                assert result[0].lookup_keys == ["U1234567890"]
                assert result[0].allow_self is False
        finally:
            IntegrationHandler.deregister_handler(IntegrationType.PAGERDUTY)
