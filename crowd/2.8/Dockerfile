FROM java:openjdk-7-jdk

MAINTAINER Tommy Lau <tommy@gen-new.com>

ENV DOWNLOAD_URL        https://www.atlassian.com/software/crowd/downloads/binary/atlassian-crowd-

ENV CROWD_HOME          /var/atlassian/application-data/crowd


# Use the default unprivileged account. This could be considered bad practice
# on systems where multiple processes end up being executed by 'daemon' but
# here we only ever run one process anyway.
ENV RUN_USER            daemon
ENV RUN_GROUP           daemon

# Install Atlassian Crowd to the following location
ENV CROWD_INSTALL_DIR   /opt/atlassian/crowd

ENV CROWD_VERSION 2.8.4

RUN mkdir -p                             ${CROWD_INSTALL_DIR} \
    && curl -L --silent                  ${DOWNLOAD_URL}${CROWD_VERSION}.tar.gz | tar -xz --strip=1 -C "$CROWD_INSTALL_DIR" \
    && chmod -R 700                      ${CROWD_INSTALL_DIR}/apache-tomcat/logs  \
    && chmod -R 700                      ${CROWD_INSTALL_DIR}/apache-tomcat/temp  \
    && chmod -R 700                      ${CROWD_INSTALL_DIR}/apache-tomcat/work  \
    && chmod -R 700                      ${CROWD_INSTALL_DIR}/apache-tomcat/conf  \
    && cd ${CROWD_INSTALL_DIR}/crowd-webapp/WEB-INF/lib                           \
    && curl -SLO "https://gist.github.com/TommyLau/8a5ce4629d027f7884e6/raw/2c5a9b2a26fa0da8b78938c5da1ad57dc05ea1b0/atlassian-extras-3.2.jar" \
    && chown -R ${RUN_USER}:${RUN_GROUP} ${CROWD_INSTALL_DIR}                     \
    && echo "crowd.home=${CROWD_HOME}" >> ${CROWD_INSTALL_DIR}/crowd-webapp/WEB-INF/classes/crowd-init.properties

USER ${RUN_USER}:${RUN_GROUP}

VOLUME ["${CROWD_INSTALL_DIR}"]

# HTTP Port
EXPOSE 8095

WORKDIR $CROWD_INSTALL_DIR

# Run in foreground
CMD ["./apache-tomcat/bin/catalina.sh", "run"]
