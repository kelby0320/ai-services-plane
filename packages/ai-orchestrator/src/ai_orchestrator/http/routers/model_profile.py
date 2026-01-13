from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status

from ai_orchestrator.context import AppContext
from ai_orchestrator.http.dependencies import get_context
from ai_orchestrator.http.dtos import ModelProfileResponse

router = APIRouter()


@router.get(
    "/model_profile/{model_profile_id}",
    response_model=ModelProfileResponse,
    summary="Get Model Profile",
)
async def get_model_profile(
    model_profile_id: UUID,
    context: AppContext = Depends(get_context),
) -> ModelProfileResponse:
    """Get a model profile by ID."""
    repository = context.get_model_profile_repository()
    profile = repository.get_by_id(model_profile_id)

    if profile is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Model profile {model_profile_id} not found",
        )

    return ModelProfileResponse(
        id=profile.id,
        name=profile.name,
        description=profile.description,
        model=profile.model,
        created_at=profile.created_at,
        updated_at=profile.updated_at,
        is_active=profile.is_active,
        temperature=profile.temperature,
        top_p=profile.top_p,
        max_tokens=profile.max_tokens,
    )
