import logging

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from resource_access.db_models import ResidentDB

logger = logging.getLogger(__name__)


class ResidentRepository:
    def __init__(self, db_session: Session):
        self._db_session = db_session

    async def create_resident(self, state_data: dict) -> ResidentDB:
        resident_db = ResidentDB(
            home_number=state_data.get('home_number'),
            name=state_data.get('name')
        )
        self._db_session.add(resident_db)
        try:
            await self._db_session.commit()
            await self._db_session.refresh(resident_db)
            return resident_db
        except IntegrityError as error:
            logger.error(
                f"Error while creating User. Details: {error.orig.args}"
            )
            await self._db_session.rollback()
