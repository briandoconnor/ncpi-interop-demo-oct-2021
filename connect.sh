#!/usr/bin/env bash

docker exec -it `docker ps | grep ncpi-intero-demo | awk '{print $1}'` /bin/bash
