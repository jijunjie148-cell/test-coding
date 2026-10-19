class TaskNotFoundError(Exception):
    def __init__(self, task_id: int) -> None:
        super().__init__(f"Task {task_id} was not found")
        self.task_id = task_id


class VersionConflictError(Exception):
    def __init__(self) -> None:
        super().__init__("The task was modified by another request; reload and retry")
