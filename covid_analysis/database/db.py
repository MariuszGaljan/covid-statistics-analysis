'''
This file contains all the functions neccessary to process data in the database.
It establishes a connection to the database once it's imported

Using session_scope is convenient, because it automatically opens and closes the session.
See import_data_from_csv() function for an example usage.
'''

from calendar import monthrange
from contextlib import contextmanager

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import extract

from covid_analysis.database.csv_data_loader import load_covid_data
from covid_analysis.database.models import Base, Continent, Country, DailyStatistic


DATABASE_URI = 'postgresql://postgres:password@localhost:5432/covid_db'

engine = create_engine(DATABASE_URI)
Base.metadata.create_all(engine)
Session = sessionmaker(engine)

def init_db():
    '''Invoked at the end of this script to load data into database'''
    # recreate_database()
    import_data_from_csv('covid_data.csv')


def recreate_database():
    '''Restores the database to its default state'''
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)


@contextmanager
def session_scope():
    '''
    Session scope lets us use Python's context manager (with keyword)
    This way we can put all queries and session operations within the with block
    and it will automatically create a new session, commit changes and close the session
    '''
    session = Session()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()


def import_data_from_csv(file_path):
    ''' Imports data from the csv file into tables if they are empty '''
    country_list = load_covid_data(file_path)
    with session_scope() as session:
        if query_is_empty(session.query(Continent)):
            import_continents_from_csv(country_list, session)
        if query_is_empty(session.query(Country)):
            import_countries_from_csv(country_list, session)
        if query_is_empty(session.query(DailyStatistic)):
            import_daily_statistics_from_csv(country_list, session)


def query_is_empty(query):
    return query.count() == 0


def import_continents_from_csv(country_list, session):
    continents = set(
        [country.continent for country in country_list if country.continent != ''])
    for c in continents:
        session.add(Continent(name=c))


def import_countries_from_csv(country_list, session):
    countries = set([(country.continent, country.name)
                     for country in country_list if country.continent != ''])

    for continent, country in countries:
        continent_id = session.query(Continent).filter(
            Continent.name == continent).first().id
        session.add(Country(name=country, continent_id=continent_id))


def import_daily_statistics_from_csv(country_list, session):
    # Creating a dict of country_name:country_id to speed up the insertion process
    countries = session.query(Country).all()
    country_name_id_dict = {}
    for c in countries:
        country_name_id_dict[c.name] = c.id

    for country_daily in country_list:
        try:
            country_id = country_name_id_dict[country_daily.name]

            session.add(
                DailyStatistic(
                    country_id=country_id,
                    date=country_daily.day,
                    new_cases=country_daily.new_cases,
                    total_cases=country_daily.total_cases,
                    new_cases_per_million=country_daily.new_cases_per_million
                ))
        except:
            # we skip the data with 'World' as country
            pass


def query_countries_from_continent(continent_name, session):
    continent = session.query(Continent).filter(
        Continent.name == continent_name).first()
    return continent.countries


def calculate_country_month_mean(country, month):
    stats_from_month = country.statistics.filter(
        extract('month', DailyStatistic.date) == month
    ).all()
    new_cases_per_million = [
        stat.new_cases_per_million for stat in stats_from_month]

    days_in_month = monthrange(2020, month)[1]
    return sum(new_cases_per_million) / days_in_month



init_db()