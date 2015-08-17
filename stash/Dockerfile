FROM java:openjdk-7-jre

MAINTAINER Tommy Lau <tommy@gen-new.com>

ENV DOWNLOAD_URL        https://downloads.atlassian.com/software/stash/downloads/atlassian-stash-

# https://confluence.atlassian.com/display/STASH/Stash+home+directory
ENV STASH_HOME          /var/atlassian/application-data/stash

# Install git, download and extract Stash and create the required directory layout.
# Try to limit the number of RUN instructions to minimise the number of layers that will need to be created.
RUN apt-get update -qq \
    && apt-get install -y --no-install-recommends git openssh-client zip \
    && apt-get clean autoclean \
    && apt-get autoremove --yes \
    && rm -rf /var/lib/{apt,dpkg,cache,log}/

# Use the default unprivileged account. This could be considered bad practice
# on systems where multiple processes end up being executed by 'daemon' but
# here we only ever run one process anyway.
ENV RUN_USER            daemon
ENV RUN_GROUP           daemon

# Install Atlassian Stash to the following location
ENV STASH_INSTALL_DIR   /opt/atlassian/stash

ENV STASH_VERSION 3.11.2

RUN mkdir -p                             ${STASH_INSTALL_DIR} \
    && curl -L --silent                  ${DOWNLOAD_URL}${STASH_VERSION}.tar.gz | tar -xz --strip=1 -C "$STASH_INSTALL_DIR" \
    && mkdir -p                          ${STASH_INSTALL_DIR}/conf/Catalina      \
    && chmod -R 700                      ${STASH_INSTALL_DIR}/conf/Catalina      \
    && chmod -R 700                      ${STASH_INSTALL_DIR}/logs               \
    && chmod -R 700                      ${STASH_INSTALL_DIR}/temp               \
    && chmod -R 700                      ${STASH_INSTALL_DIR}/work               \
    && chown -R ${RUN_USER}:${RUN_GROUP} ${STASH_INSTALL_DIR}/logs               \
    && chown -R ${RUN_USER}:${RUN_GROUP} ${STASH_INSTALL_DIR}/temp               \
    && chown -R ${RUN_USER}:${RUN_GROUP} ${STASH_INSTALL_DIR}/work               \
    && chown -R ${RUN_USER}:${RUN_GROUP} ${STASH_INSTALL_DIR}/conf               \
    && cd ${STASH_INSTALL_DIR}/atlassian-stash/WEB-INF/lib                       \
    && curl -SLO "https://gist.github.com/TommyLau/8a5ce4629d027f7884e6/raw/18fb5f18b5cf7997a37169c0ba4f17e2e38c7c96/atlassian-extras-decoder-v2-3.2.jar" \
    && chown 500.1000 atlassian-extras-decoder-v2-3.2.jar                        \
    && cd ../classes/                                                            \
    && curl -SLO "https://gist.github.com/TommyLau/8a5ce4629d027f7884e6/raw/4d1a3fc95f7d6be947fe4a4b79f4105b817294fe/atlassian-universal-plugin-manager-plugin-2.18.4.jar" \
    && zip -u9 stash-bundled-plugins.zip atlassian-universal-plugin-manager-plugin-2.18.4.jar \
    && rm -fr atlassian-universal-plugin-manager-plugin-2.18.4.jar \
    && chown 500.1000 stash-bundled-plugins.zip

USER ${RUN_USER}:${RUN_GROUP}

VOLUME ["${STASH_INSTALL_DIR}"]

# HTTP Port
EXPOSE 7990

# SSH Port
EXPOSE 7999

WORKDIR $STASH_INSTALL_DIR

# Run in foreground
CMD ["./bin/start-stash.sh", "-fg"]
