from sqlalchemy import Column, Integer, String, Float, Text, DateTime
from sqlalchemy.orm import declarative_base
from datetime import datetime

Base = declarative_base()

class MatchHistory(Base):
    __tablename__ = "match_history"
    id = Column(Integer, primary_key=True, index=True)
    resume_filename = Column(String(255))
    job_title = Column(String(255), nullable=True)
    score = Column(Float)
    verdict = Column(String(255))
    missing_keywords = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
