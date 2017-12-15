FROM playlog:latest

RUN apt-get update && apt-get install -y wget

ENV DOCKERIZE_VERSION v0.6.0
RUN wget -q https://github.com/jwilder/dockerize/releases/download/$DOCKERIZE_VERSION/dockerize-linux-amd64-$DOCKERIZE_VERSION.tar.gz \
    && tar -C /usr/local/bin -xzvf dockerize-linux-amd64-$DOCKERIZE_VERSION.tar.gz \
    && rm dockerize-linux-amd64-$DOCKERIZE_VERSION.tar.gz

WORKDIR /tests

COPY requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r ./requirements.txt

COPY . ./

ENV PYTHONPATH $PYTHONPATH:/tests/src

CMD ["./bin/run"]
