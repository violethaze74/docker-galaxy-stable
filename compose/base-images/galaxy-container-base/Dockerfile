FROM buildpack-deps:22.04 as build_apptainer

COPY ./files/common_cleanup.sh /usr/bin/common_cleanup.sh

# Install Go (only needed for building apptainer)
ENV GO_VERSION=1.22.7
RUN apt update && apt install --no-install-recommends cryptsetup-bin uuid-dev libseccomp-dev libfuse-dev libfuse3-dev -y \
    && wget https://dl.google.com/go/go${GO_VERSION}.linux-amd64.tar.gz \
    && tar -C /usr/local -xzvf go${GO_VERSION}.linux-amd64.tar.gz \
    && rm go${GO_VERSION}.linux-amd64.tar.gz \
    && /usr/bin/common_cleanup.sh

ENV PATH=/usr/local/go/bin:${PATH}
ENV APPTAINER_VERSION=1.3.4
RUN wget https://github.com/apptainer/apptainer/releases/download/v${APPTAINER_VERSION}/apptainer-${APPTAINER_VERSION}.tar.gz \
    && mkdir -p apptainer \
    && tar -xzf apptainer-${APPTAINER_VERSION}.tar.gz --strip-components=1 -C apptainer \
    && cd apptainer \
    && ./mconfig --with-suid \
    && make -C builddir \
    && /usr/bin/common_cleanup.sh


# --- Final image ---
FROM ubuntu:22.04 as final

COPY ./files/common_cleanup.sh /usr/bin/common_cleanup.sh

# Base dependencies
RUN apt update && apt install --no-install-recommends ca-certificates python3-distutils squashfs-tools tzdata -y \
    && /usr/bin/common_cleanup.sh

# Install Docker
RUN apt update \
    && apt install --no-install-recommends docker.io -y \
    && /usr/bin/common_cleanup.sh

# Install Apptainer
COPY --from=build_apptainer /apptainer /apptainer
RUN apt update && apt install --no-install-recommends make -y \
    && make -C /apptainer/builddir install \
    && apt remove make -y \
    && rm -rf /apptainer \
    && sed -e '/bind path = \/etc\/localtime/s/^/#/g' -i /usr/local/etc/apptainer/apptainer.conf \
    && /usr/bin/common_cleanup.sh
