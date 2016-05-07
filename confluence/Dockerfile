FROM ubuntu:14.04

MAINTAINER Tommy Lau <tommy@gen-new.com>

# Download and extract Confluence and create the required directory layout.
# Try to limit the number of RUN instructions to minimise the number of layers that will need to be created.
RUN apt-get update -qq \
    && apt-get install -y --no-install-recommends curl software-properties-common \
    && apt-get install -y --no-install-recommends fonts-dejavu fonts-wqy-* fonts-arphic-uming \
    && echo oracle-java8-installer shared/accepted-oracle-license-v1-1 select true | debconf-set-selections \
    && apt-add-repository -y ppa:webupd8team/java \
    && apt-get update -qq \
    && apt-get install -y --no-install-recommends oracle-java8-installer \
    && apt-get clean autoclean \
    && apt-get autoremove --yes \
    && rm -rf /var/lib/{apt,dpkg,cache,log}/ \
    && cd /usr/lib/jvm/java-8-oracle/jre/lib \
    && cp fontconfig.Ubuntu.properties fontconfig.properties \
    && sed -i 's/ttf-dejavu/dejavu/g' fontconfig.properties

# Use the default unprivileged account. This could be considered bad practice
# on systems where multiple processes end up being executed by 'daemon' but
# here we only ever run one process anyway.
ENV RUN_USER            daemon
ENV RUN_GROUP           daemon

ENV CONFLUENCE_HOME     /var/atlassian/application-data/confluence

# Install Atlassian Confluence to the following location
ENV CONFLUENCE_INSTALL_DIR   /opt/atlassian/confluence

ENV CONFLUENCE_VERSION 5.9.9
ENV DOWNLOAD_URL        https://downloads.atlassian.com/software/confluence/downloads/atlassian-confluence-${CONFLUENCE_VERSION}.tar.gz

RUN mkdir -p                             ${CONFLUENCE_INSTALL_DIR} \
    && curl -L --silent                  ${DOWNLOAD_URL} | tar -xz --strip=1 -C "$CONFLUENCE_INSTALL_DIR" \
    && mkdir -p                          ${CONFLUENCE_INSTALL_DIR}/conf/Catalina \
    && chmod -R 700                      ${CONFLUENCE_INSTALL_DIR}/conf/Catalina \
    && chmod -R 700                      ${CONFLUENCE_INSTALL_DIR}/logs          \
    && chmod -R 700                      ${CONFLUENCE_INSTALL_DIR}/temp          \
    && chmod -R 700                      ${CONFLUENCE_INSTALL_DIR}/work          \
    && chown -R ${RUN_USER}:${RUN_GROUP} ${CONFLUENCE_INSTALL_DIR}/              \
    && cd ${CONFLUENCE_INSTALL_DIR}/confluence/WEB-INF/lib                       \
    && curl -SLO "https://gist.github.com/TommyLau/8a5ce4629d027f7884e6/raw/18fb5f18b5cf7997a37169c0ba4f17e2e38c7c96/atlassian-extras-decoder-v2-3.2.jar" \
    && chown 500.500 atlassian-extras-decoder-v2-3.2.jar                         \
    && cd ../atlassian-bundled-plugins/                                          \
    && curl -SLO "https://gist.github.com/TommyLau/8a5ce4629d027f7884e6/raw/9bc3df0e1134c0a290665bdbec041a847a903cef/atlassian-universal-plugin-manager-plugin-2.20.jar" \
    && chown 500.500 atlassian-universal-plugin-manager-plugin-2.20.jar          \
    && echo "confluence.home=${CONFLUENCE_HOME}" > ${CONFLUENCE_INSTALL_DIR}/confluence/WEB-INF/classes/confluence-init.properties

USER ${RUN_USER}:${RUN_GROUP}

VOLUME ["${CONFLUENCE_HOME}"]

# HTTP Port
EXPOSE 8090

WORKDIR $CONFLUENCE_INSTALL_DIR

# Run in foreground
CMD ["./bin/start-confluence.sh", "-fg"]
