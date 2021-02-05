'''
Zadanie 4

Wyznaczyć średni miesięczny przedział dziennych zachorowań na milion mieszkańców
oraz pogrupować państwa na trzy kategorie (low, medium, high)  wg w.w. wymienionego przedziału,
następnie wyświetlić wszystkie państwa, które polepszyły swoją sytuację
od początku kwietnia do końca października.

Przez polepszenie należy rozumieć „awans” do grupy o mniejszej średniej miesięcznej
liczbie zachorowań na milion mieszkańców

**Afryka**

Dni, w których brak danych nt. nowych zakażeń, są traktowane jako 0 nowych zakazeń


Algorytm:

1. Dla każdego kraju średnia miesięczna liczba nowych zachorowań
(obliczamy średnią liczbę nowych zachorowań dla miesiąca końcowego i początkowego).
I tak dla każdego kraju).

średnia liczba nowych zachorowań na początku kwietnia (czyli średnia z marca)
średnia liczba nowych zachorowań na końcu października (czyli średnia z października)

2. Przedziały to (dla wartości średnich z danego miesiąca dla wszystkich krajów):
	- low = [min, (max - min)/3],
	- medium = [(max - min)/3, 2*(max - min)/3],
	- high = [2*(max - min)/3, max]

3. Zakwalifikować każde państwo na podstawie średniej liczby nowych zachorowań na początku kwietnia (czyli średnia z marca)

4. Zakwalifikować każde państwo na podstawie średniej liczby nowych zachorowań na końcu października (czyli średnia z października)

5. Znaleźć państwa, w których kategoria zmieniła się na lepszą
'''

from enum import IntEnum
from database import db


march_means = []
october_means = []
country_names = []

with db.session_scope() as session:
    african_countries = db.query_countries_from_continent('Africa', session)
    african_countries = sorted(african_countries, key=lambda c: c.name)

    march_means = list(map(
        lambda country: db.calculate_country_month_mean(country, 3),
        african_countries
    ))

    october_means = list(map(
        lambda country: db.calculate_country_month_mean(country, 10),
        african_countries
    ))

    country_names = [country.name for country in african_countries]

countries_with_means = [
    (name, march, october) for name, march, october in zip(country_names, march_means, october_means)
]


# 2
march_min = min(march_means)
march_max = max(march_means)

march_low = [march_min, (march_max - march_min) / 3]
march_medium = [(march_max - march_min) / 3, 2 * (march_max - march_min) / 3]
march_high = [2 * (march_max - march_min) / 3, march_max]


oct_min = min(october_means)
oct_max = max(october_means)

oct_low = [oct_min, (oct_max - oct_min) / 3]
oct_medium = [(oct_max - oct_min) / 3, 2 * (oct_max - oct_min) / 3]
oct_high = [2 * (oct_max - oct_min) / 3, oct_max]


# 3
# Categories are assigned as enum integer values, which allows us to assign them names and compare them as integers
class Group(IntEnum):
    LOW = 1
    MEDIUM = 2
    HIGH = 3


# Function used with the map function. The country argument should be an element of the countries_with_means list
def assign_country_to_group_march(country):
    if country[1] < march_low[1]:
        return(Group.LOW)
    elif march_medium[0] < country[1] < march_medium[1]:
        return(Group.MEDIUM)
    else:
        return(Group.HIGH)


# Function used with the map function. The country argument should be an element of the countries_with_means list
def assign_country_to_group_october(country):
    if country[2] < oct_low[1]:
        return(Group.LOW)
    elif oct_medium[0] < country[2] < oct_medium[1]:
        return(Group.MEDIUM)
    else:
        return(Group.HIGH)


april_classification = list(
    map(assign_country_to_group_march, countries_with_means))
october_classification = list(
    map(assign_country_to_group_october, countries_with_means))

countries_classified = [(country, april, october) for country, april, october in zip(
    country_names, april_classification, october_classification)]


# 4
result = list(
    filter(lambda country: country[1] > country[2], countries_classified))


countries_classified = [(country, str(april), str(october)) for country, april, october in zip(
    country_names, april_classification, october_classification)]


for country in result:
    print(country)
