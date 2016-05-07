FROM ubuntu:14.04

MAINTAINER Tommy Lau <tommy@gen-new.com>

# Download and extract JIRA and create the required directory layout.
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

ENV JIRA_HOME           /var/atlassian/application-data/jira

# Install Atlassian JIRA to the following location
ENV JIRA_INSTALL_DIR   /opt/atlassian/jira

ENV JIRA_VERSION 7.1.6
ENV DOWNLOAD_URL        https://downloads.atlassian.com/software/jira/downloads/atlassian-jira-software-${JIRA_VERSION}-jira-${JIRA_VERSION}.tar.gz

RUN mkdir -p                             ${JIRA_INSTALL_DIR} \
    && curl -L --silent                  ${DOWNLOAD_URL} | tar -xz --strip=1 -C "$JIRA_INSTALL_DIR" \
    && mkdir -p                          ${JIRA_INSTALL_DIR}/conf/Catalina      \
    && chmod -R 700                      ${JIRA_INSTALL_DIR}/conf/Catalina      \
    && chmod -R 700                      ${JIRA_INSTALL_DIR}/logs               \
    && chmod -R 700                      ${JIRA_INSTALL_DIR}/temp               \
    && chmod -R 700                      ${JIRA_INSTALL_DIR}/work               \
    && chown -R ${RUN_USER}:${RUN_GROUP} ${JIRA_INSTALL_DIR}/                   \
    && cd ${JIRA_INSTALL_DIR}/atlassian-jira/WEB-INF/lib                        \
    && curl -SLO "https://gist.github.com/TommyLau/8a5ce4629d027f7884e6/raw/ea2b58dcbf1ca18508a1b99d847c11f1ccb692a2/atlassian-extras-3.1.2.jar" \
    && chown 500.500 atlassian-extras-3.1.2.jar                                 \
    && cd ../atlassian-bundled-plugins/                                         \
    && curl -SLO "https://gist.github.com/TommyLau/8a5ce4629d027f7884e6/raw/f9597f68f2d244022a12551660394088922c04d1/atlassian-universal-plugin-manager-plugin-2.20.6.jar" \
    && chown 500.500 atlassian-universal-plugin-manager-plugin-2.20.6.jar

USER ${RUN_USER}:${RUN_GROUP}

VOLUME ["${JIRA_HOME}"]

# HTTP Port
EXPOSE 8080

WORKDIR $JIRA_INSTALL_DIR

# Run in foreground
CMD ["./bin/start-jira.sh", "-fg"]
