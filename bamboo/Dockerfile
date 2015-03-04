FROM java:openjdk-7-jre

MAINTAINER Tommy Lau <tommy@gen-new.com>

ENV BAMBOO_VERSION 5.7.2

ENV DOWNLOAD_URL        https://www.atlassian.com/software/bamboo/downloads/binary/atlassian-bamboo-

ENV BAMBOO_HOME          /var/atlassian/application-data/bamboo

# Install Atlassian Stash to the following location
ENV BAMBOO_INSTALL_DIR   /opt/atlassian/bamboo



# Use the default unprivileged account. This could be considered bad practice
# on systems where multiple processes end up being executed by 'daemon' but
# here we only ever run one process anyway.
ENV RUN_USER            daemon
ENV RUN_GROUP           daemon


# Install git, download and extract Stash and create the required directory layout.
# Try to limit the number of RUN instructions to minimise the number of layers that will need to be created.
RUN apt-get update -qq                                                            \
    && apt-get install -y --no-install-recommends                                 \
            zip                                                                   \
    && apt-get clean autoclean                                                    \
    && apt-get autoremove --yes                                                   \
    && rm -rf                  /var/lib/{apt,dpkg,cache,log}/

RUN mkdir -p                             $BAMBOO_INSTALL_DIR


RUN curl -L --silent                     ${DOWNLOAD_URL}${BAMBOO_VERSION}.tar.gz | tar -xz --strip=1 -C "$BAMBOO_INSTALL_DIR" \
    && mkdir -p                          ${BAMBOO_INSTALL_DIR}/conf/Catalina      \
    && chmod -R 700                      ${BAMBOO_INSTALL_DIR}/conf/Catalina      \
    && chmod -R 700                      ${BAMBOO_INSTALL_DIR}/logs               \
    && chmod -R 700                      ${BAMBOO_INSTALL_DIR}/temp               \
    && chmod -R 700                      ${BAMBOO_INSTALL_DIR}/work               \
    && chown -R ${RUN_USER}:${RUN_GROUP} ${BAMBOO_INSTALL_DIR}/logs               \
    && chown -R ${RUN_USER}:${RUN_GROUP} ${BAMBOO_INSTALL_DIR}/temp               \
    && chown -R ${RUN_USER}:${RUN_GROUP} ${BAMBOO_INSTALL_DIR}/work               \
    && chown -R ${RUN_USER}:${RUN_GROUP} ${BAMBOO_INSTALL_DIR}/conf               \
    && cd ${BAMBOO_INSTALL_DIR}/atlassian-bamboo/WEB-INF/lib                      \
    && curl -SLO "https://gist.github.com/TommyLau/8a5ce4629d027f7884e6/raw/806158e4fed98d734409894f724af67c5f2ee418/atlassian-extras-2.4.jar" \
    && chown 500.1000 atlassian-extras-2.4.jar                                    \
    && cd ../classes/                                                             \
    && curl -SLO "https://gist.github.com/TommyLau/8a5ce4629d027f7884e6/raw/a382eb800b33d509a0ef4db9508956c8ea89fc96/atlassian-universal-plugin-manager-plugin-2.16.2.jar" \
    && zip -u9 atlassian-bundled-plugins.zip atlassian-universal-plugin-manager-plugin-2.16.2.jar \
    && rm -fr atlassian-universal-plugin-manager-plugin-2.16.2.jar                \
    && chown 500.1000 atlassian-bundled-plugins.zip                               \
    && echo "bamboo.home=${BAMBOO_HOME}" >> ${BAMBOO_INSTALL_DIR}/atlassian-bamboo/WEB-INF/classes/bamboo-init.properties

USER ${RUN_USER}:${RUN_GROUP}

VOLUME ["${BAMBOO_INSTALL_DIR}"]

# HTTP Port
EXPOSE 8085

WORKDIR $BAMBOO_INSTALL_DIR

# Run in foreground
CMD ["./bin/start-bamboo.sh", "-fg"]
