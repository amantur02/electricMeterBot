from sqlalchemy import Column, Integer, String, Date, Boolean, Float, ForeignKey, TIMESTAMP, func
from .db_base_class import Base


class ResidentDB(Base):
    __tablename__ = 'residents'

    home_number = Column(String, nullable=False)
    name = Column(String, nullable=True)
    phone_number = Column(String, nullable=True)


class ElectricityReadingDB(Base):
    __tablename__ = 'electricity_readings'

    resident_id = Column(
        Integer,
        ForeignKey("residents.id", ondelete="RESTRICT"),
        nullable=False,
    )
    current_kwh = Column(Integer, nullable=False)
    consumed_kwh = Column(Integer, nullable=True)
    increased_kwh = Column(Integer, nullable=True)
    payment_status = Column(Boolean, default=False)
    amount = Column(Float, nullable=True)
    increased_amount = Column(Float, nullable=True)
    not_increased_amount = Column(Float, nullable=True)
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())
