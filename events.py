"""CSC110 Final Project Submission: Event Classes

Instructions (READ THIS FIRST!)
===============================

This Python module contains the abstract class Event and two subclasses NewsEvents and MajorEvents.
These store information containing the title, date and description of Events (with each subclass
possessing their own unique attributes in addition to these) to be filtered later.

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
import datetime


class Event:
    """Represents data for an event."""
    title: str
    date: datetime.date
    description: str

    def __init__(self, title: str, date: datetime.date, description: str) -> None:
        """Initialize a new NewsEvents object."""
        self.title = title
        self.date = date
        self.description = description


class NewsEvents(Event):
    """Represents data for a news article."""
    authors: str

    def __init__(self, authors: str, title: str, publish_date: datetime.date,
                 description: str) -> None:
        """Initialize a new NewsEvents object."""
        Event.__init__(self, title, publish_date, description)
        self.authors = authors

    def is_related(self) -> bool:
        """Returns if the given headline is related to anti-Asian hate"""
        keyword1 = {'asian', 'aapi', 'asia'}
        keyword2 = gather_keywords('east_asian_countries.txt')
        keyword3 = gather_keywords('chinese_cities.txt')
        lowercase_str = self.title.lower() + ' ' + self.description.lower()

        has_keyword1 = any(keyword in lowercase_str for keyword in keyword1)
        has_keyword2 = any(keyword.lower()[0: len(keyword) - 1] in lowercase_str
                           for keyword in keyword2)
        has_keyword3 = any(keyword.lower()[0: len(keyword) - 1] in lowercase_str
                           for keyword in keyword3)

        return any([has_keyword1, has_keyword2, has_keyword3])


class MajorEvents(Event):
    """Represents data for a major (COVID-19 related) event"""
    location: str

    def __init__(self, title: str, date: datetime.date, location: str, description: str) -> None:
        Event.__init__(self, title, date, description)
        self.location = location


def gather_keywords(filename: str) -> list[str]:
    """Return the keywords in the file filename as a list of strings"""
    with open(filename, 'r') as f:
        return f.readlines()


if __name__ == '__main__':
    import python_ta
    import python_ta.contracts

    python_ta.contracts.DEBUG_CONTRACTS = False
    python_ta.contracts.check_all_contracts()

    import doctest

    doctest.testmod()

    python_ta.check_all(config={
        'extra-imports': ['datetime'],
        'allowed-io': ['gather_keywords'],
        'max-line-length': 100,
        'disable': ['R1705', 'C0200']
    })
