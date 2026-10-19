# TaskFlow API 调用示例

以下示例假设服务运行在 `http://127.0.0.1:8080`。

## 创建任务

```bash
curl -X POST http://127.0.0.1:8080/api/tasks \
  -H 'Content-Type: application/json' \
  -d '{
    "title": "修复登录超时",
    "description": "JWT 过期时应返回 401",
    "status": "TODO",
    "priority": "HIGH",
    "dueAt": "2026-10-25T18:00:00"
  }'
```

成功返回 `201 Created`，响应包含 `id`、`version` 和审计时间。

## 按状态分页查询

```bash
curl 'http://127.0.0.1:8080/api/tasks?status=TODO&page=0&size=10'
```

响应结构：

```json
{
  "items": [],
  "page": 0,
  "size": 10,
  "totalElements": 0,
  "totalPages": 0
}
```

`page` 从 0 开始，`size` 范围为 1–100，默认按创建时间倒序。

## 更新任务

```bash
curl -X PATCH http://127.0.0.1:8080/api/tasks/1 \
  -H 'Content-Type: application/json' \
  -d '{"status":"DONE","priority":"MEDIUM"}'
```

成功响应中的 `version` 会递增，可用于后续乐观锁更新。

## 删除任务

```bash
curl -X DELETE http://127.0.0.1:8080/api/tasks/1
```

成功返回 `204 No Content`。

## 错误响应

```json
{
  "code": "VALIDATION_ERROR",
  "message": "Request validation failed",
  "fieldErrors": {
    "title": "title must not be blank"
  },
  "traceId": "1b0d2e5b-5c38-4e2e-8e31-4b0f0d8e7a10"
}
```

常见状态码：`400` 参数错误，`404` 任务不存在，`409` 乐观锁冲突，`500` 未预期异常。
