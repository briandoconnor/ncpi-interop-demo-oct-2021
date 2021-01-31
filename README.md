# Docker Local Development Environments

## About

I wanted to create a simple development environment that I could fork to quickly  
get started on a Python (or another) project.  By using Docker Compose it allowed me to create
multi-container applications using different technologies and stitch them together.
For script development it gives me the ability to create a container with all the software I need
and I can create a new environment for different scripts if needed.

## Origin

This project is inspired by, and forked from, this blog post:

**🐳 Simplified guide to using Docker for local development environment**

_The blog link :_

[https://blog.atulr.com/docker-local-environment/](https://blog.atulr.com/docker-local-environment/)

## Running

To run the example:

- `git clone https://github.com/briandoconnor/blog-docker-dev-environment-example.git`
- `docker-compose up` or `docker-compose up -d` if you want to avoid console output

Details about each service and how to run them is present in the individual services directories.

## My Modifications

I'm leaving the go and node services in place but turning them off in the
docker-compose.yml file.  The old docker-compose is preserved here.

I've reorganized the services into the `services` directory and the
working directory is mounted and shared across the docker containers when run.

## Basic Python Script

I have a basic script located in `working/scripts/basic_python_script/process.py`
that shows how to use argparse and json, items that I routinely need to use in
simple scripts.

## Python Version

See the [official python images](https://hub.docker.com/_/python) on DockerHub
as well as the [releases of Debian](https://wiki.debian.org/DebianReleases).  I'm
using Debian Buster and Python 3 as the basis for the Python environment that gets
launched:

    python:3-buster

It's probably a good idea to use a specific version number of Python when
writing real scripts/services.

## Connecting to Python Dev Environments

Once you launch with `docker-compose up` you can login in to the Python service
container using:

```
# list out the running containers
$> docker ps
CONTAINER ID   IMAGE             COMMAND                  CREATED          STATUS          PORTS                    NAMES
02d2b8fce3af   python:3-buster   "sh -c 'pip install …"   44 seconds ago   Up 43 seconds   0.0.0.0:9000->9000/tcp   blog-docker-dev-environment-example_py-dev_1

# connect to this running container
$> docker exec -it 02d2b8fce3af /bin/bash

# now within the container I'm running as root and in the ~/py1 directory
# which is the directory containing the flask app
root@02d2b8fce3af:~/py1# whoami
root

# now if I go to ~/py-dev it contains the working directory with my scripts
root@02d2b8fce3af:~# cd ~/py-dev/
root@02d2b8fce3af:~/py-dev# ls
scripts 
```
