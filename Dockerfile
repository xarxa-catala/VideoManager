FROM python:3.7-buster

ENV MYSQL_ROOT_PASSWORD password

RUN apt-get update
RUN apt-get install -y python3 python3-venv python3-pip git mariadb-server mariadb-client libz-dev libjpeg-dev libfreetype6-dev python3-dev
RUN pip3 install Django mysqlclient django-simple-captcha

# Create the database.
RUN service mysql start &&\
    mysql -u root -p${MYSQL_ROOT_PASSWORD} -e "CREATE DATABASE xarxacat_multimedia;" &&\
    mysql -u root -p${MYSQL_ROOT_PASSWORD} -e "CREATE USER 'xarxacat'@'localhost' IDENTIFIED BY 'password'" &&\
    mysql -u root -p${MYSQL_ROOT_PASSWORD} -e "GRANT ALL PRIVILEGES ON xarxacat_multimedia.* TO 'xarxacat'@'localhost'" &&\
    mysql -u root -p${MYSQL_ROOT_PASSWORD} -e "FLUSH PRIVILEGES"

WORKDIR /app
COPY . /app

CMD service mysql start && python3 manage.py makemigrations && python3 manage.py migrate && python3 manage.py runserver 0.0.0.0:8000

EXPOSE 8000
