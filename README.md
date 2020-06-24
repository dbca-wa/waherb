# WAHerb

A Django prototype to manage herbarium collection data and taxonomic
information.

Requires Python 3.7+. Manage project virtual environment and
dependencies using `Poetry`.

~~~
poetry install
poetry run python manage.py check
~~~

Define project-local variables in a `.env` file. As a minimum we need `DATABASE_URL`.
