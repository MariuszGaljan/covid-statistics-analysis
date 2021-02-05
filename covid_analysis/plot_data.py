'''
This file contains functions used to represent each tasks results as plots.
'''


import pandas as pd
import plotly.express as px

from exercises import exercise_1, exercise_2, exercise_3

def main():
    '''Used mainly for testing if needed'''
    plot_exercise_2()


def plot_exercise_1():
    data = exercise_1.data
    fig = px.choropleth(data, 
        locations='country_name',
        locationmode='country names', 
        color='total_cases',
        title="African countries' statistics from last day of may",
        labels={
            'total_cases': 'Total cases'
        }
    )
    fig.show()


def plot_exercise_2():
    data = exercise_2.data
    fig = px.bar(data, x='continent', y='max_cases')
    fig.show()


def plot_exercise_3():
    data = pd.DataFrame(exercise_3.countries_classified)
    data.columns = ['country_name', 'group_april', 'group_october']
    data['group_april'] = data['group_april'].astype('category')
    data['group_october'] = data['group_october'].astype('category')

    fig = px.choropleth(data, locations='country_name',
                        locationmode='country names', color='group_april',
                        title='Country classification in april')
    fig.update_traces(hovertemplate='%{location}')
    fig.show()

    fig = px.choropleth(data, locations='country_name',
                        locationmode='country names', color='group_october',
                        title='Country classification in october')
    fig.update_traces(hovertemplate='%{location}')
    fig.show()


if __name__ == "__main__":
    main()
