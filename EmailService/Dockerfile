FROM python:3.7

ARG privatepypiurl
ARG privatepypiusername
ARG privatepypipassword

WORKDIR /usr/src/app

COPY ./emailme.emailservice emailme.emailservice

RUN apt-get update && apt-get install curl && \
curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python3 -

ENV PATH="${PATH}:/root/.poetry/bin" \
POETRY_NO_INTERACTION=1

WORKDIR /usr/src/app/emailme.emailservice

RUN poetry config virtualenvs.create false && \
poetry config repositories.ppypi $privatepypiurl && \
poetry config http-basic.ppypi  $privatepypiusername $privatepypipassword && \
poetry install

CMD [ "./startup.sh" ]
