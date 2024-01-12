from sqlalchemy import Column, Integer, String, Date, Boolean, Float, ForeignKey
from .db_base_class import Base


class ResidentDB(Base):
    __tablename__ = 'residents'

    id = Column(Integer, primary_key=True)
    home_number = Column(String)
    name = Column(String)
    phone_number = Column(String)


class ElectricityReading(Base):
    __tablename__ = 'electricity_readings'

    id = Column(Integer, primary_key=True)
    resident_id = Column(
        Integer,
        ForeignKey("residents.id", ondelete="RESTRICT"),
        nullable=False,
    )
    last_reading = Column(Integer, nullable=True)
    current_reading = Column(Integer, nullable=False)
    payment_status = Column(Boolean, default=False)
    amount = Column(Float)
    created_date = Column(Date)
