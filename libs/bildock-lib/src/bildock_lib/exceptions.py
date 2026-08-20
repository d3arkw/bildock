from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse


class AppError(Exception):
    status_code: int
    code: str

    def __init__(self, message: str):
        self.message = message
        super().__init__(message)


class NotFoundError(AppError):
    status_code = 404
    code = "NOT_FOUND"


class ConflictError(AppError):
    status_code = 409
    code = "CONFLICT"


class UnauthorizedError(AppError):
    status_code = 401
    code = "UNAUTHORIZED"


def register_exception_handlers(app: FastAPI) -> None:
    @app.exception_handler(AppError)
    def app_error_handler(request: Request, exc: AppError) -> JSONResponse:
        return JSONResponse(status_code=exc.status_code, content={"message": exc.message, "code": exc.code})
