FROM python:3-buster

WORKDIR /root
ADD requirements.txt /root

# install various things
RUN apt-get update && apt-get install -y \
  vim \
  less \
  apt-transport-https \
  ca-certificates \
  gnupg

# install python dependencies
RUN pip install -r requirements.txt
