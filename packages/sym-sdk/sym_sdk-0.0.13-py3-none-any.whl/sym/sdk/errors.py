"""Common errors that can be thrown."""

from typing import Optional


class SymSDKError(Exception):
    """The base exception class used by Sym's SDK."""

    # To ensure all user-facing errors are informative and actionable,
    # all SymSDKErrors are required to have an error message, a hint as to
    # the next step a user should take, and a relevant link to Sym documentation.
    def __init__(self, message: str, hint: str, doc_url: str, **kwargs):
        self.message = message
        self.hint = hint
        self.doc_url = doc_url
        super().__init__(message, **kwargs)

    def __str__(self):
        return (
            f"{self.message}\n\nHint: {self.hint}\n\nFor more details, please see: {self.doc_url}"
        )

    def format_slack(self) -> str:
        """Returns a string representation of this error formatted for display
        in Slack's markdown.
        """

        return f"*{self.message}*\n\n*Hint:* {self.hint}\n\nFor more details, please see: {self.doc_url}."


class SymIntegrationError(SymSDKError):
    """Raised when there is an error in an Integration."""


class PagerDutyError(SymIntegrationError):
    """Raised when the PagerDuty API throws an error."""

    def __init__(
        self,
        message: Optional[str] = None,
        hint: Optional[str] = None,
        doc_url: Optional[str] = None,
    ):
        if message and hint and doc_url:
            super().__init__(message=message, hint=hint, doc_url=doc_url)
        else:
            super().__init__(
                message="An unexpected error occurred while trying to connect to PagerDuty.",
                hint="Sym Support has been notified of this issue and should be reaching out shortly.",
                doc_url="https://docs.symops.com/docs/support",
            )


class SlackError(SymIntegrationError):
    """Raised when Slack's API throws an error."""

    def __init__(
        self,
        message: Optional[str] = None,
        hint: Optional[str] = None,
        doc_url: Optional[str] = None,
    ):
        if message and hint and doc_url:
            super().__init__(message=message, hint=hint, doc_url=doc_url)
        else:
            super().__init__(
                message="An unexpected error occurred while trying to connect to Slack.",
                hint="Sym Support has been notified of this issue and should be reaching out shortly.",
                doc_url="https://docs.symops.com/docs/support",
            )


class SlackTimeoutError(SlackError):
    """Raised when Slack's API times out."""

    def __init__(self):
        super().__init__(
            message="Sym timed out while trying to connect to Slack.",
            hint="Try again in a few seconds. Please reach out to support@symops.io if this issue persists.",
            doc_url="https://docs.symops.com/docs/support",
        )


class InvalidSRNError(SymSDKError):
    """Raised when an invalid SRN is supplied."""

    def __init__(self, srn: str):
        super().__init__(
            message=f"SRN {srn} is not valid.",
            hint="SRNs must match the following structure: <ORG>:<MODEL>:<SLUG>:<VERSION>:<?IDENTIFIER>, where org, model, slug, and version are required.",
            doc_url="https://docs.symops.com/docs/sym-concepts",
        )


class InvalidSemverError(InvalidSRNError):
    """Raised when an invalid version is provided."""

    def __init__(self, srn: str):
        super(InvalidSRNError, self).__init__(
            message=f"SRN {srn} is not valid.",
            hint="The VERSION of a SRN must be valid semver, or the string 'latest'.",
            doc_url="https://docs.symops.com/docs/sym-concepts",
        )
