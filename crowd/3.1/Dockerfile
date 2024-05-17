FROM openjdk:8-jdk-alpine

MAINTAINER Tommy Lau <tommy@gen-new.com>

# Setup useful environment variables
ENV CROWD_HOME		/var/atlassian/application-data/crowd
ENV CROWD_INSTALL	/opt/atlassian/crowd
ENV CROWD_VERSION	3.1.2
ENV DOWNLOAD_URL	https://www.atlassian.com/software/crowd/downloads/binary/atlassian-crowd-${CROWD_VERSION}.tar.gz

LABEL Description="This image is used to start Atlassian Crowd" Vendor="Tommy Lau" Version="${CROWD_VERSION}"

# Use the default unprivileged account. This could be considered bad practice
# on systems where multiple processes end up being executed by 'daemon' but
# here we only ever run one process anyway.
ENV RUN_USER            daemon
ENV RUN_GROUP           daemon

# Install Atlassian Crowd to the following location
RUN set -x \
    && apk add --update ca-certificates curl tar tomcat-native \
    && rm -rf /var/lib/{apt,dpkg,cache,log}/ /tmp/* /var/tmp/* \
    && mkdir -p                           "${CROWD_HOME}" \
    && chmod -R 700                       "${CROWD_HOME}" \
    && chown ${RUN_USER}:${RUN_GROUP}     "${CROWD_HOME}" \
    && mkdir -p                           "${CROWD_INSTALL}" \
    && curl -L --silent                   "${DOWNLOAD_URL}" | tar -xz --strip=1 -C "$CROWD_INSTALL" \
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

# Set volume mount points for installation and home directory. Changes to the
# home directory needs to be persisted as well as parts of the installation
# directory due to eg. logs.
VOLUME ["${CROWD_INSTALL}", "${CROWD_HOME}"]

# Set the default working directory as the Crowd installation directory.
WORKDIR ${CROWD_INSTALL}

# Run in foreground
CMD ["./apache-tomcat/bin/catalina.sh", "run"]
