"""Tools for describing Sym Resources."""

import re
from typing import List, Optional, Tuple, Union

from .errors import InvalidSRNError, SRNTrailingSeparatorError


class SRN:
    """Sym Resource Name (:class:`~sym.sdk.sym_resource.SRN`) is a unique identifier for a Sym Resource.

    SRNs have the following structure::

        <ORG>:<MODEL>:<SLUG>:<VERSION>[:<IDENTIFIER>]

    Where VERSION is either a semver string, or "latest".

    For example, the :class:`~sym.sdk.sym_resource.SRN` for the v1.0.0 sym:approval
    template is::

        sym:template:approval:1.0.0

    Or the :class:`~sym.sdk.sym_resource.SRN` for a :class:`~sym.sdk.flow.Flow`
    instance (with a UUID as an instance identifier) could be::

        sym:flow:test-flow:0.1.0:d47782bc-88be-44df-9e34-5fae0dbdea22
    """

    SEPARATOR = ":"

    ORG_REGEX = re.compile(r"^[a-zA-Z0-9-]+$")
    MODEL_REGEX = re.compile(r"^[a-zA-Z0-9-]+$")
    SLUG_REGEX = re.compile(r"^[a-zA-Z0-9-]+$")
    VERSION_REGEX = re.compile(r"^(latest|[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3})$")
    ID_REGEX = re.compile(r"^[a-zA-Z0-9-]+$")

    def __init__(
        self, org: str, model: str, slug: str, version: str, identifier: Optional[str] = None
    ):
        self._org = org
        self._model = model
        self._slug = slug
        self._version = version
        self._identifier = identifier

    def __str__(self):
        identifier_part = f":{self._identifier}" if self._identifier else ""
        return f"{self._org}:{self._model}:{self._slug}:{self._version}{identifier_part}"

    def __hash__(self):
        return hash(str(self))

    def __eq__(self, other):
        return (
            self._org == other._org
            and self._model == other._model
            and self._slug == other._slug
            and self._version == other._version
            and self._identifier == other._identifier
        )

    @classmethod
    def parse(cls, raw: str) -> Tuple[str, str, str, str, Optional[str]]:
        """Validates the given string as an SRN

        Args:
            raw: A raw SRN string

        Returns:
            A tuple of the components of the SRN

        Raises:
            SRNTrailingSeparatorError:   The SRN has a trailing separator
            InvalidSRNError:             The SRN is missing components, or at least one component is invalid
        """
        if raw.endswith(cls.SEPARATOR):
            raise SRNTrailingSeparatorError(raw)

        parts = raw.split(cls.SEPARATOR)
        if len(parts) < 4:
            raise InvalidSRNError(
                raw, f"An SRN must have at least 4 components separated by '{cls.SEPARATOR}'."
            )

        identifier = parts[4] if len(parts) == 5 else None

        patterns = [
            cls.ORG_REGEX,
            cls.MODEL_REGEX,
            cls.SLUG_REGEX,
            cls.VERSION_REGEX,
            cls.ID_REGEX if identifier else None,
        ]
        names = ["org", "model", "slug", "version", "identifier" if identifier else None]

        # Check each component with its regex
        match_pairs = [
            (name, pattern.match(part))
            for part, pattern, name in zip(parts, patterns, names)
            if name and pattern
        ]
        invalid_parts = [name for name, match in match_pairs if not match]

        if len(invalid_parts) > 0:  # Some parts of the SRN are invalid
            message = f"The invalid parts were: {str(invalid_parts)}"
            raise InvalidSRNError(raw, message)

        # Must return a 5-tuple
        if identifier:
            org, model, slug, version, identifier = parts
        else:
            org, model, slug, version = parts  # identifier remains as None from above

        return org, model, slug, version, identifier

    @classmethod
    def from_string(cls, raw: str) -> "SRN":
        """Constructs an :class:`~sym.sdk.resource.SRN` from a string"""
        org, model, slug, version, identifier = cls.parse(raw)

        return cls(org, model, slug, version, identifier)

    def copy(
        self,
        organization: Optional[str] = None,
        model: Optional[str] = None,
        slug: Optional[str] = None,
        version: Optional[str] = None,
        identifier: Optional[str] = None,
    ):
        """Creates a copy of this :class:`~sym.sdk.sym_resource.SRN`.

        Optionally can create a new :class:`~sym.sdk.sym_resource.SRN` with
        modified components from the current, as specified by the keyword arguments.
        """

        components = [
            organization or self._org,
            model or self._model,
            slug or self._slug,
            version or self._version,
        ]
        if identifier:
            components.append(identifier)
        elif self._identifier:
            components.append(self._identifier)

        return self.__class__(*components)

    @property
    def organization(self) -> str:
        """The slug for the organization this :class:`~sym.sdk.sym_resource.SRN`
        belongs to.

        For example, for the sym:approval :class:`~sym.sdk.templates.Template`,
        the organization slug is `sym`.
        """

        return self._org

    @property
    def model(self) -> str:
        """The model name for this :class:`~sym.sdk.sym_resource.SRN`.

        For example, for the sym:approval :class:`~sym.sdk.templates.Template`,
        the model name is `template`.
        """

        return self._model

    @property
    def slug(self) -> str:
        """This :class:`~sym.sdk.sym_resource.SRN`'s slug.

        For example, for the sym:approval :class:`~sym.sdk.templates.Template`, the slug is `approval`.
        """
        return self._slug

    @property
    def version(self) -> str:
        """A semver string representing the version of this :class:`~sym.sdk.sym_resource.SRN`.

        For example, the first version of the sym:approval :class:`~sym.sdk.templates.Template`
        is `1.0.0`.
        """

        return self._version

    @property
    def identifier(self) -> Optional[str]:
        """An arbitrary string identifying an instance of the resource.

        This is often a UUID.
        """
        return self._identifier


class SymResource:
    """A piece of infrastructure provisioned with
    Sym's `Terraform provider <https://docs.symops.com/docs/terraform-provider>`_.

    For example, a :class:`~sym.sdk.flow.Flow` is a Resource.

    Read more about `Sym Resources <https://docs.symops.com/docs/sym-concepts>`_.
    """

    def __init__(self, srn: Union[SRN, str]):
        self._srn = SRN.from_string(str(srn))

    def __getattr__(self, name: str):
        return getattr(self._srn, name)

    @property
    def srn(self) -> SRN:
        """A :class:`~sym.sdk.sym_resource.SRN` object that represents the unique identifier
        for this resource.
        """
        return self._srn
