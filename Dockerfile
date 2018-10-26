FROM python:3.7

WORKDIR /usr/app

# Allow stdout to be printed to console
ENV PYTHONUNBUFFERED=1

# Install requirements first (allows caching)
ADD ./requirements.txt ./
RUN pip install -r requirements.txt

ADD ./ ./
RUN python manage.py collectstatic --noinput

CMD ["bash", "docker-entrypoint.sh"]
