FROM python:3.11-alpine

WORKDIR /app


ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV DJANGO_SETTINGS_MODEULE mycoffee.settings

RUN pip install --no-cache-dir --upgrade pip && \
    apk add --no-cache pango fontconfig ttf-freefont font-noto terminus-font \
    && fc-cache -f \ 
    && fc-list | sort

COPY ./requirements-dev.txt /app

RUN pip install --no-cache-dir -r requirements-dev.txt

COPY . /app
RUN chmod +x /app/entrypoint.sh

CMD [ "/app/entrypoint.sh" ] 
