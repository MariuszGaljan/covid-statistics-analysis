'''
Task 2:
Create a map, 
where the key is a continent's name and the value is a country with highest number of total cases.
'''


import pandas as pd
from sqlalchemy import func, select

from database.models import Continent, Country, DailyStatistic
from database import db


data = pd.DataFrame(columns=['continent', 'max_cases'])

with db.session_scope() as session:
    country_data_subquery = select([
        DailyStatistic.country_id.label('country_id'), func.max(
            DailyStatistic.total_cases).label('total_cases')
    ]).group_by(Country.id).alias('country_data_subquery')

    country_data_subquery = session.query(
        DailyStatistic.country_id.label('country_id'), func.max(
            DailyStatistic.total_cases).label('total_cases')
    ).group_by(DailyStatistic.country_id).order_by(DailyStatistic.country_id).subquery('country_data_subquery')

    country_data_subquery = session.query(
        Country.continent_id.label('continent_id'),
        Country.id.label('country_id'),
        country_data_subquery.c.total_cases.label('total_cases')
    ).join(country_data_subquery, Country.id == country_data_subquery.c.country_id).subquery('country_data_subquery')

    continent_data = session.query(
        Continent.name, func.max(country_data_subquery.c.total_cases)
    ).join(country_data_subquery, Continent.id == country_data_subquery.c.continent_id).group_by(Continent.name).all()

    for continent in continent_data:
        data = data.append({'continent': continent[0], 'max_cases': continent[1]}, ignore_index=True)
