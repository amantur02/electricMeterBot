# import logging
#
# from sqlalchemy import select, desc
# from sqlalchemy.exc import IntegrityError
# from sqlalchemy.orm import Session
#
# from resource_access.db_models import ResidentDB, ElectricityReadingDB
#
# logger = logging.getLogger(__name__)
#
#
# class ResidentRepository:
#     def __init__(self, db_session: Session):
#         self._db_session = db_session
#
#     async def create_resident(self, state_data: dict) -> ResidentDB:
#         resident_db = ResidentDB(
#             home_number=state_data.get('home_number'),
#             name=state_data.get('name')
#         )
#         self._db_session.add(resident_db)
#         try:
#             await self._db_session.commit()
#             await self._db_session.refresh(resident_db)
#             return resident_db
#         except IntegrityError as error:
#             logger.error(
#                 f"Error while creating User. Details: {error.orig.args}"
#             )
#             await self._db_session.rollback()
#
#     async def get_resident_by_home_number(self, resident_home_number: int) -> ResidentDB:
#         query = await self._db_session.execute(
#             select(ResidentDB).where(
#                 ResidentDB.home_number == resident_home_number
#             )
#         )
#         return query.scalar()
#
#
# class ElectricityReadingRepository:
#     def __init__(self, db_session: Session):
#         self._db_session = db_session
#
#     async def create_reading(self, state_data: dict) -> ElectricityReadingDB:
#         reading_db = ElectricityReadingDB(
#
#         )
#
#     async def get_last_reading_by_resident_id(self, resident_id: int) -> ElectricityReadingDB:
#         query = await self._db_session.execute(
#             select(ElectricityReadingDB).where(
#                 ElectricityReadingDB.resident_id == resident_id
#             ).order_by(desc(ElectricityReadingDB.created_date)).limit(1)
#         )
#         return query.scalar()
