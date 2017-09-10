#!/bin/bash
# Forward logs to docker logs collector
set -e

mkdir -p /var/log/nginx
mkdir -p /var/log/playlog

exec tail -F /var/log/nginx/* /var/log/playlog/*
