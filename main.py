from fastapi import FastAPI, Depends, HTTPException, status, Security
from sqlalchemy.orm import Session
from typing import List
from fastapi.security.api_key import APIKeyHeader, APIKey
from database import engine, get_db  # Change relative import to absolute import
from models import Base, EncKey  # Change relative import to absolute import
from schemas import (
    EncKeyCreate,
    EncKeyResponse,
    EncKeyUpdate,
)  # Change relative import to absolute import
from crud import (
    create_key,
    delete_key,
    get_key,
    get_keys,
    update_key,
)  # Change relative import to absolute import

API_KEY = "3327bc09-53c4-11ee-ae21-8cf8c5e498b3"
API_KEY_NAME = "X-API-Key"
api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=False)

Base.metadata.create_all(bind=engine)

app = FastAPI()


async def get_api_key(api_key_header: str = Security(api_key_header)):
    if api_key_header == API_KEY:
        return api_key_header
    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
        )


@app.post("/keys/", response_model=EncKeyResponse, status_code=status.HTTP_201_CREATED)
def create_key(
    key: EncKeyCreate,
    db: Session = Depends(get_db),
    api_key: APIKey = Depends(get_api_key),
):
    return create_key(db, key)


@app.delete("/keys/{tablename}", response_model=EncKeyResponse)
def delete_key_endpoint(
    tablename: str,
    db: Session = Depends(get_db),
    api_key: APIKey = Depends(get_api_key),
):
    db_key = delete_key(db, tablename)
    if db_key is None:
        raise HTTPException(status_code=404, detail="Key not found")
    return db_key


@app.get("/keys/{tablename}", response_model=EncKeyResponse)
def get_key(
    tablename: str,
    db: Session = Depends(get_db),
    api_key: APIKey = Depends(get_api_key),
):
    db_key = get_key(db, tablename)
    if db_key is None:
        raise HTTPException(status_code=404, detail="Key not found")
    return db_key


@app.get("/keys/", response_model=List[EncKeyResponse])
def get_key(db: Session = Depends(get_db), api_key: APIKey = Depends(get_api_key)):
    return get_keys(db)


@app.put("/keys/{tablename}", response_model=EncKeyResponse)
def update_key(
    tablename: str,
    key: EncKeyUpdate,
    db: Session = Depends(get_db),
    api_key: APIKey = Depends(get_api_key),
):
    db_key = update_key(db, tablename, key)
    if db_key is None:
        raise HTTPException(status_code=404, detail="Key not found")
    return db_key
