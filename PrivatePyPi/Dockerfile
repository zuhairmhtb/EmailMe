FROM pypiserver/pypiserver:v1.5.0

ARG username
ARG password

RUN apk add apache2-utils
RUN htpasswd -scb /data/.htpasswd $username $password

ENTRYPOINT [ "/entrypoint.sh" ]