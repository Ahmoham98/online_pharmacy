from fastapi import HTTPException, Depends
from sqlmodel.ext.asyncio.session import AsyncSession
from database import get_session
from views.Auth import Authentication


async def get_current_active_superuser(
    *,
    session: AsyncSession = Depends(get_session),
    admin_username: str,
):
    current_user = await Authentication(session=session).get_user_from_db(username=admin_username)
    if not current_user.is_superuser:
        raise HTTPException(status_code=403, detail="you don't have enough privilages")
    return current_user