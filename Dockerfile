FROM python:3.10-alpine

# written by: Oliver Cordes 2022-06-01
# changed by: Oliver Cordes 2022-06-01

RUN adduser -D sbs

WORKDIR /home/sbs

COPY requirements.txt requirements.txt

# add a build structure for python modules
RUN apk --no-cache add --virtual .build-dependencies zlib-dev jpeg-dev gcc libc-
dev linux-headers

RUN python -m venv venv
RUN venv/bin/pip install --no-cache-dir -r requirements.txt
RUN venv/bin/pip install --no-cache-dir gunicorn



FROM python:3.10-alpine

# add graphics and sqlite
RUN apk --no-cache add libjpeg-turbo sqlite

# add the rayqueue user
RUN adduser -D sbs

# copy from previous build
COPY --from=0 /home /home

