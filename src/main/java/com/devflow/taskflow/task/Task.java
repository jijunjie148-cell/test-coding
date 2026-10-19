package com.devflow.taskflow.task;

import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.EnumType;
import jakarta.persistence.Enumerated;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.GenerationType;
import jakarta.persistence.Id;
import jakarta.persistence.Index;
import jakarta.persistence.PrePersist;
import jakarta.persistence.PreUpdate;
import jakarta.persistence.Table;
import jakarta.persistence.Version;

import java.time.LocalDateTime;
import java.time.ZoneId;

@Entity
@Table(name = "tasks", indexes = {
        @Index(name = "idx_tasks_status_due_at", columnList = "status, due_at"),
        @Index(name = "idx_tasks_priority_created_at", columnList = "priority, created_at"),
        @Index(name = "idx_tasks_created_at", columnList = "created_at")
})
public class Task {

    private static final ZoneId APP_ZONE = ZoneId.of("Asia/Shanghai");

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(nullable = false, length = 120)
    private String title;

    @Column(columnDefinition = "TEXT")
    private String description;

    @Enumerated(EnumType.STRING)
    @Column(nullable = false, length = 20)
    private TaskStatus status;

    @Enumerated(EnumType.STRING)
    @Column(nullable = false, length = 20)
    private TaskPriority priority;

    @Column(name = "due_at")
    private LocalDateTime dueAt;

    @Version
    @Column(nullable = false)
    private Long version;

    @Column(name = "created_at", nullable = false, updatable = false)
    private LocalDateTime createdAt;

    @Column(name = "updated_at", nullable = false)
    private LocalDateTime updatedAt;

    protected Task() {
    }

    public Task(String title, String description, TaskStatus status, TaskPriority priority, LocalDateTime dueAt) {
        this.title = title;
        this.description = description;
        this.status = status;
        this.priority = priority;
        this.dueAt = dueAt;
    }

    @PrePersist
    void onCreate() {
        LocalDateTime now = LocalDateTime.now(APP_ZONE);
        createdAt = now;
        updatedAt = now;
    }

    @PreUpdate
    void onUpdate() {
        updatedAt = LocalDateTime.now(APP_ZONE);
    }

    public void changeTitle(String title) {
        this.title = title;
    }

    public void changeDescription(String description) {
        this.description = description;
    }

    public void changeStatus(TaskStatus status) {
        this.status = status;
    }

    public void changePriority(TaskPriority priority) {
        this.priority = priority;
    }

    public void changeDueAt(LocalDateTime dueAt) {
        this.dueAt = dueAt;
    }

    public Long getId() {
        return id;
    }

    public String getTitle() {
        return title;
    }

    public String getDescription() {
        return description;
    }

    public TaskStatus getStatus() {
        return status;
    }

    public TaskPriority getPriority() {
        return priority;
    }

    public LocalDateTime getDueAt() {
        return dueAt;
    }

    public Long getVersion() {
        return version;
    }

    public LocalDateTime getCreatedAt() {
        return createdAt;
    }

    public LocalDateTime getUpdatedAt() {
        return updatedAt;
    }
}
