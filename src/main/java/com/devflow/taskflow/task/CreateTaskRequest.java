package com.devflow.taskflow.task;

import jakarta.validation.constraints.Future;
import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.Size;

import java.time.LocalDateTime;

public record CreateTaskRequest(
        @NotBlank(message = "title must not be blank")
        @Size(max = 120, message = "title must be at most 120 characters")
        String title,

        @Size(max = 4000, message = "description must be at most 4000 characters")
        String description,

        TaskStatus status,

        TaskPriority priority,

        @Future(message = "dueAt must be in the future")
        LocalDateTime dueAt
) {
}
