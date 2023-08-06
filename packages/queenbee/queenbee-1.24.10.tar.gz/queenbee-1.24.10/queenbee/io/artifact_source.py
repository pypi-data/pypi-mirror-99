"""Queenbee ArtifactSource class.

ArtifactSource is a configuration to a source system to acquire artifacts from.

"""
from typing import Dict, List
from pydantic import Field, constr

from ..base.basemodel import BaseModel
from ..io.reference import references_from_string


class _ArtifactSource(BaseModel):
    """ArtifactSource.

    An Artifact Source System.
    """
    type: constr(regex='^_ArtifactSource$') = '_ArtifactSource'

    @staticmethod
    def _referenced_values(values: list = []) -> Dict[str, List[str]]:
        """Get referenced variables if any"""
        ref_values = {}

        if values == []:
            return ref_values

        for value in values:
            if value is None:
                continue
            ref_var = references_from_string(value)
            if ref_var:
                ref_values[value] = ref_var

        return ref_values

    @property
    def referenced_values(self) -> Dict[str, List[str]]:
        return self._referenced_values()


class ProjectFolder(_ArtifactSource):
    """Project Folder Source

    This is the path to a folder where files and folders can be sourced. In the context
    of a desktop run Workflow this folder will correspond to a local folder. In the
    context of a workflow run on Pollination this folder will correspond to a Project
    scoped folder.
    """
    type: constr(regex='^ProjectFolder$') = 'ProjectFolder'

    path: str = Field(
        None,
        description='The path to a folder where files and folders can be sourced. For a '
        'local filesystem this can be "C:\\Users\\me\\jobs\\test".'
    )

    @property
    def referenced_values(self) -> Dict[str, List[str]]:
        """Get referenced variables if any.

        Returns:
            Dict[str, List[str]] -- A dictionary where keys are attributes and values
                are lists contain referenced value string.
        """
        return self._referenced_values(['path'])


class HTTP(_ArtifactSource):
    """HTTP Source

    A web HTTP to an FTP server or an API for example.
    """

    type: constr(regex='^HTTP$') = 'HTTP'

    url: str = Field(
        ...,
        description="For a HTTP endpoint this can be http://climate.onebuilding.org."
    )

    @property
    def referenced_values(self) -> Dict[str, List[str]]:
        values = [self.url]

        return self._referenced_values(values)


class S3(_ArtifactSource):
    """S3 Source

    An S3 bucket artifact Source.
    """

    type: constr(regex='^S3$') = 'S3'

    key: str = Field(
        ...,
        description="The path inside the bucket to source artifacts from."
    )

    endpoint: str = Field(
        ...,
        description="The HTTP endpoint to reach the S3 bucket."
    )

    bucket: str = Field(
        ...,
        description="The name of the S3 bucket on the host server."
    )

    credentials_path: str = Field(
        None,
        description="Path to the file holding the AccessKey and SecretAccessKey to "
        "authenticate to the bucket. Assumes public bucket access if none are specified."
    )

    @property
    def referenced_values(self) -> Dict[str, List[str]]:
        values = [self.key, self.endpoint, self.bucket, self.credentials_path]

        return self._referenced_values(values)
