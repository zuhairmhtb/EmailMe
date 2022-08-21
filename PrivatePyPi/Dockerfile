FROM pypiserver/pypiserver:v1.5.0

# Receive username and password from docker-compose
ARG username
ARG password

# Install apache-utils to run the PyPi Server
RUN apk add apache2-utils

# Add credentials for the server
RUN htpasswd -scb /data/.htpasswd $username $password

# Start the PyPi Server
ENTRYPOINT [ "/entrypoint.sh" ]