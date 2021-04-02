#!/usr/bin/env bash

docker exec -it `docker ps | grep ncpi-interop-demo | awk '{print $1}'` /bin/bash
