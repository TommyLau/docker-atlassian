FROM openjdk:8-jdk-alpine

MAINTAINER Tommy Lau <tommy@gen-new.com>

# Setup useful environment variables
ENV BAMBOO_HOME         /var/atlassian/application-data/bamboo
ENV BAMBOO_INSTALL      /opt/atlassian/bamboo
ENV BAMBOO_VERSION      6.4.1
ENV DOWNLOAD_URL        https://www.atlassian.com/software/bamboo/downloads/binary/atlassian-bamboo-${BAMBOO_VERSION}.tar.gz

LABEL Description="This image is used to start Atlassian Bamboo" Vendor="Tommy Lau" Version="${BAMBOO_VERSION}"

# Use the default unprivileged account. This could be considered bad practice
# on systems where multiple processes end up being executed by 'daemon' but
# here we only ever run one process anyway.
ENV RUN_USER            daemon
ENV RUN_GROUP           daemon

# Install Atlassian Bamboo to the following location
RUN set -x \
    && apk add --update ca-certificates bash curl git git-daemon openssh openssl procps perl tar tini tomcat-native ttf-dejavu \
    && rm -rf /var/lib/{apt,dpkg,cache,log}/ /tmp/* /var/tmp/* \
    && mkdir -p                         "${BAMBOO_HOME}" \
    && chmod -R 700                     "${BAMBOO_HOME}" \
    && chown ${RUN_USER}:${RUN_GROUP}   "${BAMBOO_HOME}" \
    && mkdir -p                         "${BAMBOO_INSTALL}/conf" \
    && curl -Ls                         "${DOWNLOAD_URL}" | tar -xz --strip=1 -C "$BAMBOO_INSTALL" \
    && chmod -R 700                     "${BAMBOO_INSTALL}/conf" \
    && chmod -R 700                     "${BAMBOO_INSTALL}/logs" \
    && chmod -R 700                     "${BAMBOO_INSTALL}/temp" \
    && chmod -R 700                     "${BAMBOO_INSTALL}/work" \
    && cd ${BAMBOO_INSTALL}/atlassian-bamboo/WEB-INF/lib \
    && curl -SLO "https://gist.github.com/TommyLau/8a5ce4629d027f7884e6/raw/9bc3df0e1134c0a290665bdbec041a847a903cef/atlassian-extras-decoder-v2-3.3.0.jar" \
    && cd ../atlassian-bundled-plugins/ \
    && curl -SLO "https://gist.github.com/TommyLau/8a5ce4629d027f7884e6/raw/7e4daacc1aabc4ff5a1a46112a4d273434951118/atlassian-universal-plugin-manager-plugin-2.22.6.jar" \
    && chown -R ${RUN_USER}:${RUN_GROUP} ${BAMBOO_INSTALL} \
    && echo "bamboo.home=${BAMBOO_HOME}" > ${BAMBOO_INSTALL}/atlassian-bamboo/WEB-INF/classes/bamboo-init.properties \
    && mv ${BAMBOO_INSTALL}/atlassian-bamboo/WEB-INF/lib/javax.mail-*.jar ${BAMBOO_INSTALL}/lib

# Use the default unprivileged account. This could be considered bad practice
# on systems where multiple processes end up being executed by 'daemon' but
# here we only ever run one process anyway.
USER ${RUN_USER}:${RUN_GROUP}

# Expose default HTTP connector port.
EXPOSE 8085

# Agent Port
EXPOSE 54663

# Set volume mount points for installation and home directory. Changes to the
# home directory needs to be persisted as well as parts of the installation
# directory due to eg. logs.
VOLUME ["${BAMBOO_INSTALL}", "${BAMBOO_HOME}"]

# Set the default working directory as the Bamboo installation directory.
WORKDIR ${BAMBOO_INSTALL}

# Run in foreground
CMD ["./bin/start-bamboo.sh", "-fg"]
