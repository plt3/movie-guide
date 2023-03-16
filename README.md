# movie-guide

> Django Webapp for Leonard Maltin's Movie Guide with data extracted from books in multiple PDF and ePub files

## Installation and Running:

- clone repository
- build virtual environment with `python3 -m venv venv`
- activate it with `source venv/bin/activate`
- install dependencies with `pip install -r requirements.txt`
- run development server with `python3 webApp/manage.py runserver`
- visit http://127.0.0.1:8000/ in browser to see web application

## Features:

- list movies by director, actor, country, year, or rating
- search over all these fields and title or review
- detailed movie view showing all fields
- admin interface to edit entries
