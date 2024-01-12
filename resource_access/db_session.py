from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from core.config import settings
from resource_access.db_base_class import Base

engine = create_engine(settings.postgres_url)

Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()
