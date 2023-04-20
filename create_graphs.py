"""CSC110 Final Project Submission: Creating Graphs

Instructions (READ THIS FIRST!)
===============================

This Python module contains the code necessary to create and write all of the displayed
graphs (in the GUI) to HTML files. It uses the "plotly" Python library, as well as "events_read.py"
and"covid_data.py" to create line graphs and histograms to display the data in multiple ways.

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
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from events import NewsEvents, MajorEvents
from events_read import return_relevant_news, read_file
from covid_data import read_covid_file


def get_filtered_news_data() -> list[NewsEvents]:
    """Return a list of NewsEvents containing the 2 news datasets filtered for Asian keywords"""
    unfiltered_news1 = read_file('data/news_data.csv', 'news')
    unfiltered_news2 = read_file('data/news.csv', 'news')

    unfiltered_news = unfiltered_news1[1] + unfiltered_news2[1]

    return return_relevant_news(unfiltered_news)


def count_articles(month: bool) -> tuple[list, list]:
    """Return a tuple with two elements representing a list of dates and a list of articles
    containing an Asian keyword on that date.

    The month boolean determines whether or not the data will be grouped by month"""
    filtered_data = get_filtered_news_data()
    data = {}
    for event in filtered_data:
        if month:
            date = datetime.date(event.date.year, event.date.month, 1)
        else:
            date = event.date

        if date in data:
            data[date].append(event)
        else:
            data[date] = [event]

    dates = sorted([item for item in data if item >= datetime.date(2019, 10, 1)])
    num_articles = [len(data[article_date]) for article_date in dates]

    return (dates, num_articles)


def get_covid_data() -> tuple[list, list, list]:
    """Return a tuple of the dates, # of daily COVID-19 cases, and # of total COVID-19 cases
    in Canada from the info in the dataset covid19_data"""
    data = read_covid_file('data/covid19_data.csv')
    dates = []
    daily_cases = []
    total_cases = []
    for item in data:
        if item.date > datetime.date(2021, 3, 18):
            break
        dates.append(item.date)
        daily_cases.append(item.daily_cases)
        total_cases.append(item.total_cases)

    return (dates, daily_cases, total_cases)


def get_major_events() -> list[MajorEvents]:
    """Returns a list of Major Events."""
    return read_file('data/major_events.csv', 'major')[1]


def write_line_graphs() -> None:
    """Create and writes line graphs to html files"""
    # news article data
    dates, num_articles = count_articles(False)
    covid_dates, daily_cases, _ = get_covid_data()

    # plain line graph of article data
    article_line = px.line(x=dates, y=num_articles, title='Asian Mention In Canadian News \
    (Oct 2019 - Mar 2021)', labels={'x': 'Date', 'y': 'Number of \
    Articles Mentioning Asia/East Asian Countries'})

    # plain line graph of covid data
    covid_line = px.line(x=covid_dates, y=daily_cases, title='Daily COVID-19 Cases \
    (Jan 2020 - Mar 2021)', labels={'x': 'Date', 'y': 'Number of Cases'})

    # write all to hmtl files
    article_line.write_html('article_line.html')
    covid_line.write_html('covid_line.html')


def write_histogram() -> None:
    """Create and writes histogram graphs to html files"""
    dates, num_articles = count_articles(False)
    covid_dates, daily_cases, _ = get_covid_data()

    # article histogram
    months, article_in_mo = count_articles(True)
    article_histogram = go.Figure()
    article_histogram.add_trace(go.Bar(x=months, y=article_in_mo))
    article_histogram.update_layout(title='Asian Mention In Canadian News (Oct 2019 - Mar 2021)')
    article_histogram.update_yaxes(title_text='Number of Mentions')

    # covid histogram
    # (first get monthly stats)
    month = covid_dates[0].month
    covid_months = [datetime.date(2020, 1, 1)]
    cases_in_mo = [0]
    index = 0  # current index of new lists
    for i in range(len(covid_dates)):
        if covid_dates[i].month == month:  # adding data from the same month
            cases_in_mo[index] += daily_cases[i]
        else:  # a new month has started
            covid_months.append(datetime.date(covid_dates[i].year, covid_dates[i].month, 1))
            cases_in_mo.append(0)
            index += 1

        month = covid_dates[i].month

    covid_histogram = go.Figure()
    covid_histogram.add_trace(go.Bar(x=covid_months, y=cases_in_mo))
    covid_histogram.update_layout(title='Monthly COVID-19 Cases (Jan 2020 - Mar 2021)')
    covid_histogram.update_yaxes(title_text='Number of Cases')

    # writes to html files
    article_histogram.write_html('article_histogram.html')
    covid_histogram.write_html('covid_histogram.html')


def write_stacked_graph() -> None:
    """Create and write the stacked graph to an html file"""
    dates, num_articles = count_articles(False)
    covid_dates, daily_cases, _ = get_covid_data()
    # stacked line graphs of article and covid data
    stacked_line_graph = make_subplots(specs=[[{"secondary_y": True}]])
    # add both graphs
    stacked_line_graph.add_trace(go.Scatter(x=dates, y=num_articles, mode='lines',
                                            name='Asian Mention in News'))
    stacked_line_graph.add_trace(go.Scatter(x=covid_dates, y=daily_cases, mode='lines',
                                            name='Daily COVID-19 Cases'), secondary_y=True)
    # update layouts
    stacked_line_graph.update_layout(xaxis_title_text='Date', yaxis_title_text='Number of Mentions',
                                     title_text='Comparison of Asian Mention in News Articles '
                                                'to Daily COVID-19 Cases')
    stacked_line_graph.update_yaxes(title_text='Number of Cases', secondary_y=True)

    major_events = get_major_events()

    for event in major_events:
        if event.date >= datetime.date(2021, 3, 18):
            continue

        stacked_line_graph.add_scatter(x=[event.date], y=[16], name=event.title,
                                       hoverinfo='text',
                                       hovertemplate='<b>' + event.title + '</b><br><br>'
                                                     + 'Date: ' + str(event.date)
                                                     + '<br>Location: ' + event.location
                                                     + '<br>Description: ' + event.description
                                                     + '<extra></extra>',
                                       marker=dict(size=12, color='violet',
                                                   line=dict(width=2,
                                                             color='DarkSlateGrey')))

    stacked_line_graph.write_html('stacked_line_graph.html')


if __name__ == '__main__':
    import python_ta
    import python_ta.contracts

    python_ta.contracts.DEBUG_CONTRACTS = False
    python_ta.contracts.check_all_contracts()

    import doctest

    doctest.testmod()

    python_ta.check_all(config={
        'extra-imports': ['datetime', 'python_ta.contracts', 'plotly.express',
                          'plotly.graph_objects', 'events', 'events_read', 'covid_data',
                          'plotly.subplots'],
        'allowed-io': ['get_filtered_news_data', 'count_articles', 'get_covid_data',
                       'get_major_events', 'write_graphs'],
        'max-line-length': 100,
        'disable': ['R1705', 'C0200']
    })
