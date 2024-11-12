FROM alpine:3.17

ARG KIND_RELEASE=v0.24.0
ARG KUBECTL_RELEASE=v1.31.1

RUN apk add --no-cache docker

RUN apk add --no-cache --virtual build-deps wget \
    && apk add --no-cache bash \
    && wget -O /usr/bin/kind https://kind.sigs.k8s.io/dl/${KIND_RELEASE}/kind-linux-amd64 \
    && chmod +x /usr/bin/kind \
    && wget -O /usr/bin/kubectl https://dl.k8s.io/release/${KUBECTL_RELEASE}/bin/linux/amd64/kubectl \
    && chmod +x /usr/bin/kubectl \
    && apk del build-deps

ENV KIND_CONFIG_DIR=/kind
ENV KUBECONFIG=${KIND_CONFIG_DIR}/.kube/config

COPY docker-entrypoint.sh /usr/bin/docker-entrypoint.sh

ENTRYPOINT [ "/usr/bin/docker-entrypoint.sh" ]
