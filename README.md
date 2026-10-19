# TaskFlow API

一个用于 DevFlow AI 分析演示的 Python 任务管理服务。项目包含真实 REST API、MySQL 迁移、参数校验、统一错误响应、乐观锁、分页筛选、自动化测试和 GitHub Actions。

## 技术栈

- Python 3.12
- FastAPI
- SQLAlchemy 2.0
- PyMySQL
- MySQL 8
- Alembic
- pytest + httpx

## 数据设计

`tasks` 表存储任务标题、描述、状态、优先级、截止时间和版本号。

- 主键使用自增 `INTEGER`
- `version` 用于 SQLAlchemy 乐观锁，避免并发更新互相覆盖
- 主要索引：`(status, due_at)`、`(priority, created_at)`、`(created_at)`
- 字符集 `utf8mb4`，时间统一按 `Asia/Shanghai`
- 表结构由 `migrations/versions/0001_create_tasks.py` 管理

## API

| 方法 | 路径 | 说明 |
| --- | --- | --- |
| POST | `/api/tasks` | 创建任务 |
| GET | `/api/tasks` | 分页查询，支持 `status`、`priority` |
| GET | `/api/tasks/{id}` | 查询单个任务 |
| PATCH | `/api/tasks/{id}` | 部分更新任务 |
| DELETE | `/api/tasks/{id}` | 删除任务 |
| GET | `/health` | 健康检查 |
| GET | `/actuator/health` | 兼容健康检查 |

分页参数 `page` 从 0 开始，`size` 范围 1–100，默认按创建时间倒序。

## 本地启动

本机已有 MySQL 8 时：

```sql
CREATE DATABASE IF NOT EXISTS taskflow DEFAULT CHARACTER SET utf8mb4;
CREATE USER IF NOT EXISTS 'taskflow'@'localhost' IDENTIFIED BY 'taskflow_dev';
GRANT ALL PRIVILEGES ON taskflow.* TO 'taskflow'@'localhost';
FLUSH PRIVILEGES;
```

然后运行：

```bash
python3.12 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
alembic upgrade head
uvicorn app.main:app --reload
```

也可以使用 Docker Compose，注意它映射到主机 `3307`，避免和本机已有 MySQL 冲突：

```bash
docker compose up -d
DATABASE_URL='mysql+pymysql://taskflow:taskflow_dev@127.0.0.1:3307/taskflow?charset=utf8mb4' \
  alembic upgrade head
```

## 测试

```bash
python -m pytest
```

测试使用 SQLite 文件库，覆盖创建、校验、分页筛选、404、更新版本递增和删除。GitHub Actions 还包含一个使用 MySQL 8 的迁移与冒烟任务，验证 Alembic 和真实数据库启动。

## 配置

运行时通过环境变量覆盖数据库配置：

| 变量 | 默认值 |
| --- | --- |
| `DATABASE_URL` | `mysql+pymysql://taskflow:taskflow_dev@127.0.0.1:3306/taskflow?charset=utf8mb4` |
| `APP_NAME` | `TaskFlow API` |

这些默认值只用于本地演示，部署时应通过环境变量或密钥管理系统注入。

## 错误响应

统一返回 `code`、`message` 和 `trace_id`。校验失败返回 422，资源不存在返回 404，乐观锁冲突返回 409，未知异常返回 500 且日志保留 trace id。
