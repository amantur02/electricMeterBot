import logging
from typing import List

from pydantic import parse_obj_as
from sqlalchemy import select, desc, func
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from resource_access.db_models import ResidentDB, ElectricityReadingDB
from schemas import Electricity, Resident

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
                f"Error while creating Resident. Details: {error.orig.args}"
            )
            await self._db_session.rollback()

    async def get_resident_by_home_number(self, resident_home_number: str) -> ResidentDB:
        query = await self._db_session.execute(
            select(ResidentDB).where(
                ResidentDB.home_number == resident_home_number
            )
        )
        return query.scalar()

    async def get_residents_by_name(self, name: str) -> list[Resident]:
        query = await self._db_session.execute(
            select(ResidentDB).where(
                func.lower(ResidentDB.name).like(func.lower(f"%{name}%"))
            )
        )

        residents = query.scalars().all()
        return parse_obj_as(List[Resident], residents)


class ElectricityReadingRepository:
    def __init__(self, db_session: Session):
        self._db_session = db_session

    async def create_reading(self, electricity: Electricity) -> Electricity:
        reading_db = ElectricityReadingDB(
            **electricity.model_dump(exclude_unset=True)
        )
        self._db_session.add(reading_db)
        try:
            await self._db_session.commit()
            await self._db_session.refresh(reading_db)
            return Electricity.model_validate(reading_db)
        except IntegrityError as error:
            logger.error(
                f"Error while creating Electricity Reading. Details: {error.orig.args}"
            )
            await self._db_session.rollback()

    async def get_last_reading_by_resident_id(self, resident_id: int) -> ElectricityReadingDB:
        query = await self._db_session.execute(
            select(ElectricityReadingDB).where(
                ElectricityReadingDB.resident_id == resident_id
            ).order_by(desc(ElectricityReadingDB.created_at)).limit(1)
        )
        return query.scalar()
