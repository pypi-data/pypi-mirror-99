from typing import Any, Dict, Optional

from sym.sdk import Flow, Run, User


class BaseFlow(Flow):
    def __init__(
        self,
        srn: str,
        fields: Optional[Dict[str, Any]] = None,
        environment: Optional[Dict[str, Any]] = None,
        vars: Optional[Dict[str, str]] = None,
    ):
        super().__init__(srn)

        self._fields = fields or {}
        self._environment = environment or {}
        self._vars = vars or {}

    @property
    def fields(self) -> Dict[str, Any]:
        return self._fields

    @property
    def environment(self) -> Dict[str, Any]:
        return self._environment

    @property
    def vars(self) -> Dict[str, str]:
        return self._vars


class BaseRun(Run):
    def __init__(self, srn: str):
        super().__init__(srn)

    @property
    def actors(self) -> Dict[str, User]:
        raise NotImplementedError
