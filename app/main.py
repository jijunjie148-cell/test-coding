import logging
import uuid

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.api import router
from app.config import settings
from app.errors import TaskNotFoundError, VersionConflictError


logger = logging.getLogger("taskflow")


def create_app() -> FastAPI:
    app = FastAPI(title=settings.app_name, version="0.2.0")
    app.include_router(router)

    @app.exception_handler(TaskNotFoundError)
    async def task_not_found_handler(
        _request: Request, exception: TaskNotFoundError
    ) -> JSONResponse:
        return JSONResponse(
            status_code=404,
            content={
                "code": "TASK_NOT_FOUND",
                "message": str(exception),
                "trace_id": str(uuid.uuid4()),
            },
        )

    @app.exception_handler(VersionConflictError)
    async def version_conflict_handler(
        _request: Request, exception: VersionConflictError
    ) -> JSONResponse:
        return JSONResponse(
            status_code=409,
            content={
                "code": "TASK_CONFLICT",
                "message": str(exception),
                "trace_id": str(uuid.uuid4()),
            },
        )

    @app.exception_handler(Exception)
    async def unexpected_error_handler(
        _request: Request, exception: Exception
    ) -> JSONResponse:
        trace_id = str(uuid.uuid4())
        logger.exception("Unhandled error trace_id=%s", trace_id, exc_info=exception)
        return JSONResponse(
            status_code=500,
            content={
                "code": "INTERNAL_ERROR",
                "message": "Unexpected server error",
                "trace_id": trace_id,
            },
        )

    @app.get("/health", tags=["health"])
    @app.get("/actuator/health", tags=["health"])
    async def health() -> dict[str, str]:
        return {"status": "UP", "app": settings.app_name}

    return app


app = create_app()
