from fastapi import APIRouter, status, Response

router = APIRouter()


@router.get("/healthz")
async def healthz() -> Response:
    return Response(status_code=status.HTTP_200_OK)
