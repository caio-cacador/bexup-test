from fastapi import Request
from fastapi.responses import JSONResponse
from http import HTTPStatus


class ServiceUnavailableError(Exception):
    pass


async def service_unavailable_handler(request: Request, exc: ServiceUnavailableError):
    return JSONResponse(
        status_code=HTTPStatus.SERVICE_UNAVAILABLE,
        content={"message": f"The external service is unavailable!"},
    )
