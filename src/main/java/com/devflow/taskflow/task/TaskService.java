package com.devflow.taskflow.task;

import com.devflow.taskflow.common.PageResponse;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.PageRequest;
import org.springframework.data.domain.Pageable;
import org.springframework.data.domain.Sort;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

@Service
public class TaskService {

    private final TaskRepository repository;

    public TaskService(TaskRepository repository) {
        this.repository = repository;
    }

    @Transactional
    public TaskResponse create(CreateTaskRequest request) {
        Task task = new Task(
                request.title().trim(),
                request.description(),
                request.status() == null ? TaskStatus.TODO : request.status(),
                request.priority() == null ? TaskPriority.MEDIUM : request.priority(),
                request.dueAt()
        );
        return TaskResponse.from(repository.saveAndFlush(task));
    }

    @Transactional(readOnly = true)
    public PageResponse<TaskResponse> list(TaskStatus status, TaskPriority priority, int page, int size) {
        Pageable pageable = PageRequest.of(
                page,
                size,
                Sort.by(Sort.Order.desc("createdAt"), Sort.Order.desc("id"))
        );
        Page<Task> tasks;
        if (status != null && priority != null) {
            tasks = repository.findByStatusAndPriority(status, priority, pageable);
        } else if (status != null) {
            tasks = repository.findByStatus(status, pageable);
        } else if (priority != null) {
            tasks = repository.findByPriority(priority, pageable);
        } else {
            tasks = repository.findAll(pageable);
        }
        return PageResponse.from(tasks.map(TaskResponse::from));
    }

    @Transactional(readOnly = true)
    public TaskResponse get(long id) {
        return TaskResponse.from(find(id));
    }

    @Transactional
    public TaskResponse update(long id, UpdateTaskRequest request) {
        Task task = find(id);
        if (request.title() != null) {
            task.changeTitle(request.title().trim());
        }
        if (request.description() != null) {
            task.changeDescription(request.description());
        }
        if (request.status() != null) {
            task.changeStatus(request.status());
        }
        if (request.priority() != null) {
            task.changePriority(request.priority());
        }
        if (request.dueAt() != null) {
            task.changeDueAt(request.dueAt());
        }
        return TaskResponse.from(repository.saveAndFlush(task));
    }

    @Transactional
    public void delete(long id) {
        repository.delete(find(id));
    }

    private Task find(long id) {
        return repository.findById(id).orElseThrow(() -> new TaskNotFoundException(id));
    }
}
