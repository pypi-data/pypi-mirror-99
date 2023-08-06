from datetime import datetime
from typing import Any, Dict, Optional

from sym.sdk import Event, EventMeta, Flow, Payload, Run, Template, User


class BasePayload(Payload):
    def __init__(self, user: User, payload_data: Optional[dict] = None):
        self._user = user
        self._data = payload_data or {}

        # TODO make sure timestamp_iso8601 gets converted to datetime properly
        self._timestamp = self._data.get("timestamp_iso8601") or datetime.utcnow()
        self._fields = self._data.get("fields") or {}
        self._event_name = self._data.get("event_name") or ""

    @property
    def timestamp(self) -> datetime:
        return self._timestamp

    @property
    def fields(self) -> Dict[str, Any]:
        return self._fields

    @property
    def srn(self):
        raise NotImplementedError

    @property
    def user(self) -> User:
        return self._user

    @property
    def actors(self) -> Dict[str, User]:
        raise NotImplementedError

    @property
    def event_name(self) -> str:
        return self._event_name


class BaseEventMeta(EventMeta):
    pass


class BaseEvent(Event):
    def __init__(self, meta: EventMeta, template: Template, flow: Flow, run: Run, payload: Payload):
        self._meta = meta
        self._template = template
        self._flow = flow
        self._run = run
        self._payload = payload

    @property
    def payload(self) -> Payload:
        return self._payload

    @property
    def meta(self) -> EventMeta:
        return self._meta

    @property
    def template(self) -> Template:
        return self._template

    @property
    def flow(self) -> Flow:
        return self._flow

    @property
    def run(self) -> Run:
        return self._run

    @property
    def name(self) -> str:
        return self._payload.event_name

    @property
    def actors(self) -> Dict[str, User]:
        raise NotImplementedError

    @property
    def fields(self) -> Dict[str, Any]:
        return self._payload.fields

    @property
    def user(self) -> User:
        return self._payload.user
