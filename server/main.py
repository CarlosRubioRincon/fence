from typing import List
import uuid

from fastapi import FastAPI, HTTPException, Depends, Query
from pydantic import BaseModel
from sqlalchemy.orm import Session

import db as db_provider
from domain import CountryDomain


def get_db():
    db = db_provider.SessionLocal()
    try:
        yield db
    finally:
        db.close()


app = FastAPI()

class CountryResponse(BaseModel):
    id: str
    name: str
    code: str


@app.get("/country/{country_id}", response_model=CountryResponse)
def get_country(country_id: str, db: Session = Depends(get_db)):
    country = db_provider.get_country(db, country_id)
    
    if country is None:
        raise HTTPException(status_code=404, detail="Country not found")
        
    return CountryResponse(id=country.id, name=country.name, code=country.code)


@app.get("/country", response_model=CountryResponse)
def get_country_by_code(country_code: str = Query(..., description="The country code"), db: Session = Depends(get_db)):
    country = db_provider.get_country_by_code(db, country_code)
    
    if country is None:
        raise HTTPException(status_code=404, detail="Country not found")
        
    return CountryResponse(id=country.id, name=country.name, code=country.code)


@app.get("/countries", response_model=List[CountryResponse])
def get_countries(db: Session = Depends(get_db)):
    country_domain = db_provider.list_countries(db)
    return [CountryResponse(id=c.id, name=c.name, code=c.code) for c in country_domain]


class CreateCountryRequest(BaseModel):
    name: str
    code: str

class CreateCountryResponse(BaseModel):
    id: str


@app.post("/country", response_model=CreateCountryResponse)
def create_country(country: CreateCountryRequest, db: Session = Depends(get_db)):
    country_db = db_provider.get_country_by_code(db, country.code)
    if country_db:
        raise HTTPException(status_code=400, detail="Country already exists")
    
    country_domain = CountryDomain(id=str(uuid.uuid4()), name=country.name, code=country.code)
    c_id = db_provider.create_country(db=db, country=country_domain)
    return CreateCountryResponse(id=c_id)


class DeleteCountryResponse(BaseModel):
    ok: bool

@app.delete("/country/{country_id}", response_model=DeleteCountryResponse)
def delete_country(country_id: str, db: Session = Depends(get_db)):
    deleted = db_provider.delete_country(db, country_id)
    if deleted is None:
        raise HTTPException(status_code=404, detail="Country not found")

    return DeleteCountryResponse(ok=True)
