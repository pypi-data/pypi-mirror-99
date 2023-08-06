from typing import Any, Dict, Optional

from .integration_handler import IntegrationHandler, IntegrationType


class PagerDutyMethod:
    IS_ON_CALL = "is_on_call"
    USERS_ON_CALL = "users_on_call"


class PagerDutyHandler(IntegrationHandler):
    """Stubs out functionality for external calls to the Pagerduty API.

    This handler should eventually be used to do client-side validation
    of custom code in place of the real Sym implementation making the API calls.

    For now, all functions are placeholders to map out real functionality
    that happens in the Sym runtime.
    """

    integration_type = IntegrationType.PAGERDUTY
    api_key_location = None

    def execute(self, method_name: str, parameter_lookups: Optional[Dict[str, Any]] = None):
        if not parameter_lookups:
            parameter_lookups = {}

        if method_name == PagerDutyMethod.IS_ON_CALL:
            return self._is_on_call(parameter_lookups)
        elif method_name == PagerDutyMethod.USERS_ON_CALL:
            return self._users_on_call(parameter_lookups)

        raise ValueError(f"PagerDutyHandler has no method {method_name}")

    def _is_on_call(self, lookups: Dict[str, Any]) -> bool:
        return False

    def _users_on_call(self, lookups: Dict[str, Any]) -> list:
        return []

    @classmethod
    def set_api_key_location(cls, location: str) -> None:
        cls.api_key_location = location

    @classmethod
    def set_runtime_context(cls, context) -> None:
        cls.context = context
