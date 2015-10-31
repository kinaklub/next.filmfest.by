FROM fedora:22
MAINTAINER Stas Rudakou "stas@garage22.net"

RUN dnf -y update; dnf clean all;
RUN dnf -y install python python-virtualenv gcc postgresql-devel libjpeg-devel zlib-devel

ENV PYTHONUNBUFFERED 1

RUN useradd -d /app -m filmfest
USER filmfest
RUN virtualenv /app
RUN mkdir /app/src
WORKDIR /app/src

ADD . /app/src/
RUN /app/bin/pip install -r requirements/dev.txt

ENV DJANGO_SETTINGS_MODULE wagtrail.settings.docker
ENTRYPOINT ["/app/bin/python", "manage.py"]
