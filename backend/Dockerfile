FROM python:3.6

# Ensure that Python outputs everything that's printed inside
# the application rather than buffering it.
ENV PYTHONUNBUFFERED 1

WORKDIR /app

COPY requirements ./requirements
RUN pip install --no-cache-dir \
    -r ./requirements/main.txt \
    -r ./requirements/dev.txt

COPY . ./

ENV PYTHONPATH $PYTHONPATH:/app/src

CMD ["./bin/server"]
