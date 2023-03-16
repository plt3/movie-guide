# movie-guide

> Django webapp for Leonard Maltin's Movie Guide with data extracted from books in multiple PDF and ePub files

## Installation and Running:

- clone repository
- build virtual environment with `python3 -m venv venv`
- activate it with `source venv/bin/activate`
- install dependencies with `pip install -r requirements.txt`
- run development server with `python3 webApp/manage.py runserver`
- visit http://127.0.0.1:8000/ in browser to see web application
- NOTE: SQLite database not included in this repository, so running locally will not show the results in the screenshots below

## Features:

- list movies by director, actor, country, year, or rating
- search over all these fields and title or review
- detailed movie view showing all fields
- admin interface to edit entries

## Screenshots:

![home_page](https://user-images.githubusercontent.com/65266160/225480845-62443df9-dd7d-4336-ba32-da99189b128c.png)

![movie_detail](https://user-images.githubusercontent.com/65266160/225480921-580a6009-f830-42ba-afa7-a17e923c79f2.png)

![actor_page](https://user-images.githubusercontent.com/65266160/225480893-6e49570c-1125-457e-a16d-49e3cafb92ca.png)
