from sym.sdk._internal.annotations import get_extension, use_registry
from sym.sdk.integrations.slack import SlackLookupType

simplest_code = """
from sym.sdk.annotations import reducer
from sym.sdk.integrations import slack

@reducer
def get_approvers(event):
    return slack.channel('#managers')
"""


class TestChannelsInterface:
    def test_basic_code(self):
        with use_registry():
            exec(simplest_code, globals())

            lookup = get_extension("reducers", "get_approvers")
            assert lookup is not None
            result = lookup(None)
            assert result.lookup_type == SlackLookupType.CHANNEL
            assert result.lookup_keys == ["#managers"]
