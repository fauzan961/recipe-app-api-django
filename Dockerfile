FROM python:3.10-alpine3.17
LABEL maintainer=""

ENV PYTHONBUFFERED 1

COPY ./requirements.txt /tmp/requirements.txt
COPY ./requirements.dev.txt /tmp/requirements.dev.txt
COPY ./app /app
WORKDIR /app
EXPOSE 8000

# Setting defualt Arg to false 
ARG DEV=false

RUN python -m venv /py && \
    /py/bin/pip install --upgrade pip && \
    apk add --update --no-cache postgresql-client && \
    apk add --update --no-cache --virtual .tmp-build-deps \
    build-base postgresql-dev musl-dev && \
    /py/bin/pip install -r /tmp/requirements.txt && \ 
    # If condition starts here which checks if the DEV argument is true or false, if true it will install req.dev.txt 
    if [ $DEV = "true" ]; \
    then /py/bin/pip install -r /tmp/requirements.dev.txt ; \
    fi && \
    # is used to end the if block
    rm -rf /tmp && \
    apk del .tmp-build-deps && \
    adduser \
    --disabled-password\
    --no-create-home\
    django-user 

ENV PATH="/py/bin:$PATH"

USER django-user