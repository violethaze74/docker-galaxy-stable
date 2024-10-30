ARG DOCKER_REGISTRY=quay.io
ARG DOCKER_REGISTRY_USERNAME=bgruening
ARG IMAGE_TAG=latest

FROM buildpack-deps:22.04 as build_base

ENV EXPORT_DIR=/export \
    GALAXY_ROOT_DIR=/galaxy \
    HTCONDOR_ROOT=/opt/htcondor

ENV GALAXY_STATIC_DIR=$GALAXY_ROOT_DIR/static \
    GALAXY_EXPORT=$EXPORT_DIR/galaxy \
    GALAXY_CONFIG_DIR=$GALAXY_ROOT_DIR/config \
    GALAXY_CONFIG_TOOL_DEPENDENCY_DIR=/tool_deps \
    GALAXY_CONFIG_TOOL_PATH=$GALAXY_ROOT_DIR/tools \
    GALAXY_CONFIG_TOOL_DATA_PATH=$GALAXY_ROOT_DIR/tool-data \
    GALAXY_VIRTUAL_ENV=$GALAXY_ROOT_DIR/.venv \
    GALAXY_DATABASE_PATH=$GALAXY_ROOT_DIR/database

ENV GALAXY_USER=galaxy \
    GALAXY_GROUP=galaxy \
    GALAXY_UID=1450 \
    GALAXY_GID=1450 \
    GALAXY_HOME=/home/galaxy

ENV GALAXY_CONDA_PREFIX=$GALAXY_CONFIG_TOOL_DEPENDENCY_DIR/_conda \
    MINICONDA_VERSION=py310_24.5.0-0

RUN groupadd -r $GALAXY_USER -g $GALAXY_GID \
    && useradd -u $GALAXY_UID -r -g $GALAXY_USER -d $GALAXY_HOME -c "Galaxy user" --shell /bin/bash $GALAXY_USER \
    && mkdir $GALAXY_HOME \
    && chown -R $GALAXY_USER:$GALAXY_USER $GALAXY_HOME

FROM build_base as build_miniconda
COPY ./files/common_cleanup.sh /usr/bin/common_cleanup.sh
# Install Miniconda
RUN curl -s -L "https://repo.anaconda.com/miniconda/Miniconda3-${MINICONDA_VERSION}-Linux-x86_64.sh" > ~/miniconda.sh \
    && /bin/bash ~/miniconda.sh -b -p $GALAXY_CONDA_PREFIX \
    && rm ~/miniconda.sh \
    && ln -s $GALAXY_CONDA_PREFIX/etc/profile.d/conda.sh /etc/profile.d/conda.sh \
    && echo ". $GALAXY_CONDA_PREFIX/etc/profile.d/conda.sh" >> $GALAXY_HOME/.bashrc \
    && echo "conda activate base" >> $GALAXY_HOME/.bashrc \
    && export PATH=$GALAXY_CONDA_PREFIX/bin/:$PATH \
    && conda config --add channels defaults \
    && conda config --add channels bioconda \
    && conda config --add channels conda-forge \
    && conda install virtualenv pip ephemeris \
    && conda clean --packages -t -i \
    && /usr/bin/common_cleanup.sh

FROM build_base as build_galaxy

ARG GALAXY_RELEASE=release_24.1
ARG GALAXY_REPO=https://github.com/galaxyproject/galaxy

COPY ./files/common_cleanup.sh /usr/bin/common_cleanup.sh
# Install Galaxy
RUN apt update && apt install --no-install-recommends libcurl4-openssl-dev libssl-dev python3-dev python3-pip -y \
    && update-alternatives --install /usr/bin/python python /usr/bin/python3 10 \
    && mkdir "${GALAXY_ROOT_DIR}" \
    && curl -L -s $GALAXY_REPO/archive/$GALAXY_RELEASE.tar.gz | tar xzf - --strip-components=1 -C $GALAXY_ROOT_DIR \
    && cd $GALAXY_ROOT_DIR \
    && ./scripts/common_startup.sh \
    && . $GALAXY_ROOT_DIR/.venv/bin/activate \
    && pip3 install drmaa psycopg2 pycurl pykube redis \
    && pip3 install importlib-metadata importlib-resources pathlib2 ruamel.yaml.clib typing zipp \
    && deactivate \
    && rm -rf .ci .circleci .coveragerc .gitignore .travis.yml CITATION CODE_OF_CONDUCT.md CONTRIBUTING.md CONTRIBUTORS.md \
              LICENSE.txt Makefile README.rst SECURITY_POLICY.md pytest.ini tox.ini \
              contrib doc config/plugins lib/galaxy_test test test-data \
              .venv/lib/node_modules .venv/src/node-v10.15.3-linux-x64 \
              .venv/include/node .venv/bin/node .venv/bin/nodeenv \
    && /usr/bin/common_cleanup.sh

# --- Final image ---
FROM $DOCKER_REGISTRY/$DOCKER_REGISTRY_USERNAME/galaxy-cluster-base:$IMAGE_TAG as final

COPY ./files/common_cleanup.sh /usr/bin/common_cleanup.sh
COPY ./files/create_galaxy_user.py /usr/local/bin/create_galaxy_user.py

ENV EXPORT_DIR=/export \
    GALAXY_ROOT_DIR=/galaxy \
    GALAXY_PYTHON=/usr/bin/python3 \
    HTCONDOR_ROOT=/opt/htcondor

ENV GALAXY_RELEASE=${GALAXY_RELEASE:-release_24.1} \
    GALAXY_REPO=${GALAXY_REPO:-https://github.com/galaxyproject/galaxy} \
    GALAXY_STATIC_DIR=$GALAXY_ROOT_DIR/static \
    GALAXY_EXPORT=$EXPORT_DIR/galaxy \
    GALAXY_CONFIG_DIR=$GALAXY_ROOT_DIR/config \
    GALAXY_CONFIG_TOOL_DEPENDENCY_DIR=/tool_deps \
    GALAXY_CONFIG_TOOL_PATH=$GALAXY_ROOT_DIR/tools \
    GALAXY_CONFIG_TOOL_DATA_PATH=$GALAXY_ROOT_DIR/tool-data \
    GALAXY_VIRTUAL_ENV=$GALAXY_ROOT_DIR/.venv \
    GALAXY_DATABASE_PATH=$GALAXY_ROOT_DIR/database

ENV GALAXY_USER=galaxy \
    GALAXY_GROUP=galaxy \
    GALAXY_UID=1450 \
    GALAXY_GID=1450 \
    GALAXY_HOME=/home/galaxy

ENV GALAXY_CONFIG_FILE=$GALAXY_CONFIG_DIR/galaxy.yml

# Set permissions
RUN groupadd -r $GALAXY_USER -g $GALAXY_GID \
    && useradd -u $GALAXY_UID -r -g $GALAXY_USER -d $GALAXY_HOME -c "Galaxy user" --shell /bin/bash $GALAXY_USER \
    && /usr/bin/common_cleanup.sh

# Install remaining dependencies
RUN apt update && apt install --no-install-recommends curl gcc gnupg2 libgomp1 liblzma-dev libbz2-dev libpq-dev \
                                                      libcurl4-openssl-dev libssl-dev \
                                                      mercurial make netcat python3-dev python3-setuptools python3-pip \
                                                      zlib1g-dev sudo -y \
    # Cython and wheel are needed to later install pysam..
    && pip3 install Cython wheel \
    && pip3 install pysam \
    && /usr/bin/common_cleanup.sh

# GALAXY_USER should be able to run docker without root permissions
RUN usermod -aG docker $GALAXY_USER

# Make Python3 standard
RUN update-alternatives --install /usr/bin/python python /usr/bin/python3 10

COPY --chown=$GALAXY_USER:$GALAXY_USER --from=build_galaxy ${GALAXY_ROOT_DIR} ${GALAXY_ROOT_DIR}
COPY --chown=$GALAXY_USER:$GALAXY_USER --from=build_miniconda ${GALAXY_CONFIG_TOOL_DEPENDENCY_DIR} ${GALAXY_CONFIG_TOOL_DEPENDENCY_DIR}
COPY --chown=$GALAXY_USER:$GALAXY_USER --from=build_miniconda ${GALAXY_HOME} ${GALAXY_HOME}
COPY --chown=$GALAXY_USER:$GALAXY_USER --from=build_miniconda /etc/profile.d/conda.sh /etc/profile.d/conda.sh

# The following commands will be executed as the galaxy user
USER $GALAXY_USER

# We need to set $HOME for some Tool Shed tools (e.g Perl libs with $HOME/.cpan)
ENV HOME=$GALAXY_HOME

# Switch back to User root
USER root

COPY ./files/start.sh /usr/bin/start.sh

EXPOSE 80

ENTRYPOINT "/usr/bin/start.sh"
