FROM mcr.microsoft.com/devcontainers/python:3.12

# install socat
RUN apt-get update
RUN apt-get install socat -y

# common folder for testing
RUN mkdir /srv/pts
RUN chmod 777 /srv/pts
RUN chmod +t /srv/pts