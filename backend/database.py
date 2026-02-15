from sqlalchemy import create_engine, Column, Integer, String, DateTime, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime

SQLALCHEMY_DATABASE_URL = "sqlite:///./skillmatch.db"

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    
    user_id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    password_hash = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)

class Submission(Base):
    __tablename__ = "submissions"
    
    submission_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, index=True)
    resume_text = Column(Text)
    parsed_resume_fields = Column(Text)
    job_description_text = Column(Text)
    parsed_jd_fields = Column(Text)
    resume_clean_text = Column(Text)
    resume_tokens = Column(Text)
    resume_skills = Column(Text)
    jd_clean_text = Column(Text)
    jd_tokens = Column(Text)
    jd_skills = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)

Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
