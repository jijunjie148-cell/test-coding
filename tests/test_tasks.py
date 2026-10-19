from datetime import datetime, timedelta


def create_task(client, title="待办任务", status="TODO", priority="MEDIUM"):
    response = client.post(
        "/api/tasks",
        json={
            "title": title,
            "status": status,
            "priority": priority,
            "due_at": (datetime.now() + timedelta(days=2)).isoformat(),
        },
    )
    assert response.status_code == 201, response.text
    return response.json()


def test_creates_task_with_defaults(client):
    response = client.post("/api/tasks", json={"title": "修复登录超时"})
    assert response.status_code == 201
    body = response.json()
    assert body["title"] == "修复登录超时"
    assert body["status"] == "TODO"
    assert body["priority"] == "MEDIUM"
    assert body["version"] == 1


def test_rejects_blank_title(client):
    response = client.post("/api/tasks", json={"title": "   "})
    assert response.status_code == 422


def test_rejects_past_due_date(client):
    response = client.post(
        "/api/tasks",
        json={"title": "过期任务", "due_at": "2000-01-01T00:00:00"},
    )
    assert response.status_code == 422


def test_filters_by_status_and_paginates(client):
    create_task(client, "待办一", "TODO", "HIGH")
    create_task(client, "待办二", "TODO", "LOW")
    create_task(client, "已完成", "DONE", "MEDIUM")

    response = client.get(
        "/api/tasks",
        params={"status": "TODO", "page": 0, "size": 1},
    )
    assert response.status_code == 200
    body = response.json()
    assert len(body["items"]) == 1
    assert body["total_elements"] == 2
    assert body["total_pages"] == 2
    assert body["page"] == 0
    assert body["size"] == 1


def test_rejects_invalid_page_size(client):
    response = client.get("/api/tasks", params={"size": 0})
    assert response.status_code == 422


def test_returns_not_found_for_missing_task(client):
    response = client.get("/api/tasks/999999")
    assert response.status_code == 404
    assert response.json()["code"] == "TASK_NOT_FOUND"


def test_patch_updates_task_and_increments_version(client):
    created = create_task(client, "初始标题", "TODO", "LOW")

    response = client.patch(
        f"/api/tasks/{created['id']}",
        json={"title": "更新后的标题", "status": "DONE", "priority": "HIGH"},
    )
    assert response.status_code == 200
    body = response.json()
    assert body["title"] == "更新后的标题"
    assert body["status"] == "DONE"
    assert body["priority"] == "HIGH"
    assert body["version"] == created["version"] + 1


def test_deletes_task_and_then_returns_not_found(client):
    created = create_task(client, "待删除")
    task_id = created["id"]

    assert client.delete(f"/api/tasks/{task_id}").status_code == 204
    assert client.get(f"/api/tasks/{task_id}").status_code == 404
