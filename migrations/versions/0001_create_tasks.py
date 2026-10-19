"""create tasks table

Revision ID: 0001
Revises:
Create Date: 2026-10-19
"""

from alembic import op
import sqlalchemy as sa


revision = "0001"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "tasks",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("title", sa.String(length=120), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("status", sa.String(length=20), nullable=False),
        sa.Column("priority", sa.String(length=20), nullable=False),
        sa.Column("due_at", sa.DateTime(), nullable=True),
        sa.Column("version", sa.Integer(), server_default="0", nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        mysql_charset="utf8mb4",
        mysql_collate="utf8mb4_0900_ai_ci",
    )
    op.create_index("idx_tasks_status_due_at", "tasks", ["status", "due_at"])
    op.create_index(
        "idx_tasks_priority_created_at", "tasks", ["priority", "created_at"]
    )
    op.create_index("idx_tasks_created_at", "tasks", ["created_at"])


def downgrade() -> None:
    op.drop_index("idx_tasks_created_at", table_name="tasks")
    op.drop_index("idx_tasks_priority_created_at", table_name="tasks")
    op.drop_index("idx_tasks_status_due_at", table_name="tasks")
    op.drop_table("tasks")
