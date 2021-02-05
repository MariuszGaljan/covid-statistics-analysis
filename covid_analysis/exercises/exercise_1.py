# Zadanie 1
#
# Znaleźć top 10 krajów z najmniejszą liczbą zachorowań w Afryce na koniec miesiąca Maj 2020.

from datetime import datetime

import pandas as pd

from database import db
from database.models import DailyStatistic

data = pd.DataFrame(columns=['country_name', 'total_cases'])

with db.session_scope() as session:
    african_countries = db.query_countries_from_continent('Africa', session)
    african_countries = sorted(african_countries, key=lambda c: c.name)

    date = datetime(2020, 5, 31)

    # Getting statistics from last day of may
    for country in african_countries:
        stat_from_given_date = country.statistics.filter(
            DailyStatistic.date == date
        ).first()
        data = data.append(
            {'country_name': country.name, 'total_cases': stat_from_given_date.total_cases}, ignore_index=True
        )
