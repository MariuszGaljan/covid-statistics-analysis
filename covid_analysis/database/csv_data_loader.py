'''
Contains functions and classes neccessary to load data from a csv file to Python class instances.

To load data from the file, use function load_covid_data(file_path).
'''

import csv
from datetime import datetime


class Country:
    '''Contains data about a single row from the csv data'''
    def __init__(self, name, continent, new_cases, day, total_cases, new_cases_per_million):
        self.continent = continent
        self.name = name
        self.day = day
        self.new_cases = new_cases
        self.total_cases = total_cases
        self.new_cases_per_million = new_cases_per_million

    def __str__(self):
        return '[' + self.name + ', ' + self.continent + ', '\
            + str(self.new_cases) + ', ' + str(self.day) + ', '\
            + str(self.total_cases) + ', ' + \
            str(self.new_cases_per_million) + ']'


def load_covid_data(file_path):
    '''
    Loads data from a csv file into instances of Country class.
    Returns:
        List of Country instances. Each object contains data from 1 row of csv file
    '''
    country_list = []

    with open(file_path) as csv_file:
        # csv_reader = csv.reader(csv_file, delimiter=',')
        csv_reader = csv.DictReader(csv_file, delimiter=',')

        for row in csv_reader:
            new_cases = float(
                row['new_cases']) if row['new_cases'] != '' else 0.0
            date = datetime.strptime(row['date'], '%Y-%m-%d')
            total_cases = float(
                row['total_cases']) if row['total_cases'] != '' else 0.0
            new_cases_per_million = float(
                row['new_cases_per_million']) if row['new_cases_per_million'] != '' else 0.0

            country_list.append(
                Country(
                    row['location'],
                    row['continent'],
                    new_cases,
                    date,
                    total_cases,
                    new_cases_per_million
                )
            )
    return(country_list)


def head(country_list, n=10):
    '''Prints first n elements of the list of Country objects.'''
    for country in country_list[:n]:
        print(country)
