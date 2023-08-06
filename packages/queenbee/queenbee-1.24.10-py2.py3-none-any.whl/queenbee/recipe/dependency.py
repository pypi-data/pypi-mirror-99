"""Queenbee dependency class."""
from typing import Dict
from enum import Enum
from pydantic import Field, constr


from ..base.basemodel import BaseModel
from ..base.request import make_request, urljoin, resolve_local_source


class DependencyKind(str, Enum):
    """Dependency kind."""
    recipe = 'recipe'

    plugin = 'plugin'


class Dependency(BaseModel):
    """Configuration to fetch a Recipe or Plugin that another Recipe depends on."""
    type: constr(regex='^Dependency$') = 'Dependency'

    kind: DependencyKind = Field(
        ...,
        description='The kind of dependency. It can be a recipe or an '
        'plugin.'
    )

    name: str = Field(
        ...,
        description='Workflow name. This name should be unique among all the resources'
        ' in your resource. Use an alias if this is not the case.'
    )

    digest: str = Field(
        None,
        alias='hash',
        description='The digest hash of the dependency when retrieved from its source.'
        ' This is locked when the resource dependencies are downloaded.'
    )

    alias: str = Field(
        None,
        description='An optional alias to refer to this dependency. Useful if the name'
        ' is already used somewhere else.'
    )

    tag: str = Field(
        ...,
        description='Tag of the resource.'
    )

    source: str = Field(
        ...,
        description='URL to a repository where this resource can be found.',
        examples=[
            'https://registry.pollination.cloud/ladybugbot',
            'https://some-random-user.github.io/registry'
        ]
    )

    @property
    def dependency_kind(self):
        """Return a clean version of dependency kind.

        The value is either `recipe` or `plugin`.
        """
        return self.kind.split('_')[0]

    @property
    def is_locked(self) -> bool:
        """Indicates whether the dependency is locked to a specific digest.

        Returns:
            bool -- Boolean value to indicate whether the dependency is locked
        """
        return self.digest is not None

    @property
    def ref_name(self) -> str:
        """The name by which this dependency is referred to in the Recipe.

        Returns:
            str -- Either the dependency name or its alias
        """
        if self.alias is not None:
            return self.alias
        return self.name

    def _fetch_index(self, auth_header: Dict[str, str] = {}):
        """Fetch the source repository index object.

        Returns:
            RepositoryIndex -- A repository index
        """
        from ..repository.index import RepositoryIndex

        if self.source.startswith('file:'):
            url = resolve_local_source(self.source) + '/index.json'
        else:
            url = urljoin(self.source, 'index.json')

        res = make_request(url=url, auth_header=auth_header)

        raw_bytes = res.read()
        return RepositoryIndex.parse_raw(raw_bytes)

    def fetch(self, verify_digest: bool = True, auth_header: Dict[str, str] = {}) -> 'PackageVersion':
        """Fetch the dependency from its source

        Keyword Arguments:
            verify_digest {bool} -- If the dependency is locked, ensure the found
                manifest matches the saved digest (default: {True})

        Raises:
            ValueError: The dependency could not be found or was invalid

        Returns:
            bytes -- A byte string of the resource manifest
            str -- The digest hash of the package
            str -- The readme of the package
            str -- The license of the package
        """

        index = self._fetch_index(auth_header=auth_header)

        if self.digest is None:
            package_meta = index.package_by_tag(
                kind=self.dependency_kind,
                package_name=self.name,
                package_tag=self.tag
            )

            self.digest = package_meta.digest
        else:
            try:
                package_meta = index.package_by_digest(
                    kind=self.dependency_kind,
                    package_name=self.name,
                    package_digest=self.digest
                )
            except ValueError as error:
                # If hash does not exist then try to download
                # by tag. This is in the case where some package
                # owner overwrote the tag of the dependency
                if str(error) == f'No {self.dependency_kind} package with name ' \
                    f'{self.name} and digest {self.digest} exists in this index':
                    package_meta = index.package_by_tag(
                        kind=self.dependency_kind,
                        package_name=self.name,
                        package_tag=self.tag
                    )

                    self.digest = package_meta.digest
                else:
                    raise error

        return package_meta.fetch_package(
            source_url=self.source,
            verify_digest=verify_digest,
            auth_header=auth_header,
        )
