from sqlalchemy import Column, Integer, String, TIMESTAMP
from database import Base  # Change relative import to absolute import
from datetime import datetime


class EncKey(Base):
    __tablename__ = "enc_keys"
    enc_key = Column(Integer, primary_key=True, index=True)
    tablename = Column(String(255), unique=True, nullable=False)
    encryption_key = Column(String(255), nullable=False)
    m_time = Column(TIMESTAMP, default=datetime.utcnow, onupdate=datetime.utcnow)
