"""Helpers for interacting with the PagerDuty API."""

from typing import List, Optional

from sym.sdk._internal.integrations import (
    HandlerParameters,
    IntegrationHandler,
    IntegrationType,
    PagerDutyMethod,
)
from sym.sdk._internal.utils import wrap_with_error
from sym.sdk.errors import PagerDutyError
from sym.sdk.user import User


@wrap_with_error(PagerDutyError)
def is_on_call(
    user: User,
    escalation_policy_name: Optional[str] = None,
    escalation_policy_id: Optional[str] = None,
    schedule_name: Optional[str] = None,
    schedule_id: Optional[str] = None,
) -> bool:
    """Check if the provided user is currently on-call according to PagerDuty.

    If a name or ID is provided for either escalation policy or schedule, check if the user is
    on-call for specified escalation policy or schedule.

    If no name or ID is provided for either escalation policy or schedule, check if the user is
    on-call for ANY escalation policy or schedule.
    """
    handler = IntegrationHandler.get_handler(IntegrationType.PAGERDUTY)
    return handler.execute(
        method_name=PagerDutyMethod.IS_ON_CALL,
        parameter_lookups={
            HandlerParameters.USER: user,
            HandlerParameters.ESCALATION_POLICY_NAME: escalation_policy_name,
            HandlerParameters.ESCALATION_POLICY_IDS: [escalation_policy_id]
            if escalation_policy_id
            else [],
            HandlerParameters.SCHEDULE_NAME: schedule_name,
            HandlerParameters.SCHEDULE_IDS: [schedule_id] if schedule_id else [],
        },
    )


@wrap_with_error(PagerDutyError)
def users_on_call(
    escalation_policy_name: Optional[str] = None,
    escalation_policy_id: Optional[str] = None,
    schedule_name: Optional[str] = None,
    schedule_id: Optional[str] = None,
) -> List[User]:
    """Get all on-call users for the specified escalation policy or schedule from PagerDuty.

    Escalation policy or schedule can be specified by name or ID. If none are provided, returns
    on-call users for ALL escalation policies + schedules.
    """
    handler = IntegrationHandler.get_handler(IntegrationType.PAGERDUTY)
    return handler.execute(
        method_name=PagerDutyMethod.USERS_ON_CALL,
        parameter_lookups={
            HandlerParameters.ESCALATION_POLICY_NAME: escalation_policy_name,
            HandlerParameters.ESCALATION_POLICY_IDS: [escalation_policy_id]
            if escalation_policy_id
            else [],
            HandlerParameters.SCHEDULE_NAME: schedule_name,
            HandlerParameters.SCHEDULE_IDS: [schedule_id] if schedule_id else [],
        },
    )
