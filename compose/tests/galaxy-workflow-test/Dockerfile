FROM alpine:3.17

ENV TEST_REPO=${TEST_REPO:-https://github.com/jyotipm29/workflow-testing} \
    TEST_RELEASE=${TEST_RELEASE:-24.1}

RUN apk add --no-cache bash python3 py3-pip curl \
    && apk add --no-cache --virtual build-dep gcc make libc-dev xz-dev bzip2-dev hdf5-dev musl-dev linux-headers python3-dev \
    && pip3 install planemo \
    && mkdir /src && cd /src \
    && curl -L -s $TEST_REPO/archive/$TEST_RELEASE.tar.gz | tar xzf - --strip-components=1 \
    && apk del build-dep

ADD ./run.sh /usr/bin/run.sh

WORKDIR /src

ENTRYPOINT /usr/bin/run.sh
