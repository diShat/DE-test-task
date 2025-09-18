from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, BigInteger, String, Boolean, Text, TIMESTAMP

Base = declarative_base()

class Launch(Base):
    __tablename__ = "launches"

    id = Column(String, primary_key=True)
    flight_number = Column(Integer)
    name = Column(String)
    date_utc = Column(TIMESTAMP(timezone=True))
    date_precision = Column(String)
    success = Column(Boolean)
    upcoming = Column(Boolean)
    tbd = Column(Boolean)
    rocket = Column(String)
    core = Column(String)
    core_flight = Column(Integer)
    core_landing_success = Column(Boolean)
    core_landing_type = Column(String)
    links_wikipedia = Column(Text)
    details = Column(Text)
    launch_year = Column(Integer)
    core_reused = Column(Boolean)