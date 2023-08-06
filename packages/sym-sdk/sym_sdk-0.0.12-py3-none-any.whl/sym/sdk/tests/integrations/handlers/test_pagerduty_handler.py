from typing import Any, Dict, Optional

import pytest

from sym.sdk._internal.integrations import (
    IntegrationHandler,
    IntegrationType,
    PagerDutyHandler,
    PagerDutyMethod,
)


class MockPagerDutyHandlerMethod(IntegrationHandler):
    """Mock pagerduty handler to test multiple registrations"""

    integration_type = IntegrationType.PAGERDUTY

    def execute(self, method_name: str, parameter_lookups: Optional[Dict[str, Any]] = None):
        return method_name


class MockPagerDutyHandlerLookups(IntegrationHandler):
    """Mock pagerduty handler to test multiple registrations"""

    integration_type = IntegrationType.PAGERDUTY

    def execute(self, method_name: str, parameter_lookups: Optional[Dict[str, Any]] = None):
        return parameter_lookups


class TestPagerDutyHandler:
    @pytest.fixture
    def pagerduty_handler(self):
        IntegrationHandler.register_handler(PagerDutyHandler)
        yield IntegrationHandler.get_handler(IntegrationType.PAGERDUTY)
        IntegrationHandler.deregister_handler(IntegrationType.PAGERDUTY)

    def test_pagerduty_handler_unknown_method_name_errors(self, pagerduty_handler):
        with pytest.raises(ValueError, match="PagerDutyHandler has no method barnacle"):
            pagerduty_handler.execute(method_name="barnacle")

    def test_pagerduty_handler_is_on_call(self, pagerduty_handler):
        assert pagerduty_handler.execute(PagerDutyMethod.IS_ON_CALL) is False

    def test_pagerduty_handler_users_on_call(self, pagerduty_handler):
        assert pagerduty_handler.execute(PagerDutyMethod.USERS_ON_CALL) == []
