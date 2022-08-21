FROM python:3.7

# Receive PyPi credentials from compose file
ARG privatepypiurl
ARG privatepypiusername
ARG privatepypipassword

# Set the current working directory
WORKDIR /usr/src/app

# Copy our application codebase to the image
COPY ./emailme.emailservice emailme.emailservice

# Install poetry
RUN apt-get update && apt-get install curl && \
curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python3 -

# Set poetry path as environment variable to use the 'poetry command' from anywhere in terminal
ENV PATH="${PATH}:/root/.poetry/bin" \
POETRY_NO_INTERACTION=1

# Set current working directory
WORKDIR /usr/src/app/emailme.emailservice

# Configure private repository and install packages of the application
RUN poetry config virtualenvs.create false && \
poetry config repositories.ppypi $privatepypiurl && \
poetry config http-basic.ppypi  $privatepypiusername $privatepypipassword && \
poetry install

CMD [ "./startup.sh" ]
