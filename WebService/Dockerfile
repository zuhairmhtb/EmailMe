FROM python:3.7

ARG privatepypiurl
ARG privatepypiusername
ARG privatepypipassword

WORKDIR /usr/src/app

COPY ./emailme.webservice emailme.webservice

RUN apt-get update && apt-get install curl && \
curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python3 -

ENV PATH="${PATH}:/root/.poetry/bin" \
POETRY_NO_INTERACTION=1

WORKDIR /usr/src/app/emailme.webservice

RUN poetry config virtualenvs.create false && \
poetry config repositories.ppypi $privatepypiurl && \
poetry config http-basic.ppypi  $privatepypiusername $privatepypipassword && \
poetry install

RUN poetry run python emailme_webservice/manage.py makemigrations && \
poetry run python emailme_webservice/manage.py migrate

CMD [ "./startup.sh" ]