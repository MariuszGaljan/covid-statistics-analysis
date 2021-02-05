'''
This file contains definitions of classes for the sqlalchemy's ORM.
Each class represents a table in our database.
'''


from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy import Column, DateTime, Float, Integer, String


Base = declarative_base()


class Continent(Base):
    __tablename__ = 'continent'

    id = Column(Integer, primary_key=True)
    name = Column(String)

    countries = relationship(
        'Country', back_populates='continent', cascade='all, delete', lazy='dynamic')

    def __repr__(self) -> str:
        return f'<Continent - Id: {self.id}, name: {self.name}>'


class Country(Base):
    __tablename__ = 'country'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    continent_id = Column(Integer, ForeignKey('continent.id'))

    continent = relationship('Continent', back_populates='countries')
    statistics = relationship(
        'DailyStatistic', back_populates='country', cascade='all, delete', lazy='dynamic')

    def __repr__(self) -> str:
        return f'<Country - Id: {self.id}, name: {self.name}, continent_id: {self.continent_id}>'


class DailyStatistic(Base):
    __tablename__ = 'daily_statistic'

    id = Column(Integer, primary_key=True)
    country_id = Column(Integer, ForeignKey('country.id'))

    date = Column(DateTime)
    new_cases = Column(Float)
    total_cases = Column(Float)
    new_cases_per_million = Column(Float)

    country = relationship('Country', back_populates='statistics')
