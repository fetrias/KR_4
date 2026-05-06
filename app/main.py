from typing import Any

from fastapi import FastAPI, Query, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import BaseModel, EmailStr, Field, conint

from app.users_inmemory import router as users_router

app = FastAPI(title="KR4")
app.include_router(users_router)


class ErrorResponse(BaseModel):
    error: str
    message: str


class ValidationErrorResponse(BaseModel):
    error: str
    message: str
    details: list[dict[str, Any]]


class CustomExceptionA(Exception):
    def __init__(self, message: str = "Custom exception A") -> None:
        self.status_code = 400
        self.message = message


class CustomExceptionB(Exception):
    def __init__(self, message: str = "Custom exception B") -> None:
        self.status_code = 404
        self.message = message


class UserPayload(BaseModel):
    name: str = Field(min_length=1)
    age: conint(gt=18)
    email: EmailStr


@app.exception_handler(CustomExceptionA)
async def custom_exception_a_handler(
    request: Request, exc: CustomExceptionA
) -> JSONResponse:
    payload = ErrorResponse(error="CUSTOM_A", message=exc.message)
    return JSONResponse(status_code=exc.status_code, content=payload.model_dump())


@app.exception_handler(CustomExceptionB)
async def custom_exception_b_handler(
    request: Request, exc: CustomExceptionB
) -> JSONResponse:
    payload = ErrorResponse(error="CUSTOM_B", message=exc.message)
    return JSONResponse(status_code=exc.status_code, content=payload.model_dump())


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(
    request: Request, exc: RequestValidationError
) -> JSONResponse:
    payload = ValidationErrorResponse(
        error="VALIDATION_ERROR",
        message="Invalid request data",
        details=exc.errors(),
    )
    return JSONResponse(status_code=422, content=payload.model_dump())


@app.get("/health")
def health_check() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/errors/a", response_model=ErrorResponse)
def trigger_custom_a(ok: bool = Query(False)) -> ErrorResponse:
    if not ok:
        raise CustomExceptionA("Condition not satisfied")
    return ErrorResponse(error="NONE", message="ok")


@app.get("/errors/b/{item_id}", response_model=ErrorResponse)
def trigger_custom_b(item_id: int) -> ErrorResponse:
    items = {1: "first"}
    if item_id not in items:
        raise CustomExceptionB(f"Item {item_id} not found")
    return ErrorResponse(error="NONE", message=items[item_id])


@app.post("/users/validate", response_model=UserPayload)
def validate_user(payload: UserPayload) -> UserPayload:
    return payload
