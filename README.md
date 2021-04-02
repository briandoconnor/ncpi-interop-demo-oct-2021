# NCPI Interop Demo

## About

This is a simple development environment used for a demo showing interop between
AnVIL, BioData Catalyst, and GMKF for the NIH Cloud Platforms Interoperability
effort.  

The main feature is a python script (download.py) that
takes a Gen3 token and a file UUID from the GMKF portal and then retrieves
the file from a signed URL from the AWS cloud.

This python script can be wrapped in a WDL and used to pull in GMKF
data into a Terra workspace for an analysis demo as part of the NCPI effort.

## Origins

This project environment is inspired by, and forked from, this blog post:

**🐳 Simplified guide to using Docker for local development environment**

_The blog link :_

[https://blog.atulr.com/docker-local-environment/](https://blog.atulr.com/docker-local-environment/)

## Dependencies

You need Docker (along with `docker-compose`) setup and running on your computer.

## Running

To run the environment that has all the dependencies installed:

- `git clone https://github.com/briandoconnor/ncpi-interop-demo.git`
- `docker-compose up --build` to build and launch a Docker environment

## Connecting

Once you have the Docker running, you can connect using:

```
# connect from your computer terminal
$> ./connect.sh

# now if I go to ~/py-dev it contains the working directory with my script
root@02d2b8fce3af:~# cd /root/py-dev/scripts/python_downloading_script

```

## Python Download Script Usage

I have a basic script located in `working/scripts/python_downloading_script/download.py`
that does the download.  Here's an example of how to run it.

### Get Your GMKF Token

Go to the [GMKF Data Portal](https://portal.kidsfirstdrc.org/dashboard) and
log in with whatever ID you want to use.  Then go to your profile and
make sure you connect with the Data Repositories (typically you'll use
your eRA Commons account to do this) and (optionally) connect to your
Cavatica account.  

![account linking](/images/account_links.png)

Once you've logged in, open up the developer tools in Chrome and look for a
`token?fence=gen3` request.  You'll need to copy the `authorization: Bearer`
token and use this with Python script in this repo to download data. I'm
not sure how long the token is good for but it seems to work for at least
24 hour.  You'll need to copy all the text after "Bearer " in this image.

![token](/images/example_token.png)

### Get the File IDs

Now that you have your

## Docker Image

## WDL

## Terra Workspace



## Python Version

See the [official python images](https://hub.docker.com/_/python) on DockerHub
as well as the [releases of Debian](https://wiki.debian.org/DebianReleases).  I'm
using Debian Buster and Python 3 as the basis for the Python environment that gets
launched:

    python:3-buster

It's probably a good idea to use a specific version number of Python when
writing real scripts/services.
