"""CSC110 Final Project Submission: Reading and Filtering Events

Instructions (READ THIS FIRST!)
===============================

This Python module contains the code necessary to read and filter through the .csv datasets
pertaining to news events and major events.

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
from typing import List, Tuple
from events import NewsEvents, MajorEvents


def return_relevant_news(news_list: list[NewsEvents]) -> list[NewsEvents]:
    """Returns a list of NewsEvents relevant to anti-Asian hate."""
    news_so_far = []
    for news in news_list:
        if news.is_related():
            news_so_far.append(news)

    return news_so_far


def read_file(filename: str, filetype: str) -> Tuple[List[str], List]:
    """Return the headers and data stored in a csv file with the given filename.

    The return value is a tuple consisting of a list of headers from the csv file as well as a
    list of NewsEvents from the data of the csv file.

    Preconditions:
      - filename refers to a valid csv file with headers
      - type in {'news', 'major'}
    """
    with open(filename, encoding="utf8") as file:

        reader = csv.reader(file)
        headers = next(reader)
        data = []
        if filetype == 'news':
            data = [row_to_newsevent(row) for row in reader]
        elif filetype == 'major':
            data = [row_to_majorevent(row) for row in reader]

    return (headers, data)


def row_to_newsevent(row: List[str]) -> NewsEvents:
    """Convert a row of news data to NewsEvents object.

    Preconditions:
        - row has the correct format for the news dataset
    """
    return NewsEvents(
        row[1],
        row[2],
        str_to_date(row[3][0: 10]),  # Truncates the time portion of the date
        row[4]
    )


def row_to_majorevent(row: List[str]) -> MajorEvents:
    """Convert a row of news data to NewsEvents object.

        Preconditions:
            - row has the correct format for the major events dataset
        """
    return MajorEvents(row[0],
                       str_to_date(row[1][0: 10]),
                       row[2],
                       row[3])


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
        'extra-imports': ['csv', 'typing', 'datetime', 'events'],
        'allowed-io': ['return_relevant_news', 'read_file', 'row_to_newsevent',
                       'row_to_majorevent', 'str_to_date'],
        'max-line-length': 100,
        'disable': ['R1705', 'C0200']
    })
