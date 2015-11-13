FROM ubuntu:14.04

MAINTAINER Tommy Lau <tommy@gen-new.com>

ENV DOWNLOAD_URL        https://downloads.atlassian.com/software/confluence/downloads/atlassian-confluence-

ENV CONFLUENCE_HOME     /var/atlassian/application-data/confluence

# Install git, download and extract Stash and create the required directory layout.
# Try to limit the number of RUN instructions to minimise the number of layers that will need to be created.
RUN apt-get update -qq \
    && apt-get install -y --no-install-recommends curl software-properties-common \
    && echo oracle-java8-installer shared/accepted-oracle-license-v1-1 select true | debconf-set-selections \
    && apt-add-repository -y ppa:webupd8team/java \
    && apt-get update -qq \
    && apt-get install -y --no-install-recommends oracle-java8-installer \
    && apt-get clean autoclean \
    && apt-get autoremove --yes \
    && rm -rf /var/lib/{apt,dpkg,cache,log}/

# Use the default unprivileged account. This could be considered bad practice
# on systems where multiple processes end up being executed by 'daemon' but
# here we only ever run one process anyway.
ENV RUN_USER            daemon
ENV RUN_GROUP           daemon

# Install Atlassian Stash to the following location
ENV CONFLUENCE_INSTALL_DIR   /opt/atlassian/confluence

ENV CONFLUENCE_VERSION 5.8.15

RUN mkdir -p                             ${CONFLUENCE_INSTALL_DIR} \
    && curl -L --silent                  ${DOWNLOAD_URL}${CONFLUENCE_VERSION}.tar.gz | tar -xz --strip=1 -C "$CONFLUENCE_INSTALL_DIR" \
    && mkdir -p                          ${CONFLUENCE_INSTALL_DIR}/conf/Catalina \
    && chmod -R 700                      ${CONFLUENCE_INSTALL_DIR}/conf/Catalina \
    && chmod -R 700                      ${CONFLUENCE_INSTALL_DIR}/logs          \
    && chmod -R 700                      ${CONFLUENCE_INSTALL_DIR}/temp          \
    && chmod -R 700                      ${CONFLUENCE_INSTALL_DIR}/work          \
    && chown -R ${RUN_USER}:${RUN_GROUP} ${CONFLUENCE_INSTALL_DIR}/logs          \
    && chown -R ${RUN_USER}:${RUN_GROUP} ${CONFLUENCE_INSTALL_DIR}/temp          \
    && chown -R ${RUN_USER}:${RUN_GROUP} ${CONFLUENCE_INSTALL_DIR}/work          \
    && chown -R ${RUN_USER}:${RUN_GROUP} ${CONFLUENCE_INSTALL_DIR}/conf          \
    && cd ${CONFLUENCE_INSTALL_DIR}/confluence/WEB-INF/lib                       \
    && curl -SLO "https://gist.github.com/TommyLau/8a5ce4629d027f7884e6/raw/18fb5f18b5cf7997a37169c0ba4f17e2e38c7c96/atlassian-extras-decoder-v2-3.2.jar" \
    && chown 500.1000 atlassian-extras-decoder-v2-3.2.jar                        \
    && cd ../atlassian-bundled-plugins/                                          \
    && curl -SLO "https://gist.github.com/TommyLau/8a5ce4629d027f7884e6/raw/4d1a3fc95f7d6be947fe4a4b79f4105b817294fe/atlassian-universal-plugin-manager-plugin-2.18.4.jar" \
    && chown 500.1000 atlassian-universal-plugin-manager-plugin-2.18.4.jar       \
    && echo "confluence.home=${CONFLUENCE_HOME}" > ${CONFLUENCE_INSTALL_DIR}/confluence/WEB-INF/classes/confluence-init.properties

USER ${RUN_USER}:${RUN_GROUP}

VOLUME ["${CONFLUENCE_INSTALL_DIR}"]

# HTTP Port
EXPOSE 8090

WORKDIR $CONFLUENCE_INSTALL_DIR

# Run in foreground
CMD ["./bin/start-confluence.sh", "-fg"]
