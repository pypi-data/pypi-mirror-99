from enum import Enum
from typing import Dict, List, Generator
from datetime import datetime

from pydantic import Field, constr

from ..base.basemodel import BaseModel
from ..io.inputs.job import JobArguments

class Job(BaseModel):
    """Queenbee Job.

    A Job is an object to submit a list of arguments to execute a Queenbee recipe.
    """
    api_version: constr(regex='^v1beta1$') = Field('v1beta1', readOnly=True)

    type: constr(regex='^Job$') = 'Job'

    source: str = Field(
        ...,
        description='The source url for downloading the recipe.'
    )

    arguments: List[List[JobArguments]] = Field(
        None,
        description='Input arguments for this job.'
    )

    name: str = Field(
        None,
        description='An optional name for this job. This name will be used a the '
        'display name for the run.'
    )

    description: str = Field(
        None,
        description='Run description.'
    )

    labels: Dict[str, str] = Field(
        None,
        description='Optional user data as a dictionary. User data is for user reference'
        ' only and will not be used in the execution of the job.'
    )


class JobStatusEnum(str, Enum):
    """Enumaration of allowable status strings"""

    # The job has been created
    created = 'Created'
    # The job folder is being prepared for execution and runs are being scheduled
    pre_processing = 'Pre-Processing'
    # Runs have been scheduled
    running = 'Running'
    # The job has failed to schedule runs
    failed = 'Failed'
    # The job has been cancelled by a user
    cancelled = 'Cancelled'
    # All runs have either succeeded or failed
    completed = 'Completed'
    # Could not determine the status of the job
    unknown = 'Unknown'


class JobStatus(BaseModel):
    """Parametric Job Status."""

    api_version: constr(regex='^v1beta1$') = Field('v1beta1', readOnly=True)

    type: constr(regex='^JobStatus$') = 'JobStatus'

    id: str = Field(
        ...,
        description='The ID of the individual job.'
    )

    status: JobStatusEnum = Field(
        JobStatusEnum.unknown,
        description='The status of this job.'
    )

    message: str = Field(
        None,
        description='Any message produced by the job. Usually error/debugging hints.'
    )

    started_at: datetime = Field(
        ...,
        description='The time at which the job was started'
    )

    finished_at: datetime = Field(
        None,
        description='The time at which the task was completed'
    )

    source: str = Field(
        None,
        description='Source url for the status object. It can be a recipe or a function.'
    )

    runs_pending: int = Field(
        0,
        description='The count of runs that are pending'
    )

    runs_running: int = Field(
        0,
        description='The count of runs that are running'
    )

    runs_completed: int = Field(
        0,
        description='The count of runs that have completed'
    )

    runs_failed: int = Field(
        0,
        description='The count of runs that have failed'
    )

    runs_cancelled: int =Field(
        0,
        description='The count of runs that have been cancelled'
    )

