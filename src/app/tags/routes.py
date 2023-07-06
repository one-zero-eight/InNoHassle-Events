from fastapi import APIRouter

from src.app.dependencies import TAG_REPOSITORY_DEPENDENCY
from src.app.tags.schemas import ViewTag, ListOfTagsResponse
from src.exceptions import TagNotFoundException

router = APIRouter(prefix="/tags", tags=["Tags"])


@router.get(
    "/{tag_id}",
    responses={
        200: {"description": "Tag info", "model": ViewTag},
        404: {"description": "Tag is not found"},
    },
)
async def get_tag(
    tag_id: int,
    tag_repository: TAG_REPOSITORY_DEPENDENCY,
) -> ViewTag:
    """
    Get tag info by id
    """
    tag = await tag_repository.get_tag(tag_id)

    if tag is None:
        raise TagNotFoundException()

    return tag


@router.get(
    "/",
    responses={
        200: {"description": "List of tags", "model": ListOfTagsResponse},
    },
)
async def get_list_tags(
    tag_repository: TAG_REPOSITORY_DEPENDENCY,
) -> ListOfTagsResponse:
    """
    Get a list of all tags
    """
    tags = await tag_repository.get_all_tags()
    return ListOfTagsResponse.from_iterable(tags)
