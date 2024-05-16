FROM tommylau/java:1.8

MAINTAINER Tommy Lau <tommy.lhg@gmail.com>

# Setup useful environment variables
ENV JIRA_HOME		/var/atlassian/application-data/jira
ENV JIRA_INSTALL	/opt/atlassian/jira
ENV JIRA_VERSION	9.12.8
ENV DOWNLOAD_URL	https://www.atlassian.com/software/jira/downloads/binary/atlassian-jira-software-${JIRA_VERSION}.tar.gz

LABEL Description="This image is used to start Atlassian JIRA" Vendor="Tommy Lau" Version="${JIRA_VERSION}"

# Use the default unprivileged account. This could be considered bad practice
# on systems where multiple processes end up being executed by 'daemon' but
# here we only ever run one process anyway.
ENV RUN_USER            daemon
ENV RUN_GROUP           daemon

# Install Atlassian JIRA to the following location

RUN set -x \
    && mkdir -p                         "${JIRA_HOME}" \
    && chmod -R 700                     "${JIRA_HOME}" \
    && chown ${RUN_USER}:${RUN_GROUP}   "${JIRA_HOME}" \
    && mkdir -p                         "${JIRA_INSTALL}/conf" \
    && curl -Ls                         "${DOWNLOAD_URL}" | tar -xz --strip=1 -C "$JIRA_INSTALL" \
    && chmod -R 700                     "${JIRA_INSTALL}/conf" \
    && chmod -R 700                     "${JIRA_INSTALL}/logs" \
    && chmod -R 700                     "${JIRA_INSTALL}/temp" \
    && chmod -R 700                     "${JIRA_INSTALL}/work" \
    && cd ${JIRA_INSTALL}/atlassian-jira/WEB-INF/lib \
    && curl -SLO "https://gist.githubusercontent.com/TommyLau/8a5ce4629d027f7884e6/raw/atlassian-extras-key-manager-3.4.6.jar" \
    && chown -R ${RUN_USER}:${RUN_GROUP} ${JIRA_INSTALL}

# Use the default unprivileged account. This could be considered bad practice
# on systems where multiple processes end up being executed by 'daemon' but
# here we only ever run one process anyway.
USER ${RUN_USER}:${RUN_GROUP}

# Expose default HTTP connector port.
EXPOSE 8080

# Set volume mount points for installation and home directory. Changes to the
# home directory needs to be persisted as well as parts of the installation
# directory due to eg. logs.
VOLUME ["${JIRA_INSTALL}", "${JIRA_HOME}"]

# Set the default working directory as the JIRA installation directory.
WORKDIR $JIRA_INSTALL

# Run in foreground
CMD ["./bin/start-jira.sh", "-fg"]
