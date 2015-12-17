FROM java:openjdk-7-jdk

MAINTAINER Tommy Lau <tommy@gen-new.com>

# Download and extract Bamboo and create the required directory layout.
# Try to limit the number of RUN instructions to minimise the number of layers that will need to be created.
RUN apt-get update -qq                                                            \
    && apt-get install -y --no-install-recommends git openssh-client zip          \
    && apt-get clean autoclean                                                    \
    && apt-get autoremove --yes                                                   \
    && rm -rf                  /var/lib/{apt,dpkg,cache,log}/

# Use the default unprivileged account. This could be considered bad practice
# on systems where multiple processes end up being executed by 'daemon' but
# here we only ever run one process anyway.
ENV RUN_USER            daemon
ENV RUN_GROUP           daemon

ENV BAMBOO_HOME         /var/atlassian/application-data/bamboo

# Install Atlassian Bamboo to the following location
ENV BAMBOO_INSTALL_DIR   /opt/atlassian/bamboo

ENV BAMBOO_VERSION 5.9.7
ENV DOWNLOAD_URL        https://www.atlassian.com/software/bamboo/downloads/binary/atlassian-bamboo-${BAMBOO_VERSION}.tar.gz

RUN mkdir -p                             ${BAMBOO_INSTALL_DIR} \
    && curl -L --silent                  ${DOWNLOAD_URL} | tar -xz --strip=1 -C "$BAMBOO_INSTALL_DIR" \
    && mkdir -p                          ${BAMBOO_INSTALL_DIR}/conf/Catalina      \
    && chmod -R 700                      ${BAMBOO_INSTALL_DIR}/conf/Catalina      \
    && chmod -R 700                      ${BAMBOO_INSTALL_DIR}/logs               \
    && chmod -R 700                      ${BAMBOO_INSTALL_DIR}/temp               \
    && chmod -R 700                      ${BAMBOO_INSTALL_DIR}/work               \
    && chown -R ${RUN_USER}:${RUN_GROUP} ${BAMBOO_INSTALL_DIR}/                   \
    && cd ${BAMBOO_INSTALL_DIR}/atlassian-bamboo/WEB-INF/lib                      \
    && curl -SLO "https://gist.github.com/TommyLau/8a5ce4629d027f7884e6/raw/18fb5f18b5cf7997a37169c0ba4f17e2e38c7c96/atlassian-extras-decoder-v2-3.2.jar" \
    && cd ../atlassian-bundled-plugins/                                           \
    && curl -SLO "https://gist.github.com/TommyLau/8a5ce4629d027f7884e6/raw/a382eb800b33d509a0ef4db9508956c8ea89fc96/atlassian-universal-plugin-manager-plugin-2.16.2.jar"

USER ${RUN_USER}:${RUN_GROUP}

VOLUME ["${BAMBOO_HOME}"]

# HTTP Port
EXPOSE 8085

# Agent Port
EXPOSE 54663

WORKDIR $BAMBOO_INSTALL_DIR

# Run in foreground
CMD ["./bin/start-bamboo.sh", "-fg"]
