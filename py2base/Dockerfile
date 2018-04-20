FROM ubuntu:16.04

MAINTAINER Dockerfiles

# Install required packages and remove the apt packages cache when done.

RUN apt-get update && \
    apt-get upgrade -y && \ 
    apt-get install -y \
	git \
	python \
	python-dev \
	python-setuptools \
	python-pip \
	nginx \
	supervisor \
	sqlite3 && \
	pip install -U pip setuptools && \
  	rm -rf /var/lib/apt/lists/*

# install uwsgi now because it takes a little while
RUN pip install uwsgi

# setup all the configfiles
RUN echo "daemon off;" >> /etc/nginx/nginx.conf

COPY ./conf/nginx.conf /etc/nginx/sites-available/default

COPY ./conf/supervisor.conf /etc/supervisor/conf.d/
# uwsgi
COPY ./conf/uwsgi/uwsgi.ini /opt/django/uwsgi.ini 
COPY ./conf/uwsgi/uwsgi_params /opt/django/uwsgi_params

COPY requirements.txt /opt/django/app/

RUN pip install -r /opt/django/app/requirements.txt

# install django, normally you would remove this step because your project would already

EXPOSE 80

CMD ["supervisord", "-n"]
