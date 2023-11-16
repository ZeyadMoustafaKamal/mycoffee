FROM python:3.11-alpine

WORKDIR /app


ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY ./requirements-dev.txt /app

RUN pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements-dev.txt 
COPY . /app
RUN chmod +x /app/entrypoint.sh

CMD [ "/app/entrypoint.sh" ] 
