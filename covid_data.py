"""CSC110 Final Project Submission: Reading COVID-19 Related Data

Instructions (READ THIS FIRST!)
===============================

This Python module contains code used to read the dataset "covid_data.csv" and convert it into a
format which can be analyzed further.

Happy exploring!

Copyright and Usage Information
===============================

This file is provided solely for the personal and private use of TAs and faculty
of CSC110 at the University of Toronto St. George campus. All forms of
distribution of this code, whether as given or with any changes, are
expressly prohibited unless facilitated by the above individuals.
For more information on copyright for CSC110 materials, please consult the Course Syllabus.

This file is Copyright (c) 2021 Christian Bongalon, Yuti Wang, Jennifer Xi, and Celina Yueh.
"""
import csv
import datetime


class CovidData:
    """Represents chronological data for COVID cases in Canada"""
    total_cases: int
    daily_cases: int
    date: datetime.date

    def __init__(self, total_cases: int, daily_cases: int, date: datetime.date) -> None:
        self.total_cases = total_cases
        self.daily_cases = daily_cases
        self.date = date


def read_covid_file(filename: str) -> list[CovidData]:
    """Return the data stored in a csv file with the given filename as a CovidData list.

    The return value is a list of CovidData.

    Preconditions:
      - filename refers to a valid csv file in the proper format
    """
    with open(filename, encoding="utf8") as file:

        reader = csv.reader(file)
        next(reader)  # Skips the header.

        data = [CovidData(int(row[8]), int(row[15]), str_to_date(row[3])) for row in reader
                if row[0] == '1']

    return data


def str_to_date(string: str) -> datetime.date:
    """Convert a string in yyyy-mm-dd format to a datetime.date.

    Preconditions:
    - date_string has format yyyy-mm-dd

    >>> str_to_date('2020-09-17')
    datetime.date(2020, 9, 17)
    """
    split_list = str.split(string, '-')
    year = int(split_list[0])
    month = int(split_list[1])
    day = int(split_list[2])
    return datetime.date(year, month, day)


if __name__ == '__main__':
    import python_ta
    import python_ta.contracts

    python_ta.contracts.DEBUG_CONTRACTS = False
    python_ta.contracts.check_all_contracts()

    import doctest

    doctest.testmod()

    python_ta.check_all(config={
        'extra-imports': ['csv', 'datetime'],
        'allowed-io': ['read_covid_file', 'str_to_date'],
        'max-line-length': 100,
        'disable': ['R1705', 'C0200']
    })
