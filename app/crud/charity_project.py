from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import CharityProject
from .base import CRUDBase


class CharityProjectCRUD(CRUDBase):

    async def get_id_by_name(
            self,
            charity_project_name: str,
            session: AsyncSession,
    ) -> Optional[int]:
        charity_project_id = await session.execute(
            select(CharityProject.id).where(
                CharityProject.name == charity_project_name
            )
        )
        return charity_project_id.scalars().first()

    async def get_projects_by_completion_rate(
        self,
        session: AsyncSession,
    ) -> list[CharityProject]:
        projects = session.execute(
            select(CharityProject).where(
                CharityProject.fully_invested
            ).order_by(
                CharityProject.close_date - CharityProject.create_date
            )
        )
        return projects.scalars().all()


charity_project_crud = CharityProjectCRUD(CharityProject)
