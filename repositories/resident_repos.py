import logging

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from resource_access.db_models import ResidentDB
from schemas import Resident

logger = logging.getLogger(__name__)


class UserRepository:
    def __init__(self, db_session: Session):
        self._db_session = db_session

    async def create_resident(self, resident: Resident) -> Resident:
        resident_db = ResidentDB(**resident.model_dump(exclude={'id'}))
        self._db_session.add(resident_db)
        try:
            await self._db_session.commit()
            await self._db_session.refresh(resident_db)
            return Resident.model_validate(resident_db)
        except IntegrityError as error:
            logger.error(
                f"Error while creating User. Details: {error.orig.args}"
            )
            await self._db_session.rollback()
