## A well developed coffee market built with django

### How to install

- using docker
  - run `docker-compose up --build`
  - run `docker-compose exec web python manage.py collectstatic --noinput` to collect the static assets and run `docker-compose exec web python manage.py load_data` to load coffee data from the API
  - navigate to `127.0.0.1:8000`
- using a virtual environment
  - create a virtual environment by running `python -m venv .venv` for windows or `python3 -m venv .venv` for mac & linux
  - activate the virtual environment by running `.venv\Scripts\activate` for windows or `source .venv/bin/activate` for mac & linux
  - install dependencies by running `pip install -r requirements-dev.txt` for local environment and `pip install -r requirements.txt` for production
  - run `python manage.py migrate` to migrate the database
  - run `python manage.py collectstatic --noinput` to collect the static assets
  - run `python manage.py load_data` to get the data for the coffee products
  - navigate to `127.0.0.1:8000`

### How to manage dependencies
- If you want to add a package that will be used for the local and the production then add it to `requrements.in` then compile the dependencies by running `pip-compile requirements.in && pip-compile requirements-dev.in` then rebuild the container if you are using docker or just install the dependencies again by running `pip install -r requirements-dev.txt` 

- If you want to add a package that will be used just in the local environemnt then add it to the `requirements-dev.in` and compile it by running `pip-compile requirements-dev.in` then rebuild the container and if you are using docker or just install the dependencies again by running `pip install -r requirements-dev.txt`

### ToDo
- [x] Use HTMX in order to make the website feel like SPA applications
- [x] Customize the admin panel 
- [x] Add reports system that uses celery
- [ ] Add unit test in order to test the website in a good way
- [ ] Split docker and settings for local and production