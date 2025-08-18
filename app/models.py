from sqlalchemy import Column, Integer, String, Boolean, DateTime, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class Event(Base):
    __tablename__ = "events"
    id = Column(Integer, primary_key=True)
    event_type = Column(String)      # 'open'/'click'
    email_uid = Column(String)
    timestamp = Column(DateTime)
    user_id = Column(String)         # Google UID
    client_ip = Column(String)
    geo_city = Column(String)
    geo_region = Column(String)
    geo_country = Column(String)
    user_agent = Column(String)
    device_type = Column(String)
    proxy_detected = Column(Boolean)
    bot_detected = Column(Boolean)
    target_url = Column(String)

engine = create_engine('sqlite:///app/database.db')
SessionLocal = sessionmaker(bind=engine)
