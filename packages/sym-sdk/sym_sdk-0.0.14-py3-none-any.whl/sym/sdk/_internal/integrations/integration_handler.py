from abc import ABC, abstractmethod
from enum import Enum
from typing import Any, Dict, Optional, Type


class IntegrationType(Enum):
    UNSET = "unset"
    PAGERDUTY = "pagerduty"


class IntegrationHandler(ABC):
    integration_type = IntegrationType.UNSET

    api_key_location = None
    pagerduty_handler = None

    @classmethod
    def register_handler(cls, handler: Type["IntegrationHandler"]) -> None:
        setattr(cls, f"{handler.integration_type.value}_handler", handler)

    @classmethod
    def deregister_handler(cls, integration_type: IntegrationType) -> None:
        setattr(cls, f"{integration_type.value}_handler", None)

    @classmethod
    def get_handler(cls, integration_type: IntegrationType) -> "IntegrationHandler":
        handler = getattr(cls, f"{integration_type.value}_handler", None)
        if not handler:
            raise RuntimeError(f"Must register a working {integration_type.value} handler")
        return handler()

    @classmethod
    def set_api_key_location(cls, location: str) -> None:
        cls.api_key_location = location

    @classmethod
    def set_runtime_context(cls, context) -> None:
        cls.context = context

    @staticmethod
    def get_required_key_value(key: str, lookups: dict):
        val = lookups.get(key)
        if not val:
            raise KeyError(f"Must provide a non-trivial {key} value for handler")
        return val

    @abstractmethod
    def execute(self, method_name: str, parameter_lookups: Optional[Dict[str, Any]] = None):
        raise NotImplementedError
