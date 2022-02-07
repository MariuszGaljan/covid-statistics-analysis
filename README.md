# covid-statistics-analysis
My analysis of COVID-19 spread data.

This program runs an analysis of the COVID-19 spread data in countries all aroud the world.

# Tasks
We have 3 exercises, each described in detail in exercises/exercise_X.py, where X is the number of the exercise.

### Task 1

Find top 10 countries with the smallest number of total cases at thte end of May 2020.

### Task 2

Create a map, where the key is a continent's name and the value is a country with highest number of total cases.

### Task 3

1. Calculate a mean monthly range of daily new cases per million citizens for countries of Africa.
2. Group the countries into 3 risk categories (Low, Medium, High) based on the mean range.
3. Show all the countries which lowered their risk status from the beginning of April to the end of October.

Days with missing data are treated as 0 new cases.


For each exercise, the program queries the data from the **connected Postgres database**
and plots the results for the user.

Each plot is interactive and viewed in a website. I saved all the websites with plots in the **saved_results** folder, so you can open them yourself and check them out without running the code if you'd like.

However, I also included still images of the plot below.


# Plots

## Task 1
![Plot 1](https://github.com/MariuszGaljan/covid-statistics-analysis/blob/f49338cd2bd74e17d9c5189e50319a428230be56/saved_results/Images/Exercise%201%20Result.png)

## Task 2
![Plot 2](https://github.com/MariuszGaljan/covid-statistics-analysis/blob/f49338cd2bd74e17d9c5189e50319a428230be56/saved_results/Images/Exercise%202.png)

## Task 3
![Plot 3](https://github.com/MariuszGaljan/covid-statistics-analysis/blob/f49338cd2bd74e17d9c5189e50319a428230be56/saved_results/Images/Exercise%203.png)


# Additional notes

Although it's not a good practice to include data in the repository, I included a PostgreSQL **database backup file** in case you'd like to try it out yourself (though the application only requires a connection to a db. It will fill the rest from the CSV if needed).
