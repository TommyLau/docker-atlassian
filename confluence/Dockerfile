FROM tommylau/java:1.8

MAINTAINER Tommy Lau <tommy@gen-new.com>

ENV CONFLUENCE_HOME     /var/atlassian/application-data/confluence

# Use the default unprivileged account. This could be considered bad practice
# on systems where multiple processes end up being executed by 'daemon' but
# here we only ever run one process anyway.
ENV RUN_USER            daemon
ENV RUN_GROUP           daemon

# Install Atlassian Confluence to the following location
ENV CONFLUENCE_INSTALL  /opt/atlassian/confluence

ENV CONFLUENCE_VERSION  5.9.9
ENV DOWNLOAD_URL        https://downloads.atlassian.com/software/confluence/downloads/atlassian-confluence-${CONFLUENCE_VERSION}.tar.gz

RUN set -x \
    && mkdir -p                         "${CONFLUENCE_HOME}" \
    && chmod -R 700                     "${CONFLUENCE_HOME}" \
    && chown ${RUN_USER}:${RUN_GROUP}   "${CONFLUENCE_HOME}" \
    && mkdir -p                         "${CONFLUENCE_INSTALL}" \
    && curl -L --silent                 "${DOWNLOAD_URL}" | tar -xz --strip=1 -C "$CONFLUENCE_INSTALL" \
    && mkdir -p                         "${CONFLUENCE_INSTALL}/conf/Catalina" \
    && chmod -R 700                     "${CONFLUENCE_INSTALL}/conf/Catalina" \
    && chmod -R 700                     "${CONFLUENCE_INSTALL}/logs" \
    && chmod -R 700                     "${CONFLUENCE_INSTALL}/temp" \
    && chmod -R 700                     "${CONFLUENCE_INSTALL}/work" \
    && cd ${CONFLUENCE_INSTALL}/confluence/WEB-INF/lib \
    && curl -SLO "https://gist.github.com/TommyLau/8a5ce4629d027f7884e6/raw/18fb5f18b5cf7997a37169c0ba4f17e2e38c7c96/atlassian-extras-decoder-v2-3.2.jar" \
    && chown 500.500 atlassian-extras-decoder-v2-3.2.jar \
    && cd ../atlassian-bundled-plugins/ \
    && curl -SLO "https://gist.github.com/TommyLau/8a5ce4629d027f7884e6/raw/9bc3df0e1134c0a290665bdbec041a847a903cef/atlassian-universal-plugin-manager-plugin-2.20.jar" \
    && chown 500.500 atlassian-universal-plugin-manager-plugin-2.20.jar          \
    && chown -R ${RUN_USER}:${RUN_GROUP} ${CONFLUENCE_INSTALL} \
    && echo "confluence.home=${CONFLUENCE_HOME}" > ${CONFLUENCE_INSTALL}/confluence/WEB-INF/classes/confluence-init.properties

USER ${RUN_USER}:${RUN_GROUP}

VOLUME ["${CONFLUENCE_INSTALL}", "${CONFLUENCE_HOME}"]

# HTTP Port
EXPOSE 8090

WORKDIR ${CONFLUENCE_INSTALL}

# Run in foreground
CMD ["./bin/start-confluence.sh", "-fg"]
