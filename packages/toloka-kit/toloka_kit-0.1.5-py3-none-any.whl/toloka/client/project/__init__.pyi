from datetime import datetime
from enum import Enum
from typing import Any, Dict, Optional

from ..primitives.base import BaseTolokaObject
from .task_spec import TaskSpec
from ..quality_control import QualityControl


class Project(BaseTolokaObject):
    """In a project, you set properties for tasks and responses:

    * Input data parameters. These parameters describe the objects to display in a task, such as images or text.
    * Output data parameters. These parameters describe users' responses. They are used for validating the
        responses entered: the data type (integer, string, etc.), range of values, string length, and so on.
    * Task interface. For more information about how to define the appearance of tasks, see the document
        Toloka. requester's guide.
    Attributes:
        public_name: Name of the project. Visible to users.
        public_description: Description of the project. Visible to users.
        public_instructions: Instructions for completing the task. You can use any HTML markup in the instructions.
        private_comment: Comments about the project. Visible only to the requester.
        task_spec: Parameters for input and output data and the task interface.
        assignments_issuing_type: How to assign tasks. The default value is AUTOMATED.
        assignments_automerge_enabled: Solve merging identical tasks in the project.
        max_active_assignments_count: The number of task suites the user can complete simultaneously (“Active” status)
        quality_control: The quality control rule.
        status: Project status.
        created: The UTC date and time the project was created.
        id: Project ID (assigned automatically).
        public_instructions: Instructions for completing tasks. You can use any HTML markup in the instructions.
        private_comment: Comment on the project. Available only to the customer.
    """

    class AssignmentsIssuingType(Enum):
        """How to assign tasks:

        * AUTOMATED — The user is assigned a task suite from the pool. You can configure the order
                for assigning task suites.
        * MAP_SELECTOR — The user chooses a task suite on the map. If you are using MAP_SELECTOR,
            specify the text to display in the map name and description in the assignments_issuing_view_config key:
            "assignments_issuing_view_config": {
               "title_template": "<task name>",
               "description_template": "<brief description of the task>"
            }
        """
        ...

    class ProjectStatus(Enum):
        """Project status:

        * ACTIVE
        * ARCHIVED
        """
        ...

    class AssignmentsIssuingViewConfig(BaseTolokaObject):

        def __repr__(self): ...

        def __str__(self): ...

        def __eq__(self, other): ...

        def __ne__(self, other): ...

        def __lt__(self, other): ...

        def __le__(self, other): ...

        def __gt__(self, other): ...

        def __ge__(self, other): ...

        def __init__(
            self,*,
            title_template: Optional[str] = ...,
            description_template: Optional[str] = ...
        ) -> None: ...

        _unexpected: Optional[Dict[str, Any]]
        title_template: Optional[str]
        description_template: Optional[str]

    def __attrs_post_init__(self): ...

    def __repr__(self): ...

    def __str__(self): ...

    def __eq__(self, other): ...

    def __ne__(self, other): ...

    def __lt__(self, other): ...

    def __le__(self, other): ...

    def __gt__(self, other): ...

    def __ge__(self, other): ...

    def __init__(
        self,*,
        public_name: Optional[str] = ...,
        public_description: Optional[str] = ...,
        task_spec: Optional[TaskSpec] = ...,
        assignments_issuing_type: Optional[AssignmentsIssuingType] = ...,
        assignments_issuing_view_config: Optional[AssignmentsIssuingViewConfig] = ...,
        assignments_automerge_enabled: Optional[bool] = ...,
        max_active_assignments_count: Optional[int] = ...,
        quality_control: Optional[QualityControl] = ...,
        status: Optional[ProjectStatus] = ...,
        created: Optional[datetime] = ...,
        id: Optional[str] = ...,
        public_instructions: Optional[str] = ...,
        private_comment: Optional[str] = ...
    ) -> None: ...

    _unexpected: Optional[Dict[str, Any]]
    public_name: Optional[str]
    public_description: Optional[str]
    task_spec: Optional[TaskSpec]
    assignments_issuing_type: Optional[AssignmentsIssuingType]
    assignments_issuing_view_config: Optional[AssignmentsIssuingViewConfig]
    assignments_automerge_enabled: Optional[bool]
    max_active_assignments_count: Optional[int]
    quality_control: Optional[QualityControl]
    status: Optional[ProjectStatus]
    created: Optional[datetime]
    id: Optional[str]
    public_instructions: Optional[str]
    private_comment: Optional[str]
