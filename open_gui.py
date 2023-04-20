"""CSC110 Final Project Submission: Opening the GUI

Instructions (READ THIS FIRST!)
===============================

This Python module contains the code necessary to create the interactive portion of the data.
When run, the program will produce a GUI (graphical user interface) created by
the Python library 'tkinter' in which you may choose which of the various interactive
formats you would like to display the data with, opening it in your computer's default browser.
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
import tkinter as tk
import webbrowser
import os
from create_graphs import write_line_graphs, write_stacked_graph, write_histogram


def create_gui() -> None:
    """Creates a GUI to view each form of graphical analysis corresponding to the collected data"""
    write_line_graphs()  # writes .html files of each graph to the project folder
    write_stacked_graph()
    write_histogram()

    root = tk.Tk()
    root.title('Asian Hate Speech Following COVID-19 Pandemic')
    root.geometry("1085x265")

    b1 = tk.PhotoImage(file='article_line.png')
    b2 = tk.PhotoImage(file='article_histogram.png')
    b3 = tk.PhotoImage(file='covid_line.png')
    b4 = tk.PhotoImage(file='covid_histogram.png')
    b5 = tk.PhotoImage(file='stacked_line_graph.png')

    tk.Button(root, image=b1, command=lambda url='article_line.html': open_web(url))\
        .place(x=50, y=20)
    tk.Button(root, image=b2, command=lambda url='article_histogram.html': open_web(url))\
        .place(x=250, y=20)
    tk.Button(root, image=b3, command=lambda url='covid_line.html': open_web(url))\
        .place(x=450, y=20)
    tk.Button(root, image=b4, command=lambda url='covid_histogram.html': open_web(url))\
        .place(x=650, y=20)
    tk.Button(root, image=b5, command=lambda url='stacked_line_graph.html': open_web(url))\
        .place(x=850, y=20)

    root.mainloop()


def open_web(url: str) -> None:
    """Opens url in the default browser of the computer.

    Preconditions:
      - url refers to a valid html file in the proper format and in the same directory as this file.
    """
    webbrowser.open('file://' + os.path.realpath(url))


if __name__ == '__main__':
    import python_ta
    import python_ta.contracts
    python_ta.contracts.DEBUG_CONTRACTS = False
    python_ta.contracts.check_all_contracts()

    import doctest

    doctest.testmod()

    python_ta.check_all(config={
        'extra-imports': ['python_ta.contracts', 'tkinter', 'webbrowser', 'os', 'create_graphs'],
        'allowed-io': ['create_gui', 'open_web'],
        'max-line-length': 100,
        'disable': ['R1705', 'C0200']
    })
