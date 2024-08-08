from sqlalchemy.orm import Session
from models import EncKey  # Change relative import to absolute import
from schemas import (
    EncKeyCreate,
    EncKeyUpdate,
)  # Change relative import to absolute import


def create_key(db: Session, key: EncKeyCreate):
    db_key = EncKey(**key.dict())
    db.add(db_key)
    db.commit()
    db.refresh(db_key)
    return db_key


def delete_key(db: Session, tablename: str):
    db_key = db.query(EncKey).filter(EncKey.tablename == tablename).first()
    if db_key:
        db.delete(db_key)
        db.commit()
        return db_key
    return None


def get_key(db: Session, tablename: str):
    return db.query(EncKey).filter(EncKey.tablename == tablename).first()


def get_keys(db: Session):
    return db.query(EncKey).all()


def update_key(db: Session, tablename: str, key_update: EncKeyUpdate):
    db_key = db.query(EncKey).filter(EncKey.tablename == tablename).first()
    if db_key:
        db_key.encryption_key = key_update.encryption_key
        db.commit()
        db.refresh(db_key)
        return db_key
    return None
