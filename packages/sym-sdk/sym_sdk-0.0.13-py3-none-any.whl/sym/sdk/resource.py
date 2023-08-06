"""Tools for describing Sym Resources."""

from typing import Optional, Union

import semver

from .errors import InvalidSemverError, InvalidSRNError


class SRN:
    """Sym Resource Name (:class:`~sym.sdk.sym_resource.SRN`) is a unique identifier for a Sym Resource.

    SRNs have the following structure::

        <ORG>:<MODEL>:<SLUG>:<VERSION>:<?IDENTIFIER>

    Where VERSION is either a semver string, or "latest".

    For example, the :class:`~sym.sdk.sym_resource.SRN` for the v1.0.0 sym:approval
    template is::

        sym:template:approval:1.0.0

    Or the :class:`~sym.sdk.sym_resource.SRN` for a :class:`~sym.sdk.flow.Flow`
    instance (with a UUID as an instance identifier) could be::

        sym:flow:test-flow:0.1.0:d47782bc-88be-44df-9e34-5fae0dbdea22
    """

    SEPARATOR = ":"

    def __init__(self, raw: str):
        self.raw = str(raw)

        srn_parts = self.raw.split(self.SEPARATOR)
        if len(srn_parts) < 4:
            raise InvalidSRNError(raw)

        self._org, self._model, self._slug, self._version, *self._rest = srn_parts

        if self._version and self._version != "latest":
            if not semver.VersionInfo.isvalid(self._version):
                raise InvalidSemverError(raw)

    def __str__(self):
        return self.raw

    def __hash__(self):
        return hash(self.raw)

    def __eq__(self, other):
        return self.raw == other.raw

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
        else:
            components.extend(self._rest)
        return self.__class__(self.SEPARATOR.join(components))

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
        try:
            return self._rest[0]
        except IndexError:
            return None


class SymResource:
    """A piece of infrastructure provisioned with
    Sym's `Terraform provider <https://docs.symops.com/docs/terraform-provider>`_.

    For example, a :class:`~sym.sdk.flow.Flow` is a Resource.

    Read more about `Sym Resources <https://docs.symops.com/docs/sym-concepts>`_.
    """

    def __init__(self, srn: Union[SRN, str]):
        self._srn = SRN(str(srn))

    def __getattr__(self, name: str):
        return getattr(self._srn, name)

    @property
    def srn(self) -> SRN:
        """A :class:`~sym.sdk.sym_resource.SRN` object that represents the unique identifier
        for this resource.
        """
        return self._srn
