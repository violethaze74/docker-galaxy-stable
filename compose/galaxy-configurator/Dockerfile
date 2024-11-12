FROM alpine:3.17

RUN apk add --no-cache bash python3 py3-pip \
    && pip3 install j2cli[yaml] jinja2-ansible-filters

COPY ./templates /templates
COPY ./customize.py /customize.py
COPY ./run.sh /usr/bin/run.sh

ENTRYPOINT "/usr/bin/run.sh"
