FROM phusion/baseimage:0.9.22

# Add "playlog" group and user
RUN addgroup --gid 9999 playlog && \
    adduser --uid 9999 --gid 9999 --disabled-password --gecos "Playlog" playlog && \
    usermod -L playlog

# Install required packages
RUN apt-get update && \
    apt-get install -y \
    nginx \
    python3 \
    python3-pip && \
    pip3 install -U --no-cache-dir pip setuptools

# Install backend requirements
COPY backend/requirements/main.txt ./requirements.txt
RUN pip install --no-cache-dir -r ./requirements.txt && \
    rm ./requirements.txt

WORKDIR /home/playlog

COPY backend/bin ./backend/bin
COPY backend/migrations ./backend/migrations
COPY backend/src ./backend/src
COPY frontend/build ./frontend
RUN chown -R playlog:playlog /home/playlog

COPY production/nginx.conf /etc/nginx/sites-available/default

# Add services
RUN cd /etc/service && mkdir nginx playlog logs-forwarder
COPY production/nginx.sh /etc/service/nginx/run
COPY production/playlog.sh /etc/service/playlog/run
COPY production/logs-forwarder.sh /etc/service/logs-forwarder/run
RUN find /etc/service/ -name 'run' -exec chmod +x '{}' \;

# Disbale cron
RUN touch /etc/service/cron/down

# Cleanup
RUN apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

ENV PYTHONPATH $PYTHONPATH:/home/playlog/backend/src
ENV PYTHONUNBUFFERED 1
ENV PLAYLOG_DEBUG false
ENV PLAYLOG_SESSION_LIFETIME 86400
ENV PLAYLOG_SERVER_HOST 0.0.0.0
ENV PLAYLOG_SERVER_PORT 8000

EXPOSE 8000 8001

CMD ["/sbin/my_init"]
