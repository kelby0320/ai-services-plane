from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status

from ai_orchestrator.context import AppContext
from ai_orchestrator.http.dependencies import get_context
from ai_orchestrator.http.dtos import GraphProfileResponse

router = APIRouter()


@router.get(
    "/graph_profile/{graph_profile_id}",
    response_model=GraphProfileResponse,
    summary="Get Graph Profile",
)
async def get_graph_profile(
    graph_profile_id: UUID,
    context: AppContext = Depends(get_context),
) -> GraphProfileResponse:
    """Get a graph profile by ID."""
    repository = context.get_graph_profile_repository()
    profile = repository.get_by_id(graph_profile_id)

    if profile is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Graph profile {graph_profile_id} not found",
        )

    return GraphProfileResponse(
        id=profile.id,
        name=profile.name,
        version_major=profile.version_major,
        version_minor=profile.version_minor,
        graph_name=profile.graph_name,
        created_at=profile.created_at,
        updated_at=profile.updated_at,
        is_active=profile.is_active,
    )
