from sqlalchemy import create_engine, Column, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session

from domain import CountryDomain

# In a real scenario, these config and secrets would be read from another source (vault, configmap, etc)
# For the sake of this example, they have been harcoded here.
DATABASE_URL = "postgresql://myuser:mypassword@postgres/mydatabase"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

class Country(Base):
    __tablename__ = "country"
    id = Column(String, primary_key=True, index=True)
    name = Column(String, index=True)
    code = Column(String, index=True)

Base.metadata.create_all(bind=engine)


def list_countries(db: Session):
    countries = db.query(Country).all()
    return [CountryDomain(id=str(c.id), name=c.name, code=c.code) for c in countries]


def get_country(db: Session, country_id: str):
    c = db.query(Country).filter(Country.id == country_id).first()
    if c is None:
        return None

    return (CountryDomain(id=country_id, name=c.name, code=c.code))


def get_country_by_code(db: Session, country_code: str):
    c = db.query(Country).filter(Country.code == country_code).first()
    if c is None:
        return None

    return (CountryDomain(id=str(c.id), name=c.name, code=c.code))


def create_country(db: Session, country: CountryDomain):
    db_country = Country(id=country.id, name=country.name, code=country.code)
    db.add(db_country)
    db.commit()
    db.refresh(db_country)
    return country.id


def delete_country(db: Session, id: str):
    country = db.query(Country).filter(Country.id == id).first()
    if not country:
        return None

    db.delete(country)
    db.commit()
    return country