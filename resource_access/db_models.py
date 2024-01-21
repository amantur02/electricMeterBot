from sqlalchemy import Column, Integer, String, Date, Boolean, Float, ForeignKey, TIMESTAMP, func
from .db_base_class import Base


class ResidentDB(Base):
    __tablename__ = 'residents'

    home_number = Column(String)
    name = Column(String)
    phone_number = Column(String)


class ElectricityReadingDB(Base):
    __tablename__ = 'electricity_readings'

    resident_id = Column(
        Integer,
        ForeignKey("residents.id", ondelete="RESTRICT"),
        nullable=False,
    )
    current_reading = Column(Integer, nullable=False)
    payment_status = Column(Boolean, default=False)
    amount = Column(Float, nullable=True)
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())
