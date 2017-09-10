#!/bin/bash
set -e
mkdir -p /var/log/playlog
exec /sbin/setuser playlog /home/playlog/backend/bin/server 2> /var/log/playlog/stderr.log 1> /var/log/playlog/stdout.log
