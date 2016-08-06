FROM tommylau/java:1.8

MAINTAINER Tommy Lau <tommy@gen-new.com>

# Setup useful environment variables
ENV BITBUCKET_HOME      /var/atlassian/application-data/bitbucket
ENV BITBUCKET_INSTALL   /opt/atlassian/bitbucket
ENV BITBUCKET_VERSION   4.8.3
ENV DOWNLOAD_URL        https://downloads.atlassian.com/software/stash/downloads/atlassian-bitbucket-${BITBUCKET_VERSION}.tar.gz

LABEL Description="This image is used to start Atlassian Bitbucket Server" Vendor="Tommy Lau" Version="${BITBUCKET_VERSION}"

# Use the default unprivileged account. This could be considered bad practice
# on systems where multiple processes end up being executed by 'daemon' but
# here we only ever run one process anyway.
ENV RUN_USER            daemon
ENV RUN_GROUP           daemon

# Install Atlassian Bitbucket Server to the following location
RUN set -x \
    && mkdir -p                         "${BITBUCKET_HOME}" \
    && chmod -R 700                     "${BITBUCKET_HOME}" \
    && chown ${RUN_USER}:${RUN_GROUP}   "${BITBUCKET_HOME}" \
    && mkdir -p                         "${BITBUCKET_INSTALL}/conf" \
    && curl -Ls                         "${DOWNLOAD_URL}" | tar -xz --strip=1 -C "$BITBUCKET_INSTALL" \
    && chmod -R 700                     "${BITBUCKET_INSTALL}/conf" \
    && chmod -R 700                     "${BITBUCKET_INSTALL}/logs" \
    && chmod -R 700                     "${BITBUCKET_INSTALL}/temp" \
    && chmod -R 700                     "${BITBUCKET_INSTALL}/work" \
    && cd ${BITBUCKET_INSTALL}/atlassian-bitbucket/WEB-INF/lib \
    && curl -SLO "https://gist.github.com/TommyLau/8a5ce4629d027f7884e6/raw/7ae5d32c6f77a39746597d46a511768e5a401b47/atlassian-extras-decoder-v2-3.3.0.jar" \
    && cd ../atlassian-bundled-plugins/ \
    && curl -SLO "https://gist.github.com/TommyLau/8a5ce4629d027f7884e6/raw/9217bf3a8ce8f1f04f105e606cf5c30e267b41a7/atlassian-universal-plugin-manager-plugin-2.21.3.jar" \
    && chown -R ${RUN_USER}:${RUN_GROUP} ${BITBUCKET_INSTALL}

# Use the default unprivileged account. This could be considered bad practice
# on systems where multiple processes end up being executed by 'daemon' but
# here we only ever run one process anyway.
USER ${RUN_USER}:${RUN_GROUP}

# Expose default HTTP connector port.
EXPOSE 7990

# SSH Port
EXPOSE 7999

# Set volume mount points for installation and home directory. Changes to the
# home directory needs to be persisted as well as parts of the installation
# directory due to eg. logs.
VOLUME ["${BITBUCKET_INSTALL}", "${BITBUCKET_HOME}"]

# Set the default working directory as the Confluence installation directory.
WORKDIR ${BITBUCKET_INSTALL}

# Run in foreground
CMD ["./bin/start-bitbucket.sh", "-fg"]

