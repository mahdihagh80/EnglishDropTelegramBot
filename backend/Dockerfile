FROM python:3.10.12

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt update && apt install -y cron && touch /var/log/cron.log

WORKDIR /backend

COPY . .

RUN pip install --upgrade pip && pip install -r requirements.txt

RUN python manage.py crontab add && python manage.py collectstatic --noinput

CMD printenv | grep "BOT_TOKEN" >> /etc/environment; service cron restart; gunicorn backend.wsgi:application --bind 0.0.0.0:8000 --workers=2