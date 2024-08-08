from pydantic import BaseModel
from datetime import datetime


class EncKeyBase(BaseModel):
    tablename: str
    encryption_key: str


class EncKeyCreate(EncKeyBase):
    pass


class EncKeyUpdate(BaseModel):
    encryption_key: str


class EncKeyResponse(EncKeyBase):
    enc_key: int
    m_time: datetime

    class Config:
        orm_mode = True
