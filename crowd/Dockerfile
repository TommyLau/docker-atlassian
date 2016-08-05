FROM tommylau/java:1.8

MAINTAINER Tommy Lau <tommy@gen-new.com>

ENV DOWNLOAD_URL        https://www.atlassian.com/software/crowd/downloads/binary/atlassian-crowd-

ENV CROWD_HOME          /var/atlassian/application-data/crowd

# Use the default unprivileged account. This could be considered bad practice
# on systems where multiple processes end up being executed by 'daemon' but
# here we only ever run one process anyway.
ENV RUN_USER            daemon
ENV RUN_GROUP           daemon

# Install Atlassian Crowd to the following location
ENV CROWD_INSTALL       /opt/atlassian/crowd

ENV CROWD_VERSION 2.9.1

RUN set -x \
    && mkdir -p                           "${CROWD_HOME}" \
    && chmod -R 700                       "${CROWD_HOME}" \
    && chown ${RUN_USER}:${RUN_GROUP}     "${CROWD_HOME}" \
    && mkdir -p                           "${CROWD_INSTALL}" \
    && curl -L --silent                   "${DOWNLOAD_URL}${CROWD_VERSION}.tar.gz" | tar -xz --strip=1 -C "$CROWD_INSTALL" \
    && chmod -R 700                       "${CROWD_INSTALL}/apache-tomcat/logs" \
    && chmod -R 700                       "${CROWD_INSTALL}/apache-tomcat/temp" \
    && chmod -R 700                       "${CROWD_INSTALL}/apache-tomcat/work" \
    && chmod -R 700                       "${CROWD_INSTALL}/apache-tomcat/conf" \
    && cd ${CROWD_INSTALL}/crowd-webapp/WEB-INF/lib \
    && curl -SLO "https://gist.github.com/TommyLau/8a5ce4629d027f7884e6/raw/2c5a9b2a26fa0da8b78938c5da1ad57dc05ea1b0/atlassian-extras-3.2.jar" \
    && chown -R ${RUN_USER}:${RUN_GROUP} ${CROWD_INSTALL} \
    && echo "crowd.home=${CROWD_HOME}" >> ${CROWD_INSTALL}/crowd-webapp/WEB-INF/classes/crowd-init.properties

USER ${RUN_USER}:${RUN_GROUP}

VOLUME ["${CROWD_INSTALL}", "${CROWD_HOME}"]

# HTTP Port
EXPOSE 8095

WORKDIR ${CROWD_INSTALL}

# Run in foreground
CMD ["./apache-tomcat/bin/catalina.sh", "run"]
