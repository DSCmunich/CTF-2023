FROM trafex/php-nginx:latest

COPY . /var/www/html

USER root
RUN chmod 777 /var/www/html/uploads
USER nobody
