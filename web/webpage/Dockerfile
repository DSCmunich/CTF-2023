FROM trafex/php-nginx:latest

COPY . /var/www/html

USER root
RUN chmod 777 /var/www/html/uploads && rm /var/www/html/reset.php
COPY reset.php /root/reset.php
COPY uploads /root/uploads-original

USER nobody
