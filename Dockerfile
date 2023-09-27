FROM python:3.11-alpine

WORKDIR /app

COPY ./requirements-dev.txt /app


ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements-dev.txt 
COPY . /app
RUN python manage.py migrate \
    && python manage.py collectstatic --noinput \
    && python manage.py load_data

CMD [ "python", "manage.py", "runserver", "0.0.0.0:8000" ]
