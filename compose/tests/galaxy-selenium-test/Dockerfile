FROM selenium/standalone-chrome:4.25.0

ARG GALAXY_RELEASE=release_24.1
ARG GALAXY_REPO=https://github.com/galaxyproject/galaxy

ENV GALAXY_ROOT_DIR=/galaxy
ENV GALAXY_PYTHON=/usr/bin/python3

USER root
RUN apt update && apt install --no-install-recommends python3-dev python3-pip libpq-dev 2to3 -y && rm -rf /var/lib/apt/lists/* \
    && mkdir "${GALAXY_ROOT_DIR}" \
    && chown seluser "${GALAXY_ROOT_DIR}"

USER seluser
RUN mkdir -p $GALAXY_ROOT_DIR && \
    curl -L -s $GALAXY_REPO/archive/$GALAXY_RELEASE.tar.gz | tar xzf - --strip-components=1 -C $GALAXY_ROOT_DIR \
    && cd "${GALAXY_ROOT_DIR}" \
    && ./scripts/common_startup.sh --skip-client-build --dev-wheels

COPY run.sh /usr/bin/run.sh

CMD "/usr/bin/run.sh"
