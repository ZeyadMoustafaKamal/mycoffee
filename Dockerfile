FROM python:3.11.4-slim-buster

WORKDIR /app

COPY ./requirements-dev.txt /app


ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip install --upgrade pip \
    && pip install -r requirements-dev.txt 
COPY . /app
RUN python manage.py migrate \
    && python manage.py collectstatic --noinput \
    && python manage.py load_data
RUN chmod += ./entrypoint.sh

ENTRYPOINT [ "./entrypoint.sh" ]
