import pytest

from sym.sdk._internal.integrations import IntegrationHandler, IntegrationType

from .test_pagerduty_handler import MockPagerDutyHandlerLookups, MockPagerDutyHandlerMethod


class TestIntegrationHandler:
    def test_handler_registration(self):
        with pytest.raises(
            RuntimeError, match=f"Must register a working {IntegrationType.PAGERDUTY.value} handler"
        ):
            IntegrationHandler.get_handler(IntegrationType.PAGERDUTY)

        IntegrationHandler.register_handler(MockPagerDutyHandlerMethod)
        assert IntegrationHandler.pagerduty_handler == MockPagerDutyHandlerMethod

        handler = IntegrationHandler.get_handler(IntegrationType.PAGERDUTY)
        assert isinstance(handler, MockPagerDutyHandlerMethod)

        IntegrationHandler.register_handler(MockPagerDutyHandlerLookups)
        assert IntegrationHandler.pagerduty_handler == MockPagerDutyHandlerLookups

        handler = IntegrationHandler.get_handler(IntegrationType.PAGERDUTY)
        assert isinstance(handler, MockPagerDutyHandlerLookups)

        IntegrationHandler.deregister_handler(IntegrationType.PAGERDUTY)
        assert IntegrationHandler.pagerduty_handler is None
