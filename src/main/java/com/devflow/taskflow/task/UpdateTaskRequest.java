package com.devflow.taskflow.task;

import jakarta.validation.constraints.Future;
import jakarta.validation.constraints.Pattern;
import jakarta.validation.constraints.Size;

import java.time.LocalDateTime;

public record UpdateTaskRequest(
        @Size(min = 1, max = 120, message = "title must be between 1 and 120 characters")
        @Pattern(regexp = ".*\\S.*", message = "title must not be blank")
        String title,

        @Size(max = 4000, message = "description must be at most 4000 characters")
        String description,

        TaskStatus status,

        TaskPriority priority,

        @Future(message = "dueAt must be in the future")
        LocalDateTime dueAt
) {
}
