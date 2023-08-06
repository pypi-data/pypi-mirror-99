import pytest

from sym.sdk import ApprovalTemplate
from sym.sdk._internal.annotations import get_extension, use_registry
from sym.sdk._internal.events import BaseEvent, BaseEventMeta, BasePayload
from sym.sdk._internal.flow import BaseFlow, BaseRun
from sym.sdk._internal.user import BaseUser
from sym.sdk.integrations.slack import SlackLookupType

event_code = """
import datetime
from sym.sdk.annotations import reducer
from sym.sdk.integrations import slack
@reducer
def get_approvers(event):
    if event.fields["Urgency"] == "High":
        return slack.channel("#break-glass")

    if datetime.datetime.now().hour >= 17:
        return slack.user('@Ari Tang')
    else:
        return [slack.user(u) for u in ['@David Ruiz', '@Jon Demo']]
"""


class TestChannelsInterface:
    @pytest.fixture
    def event(self):
        return BaseEvent(
            meta=BaseEventMeta("sym:event-spec:approval:1.0.0:request"),
            template=ApprovalTemplate("sym:template:approval:1.0.0"),
            flow=BaseFlow("sym:flow:testing:latest"),
            run=BaseRun("sym:run:12345-123:latest"),
            payload=BasePayload(
                user=BaseUser(
                    username="John Van Jacques",
                    email="test@symops.io",
                    first_name="John",
                    last_name="Van Jacques",
                ),
                payload_data={"fields": {"Urgency": "High"}},
            ),
        )

    def test_basic_code(self, event):
        with use_registry():
            exec(event_code, globals())

            lookup = get_extension("reducers", "get_approvers")
            assert lookup is not None

            result = lookup(event)
            assert result.lookup_type == SlackLookupType.CHANNEL
            assert result.lookup_keys == ["#break-glass"]
