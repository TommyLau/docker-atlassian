FROM tommylau/java:1.8

MAINTAINER Tommy Lau <tommy@gen-new.com>

# Setup useful environment variables
# FISHEYE_HOME equals to FISHEYE_INSTALL path, but not store path compared to other Atlassian products, weird... >_<
# ENV FISHEYE_HOME        /var/atlassian/application-data/fisheye
# FISHEYE_INST equals to FISHEYE_HOME compared to other Atlassian products.
ENV FISHEYE_INST        /var/atlassian/application-data/fisheye
ENV FISHEYE_INSTALL     /opt/atlassian/fisheye
ENV FISHEYE_VERSION     4.3.1
ENV DOWNLOAD_URL        https://www.atlassian.com/software/fisheye/downloads/binary/fisheye-${FISHEYE_VERSION}.zip

LABEL Description="This image is used to start Atlassian FishEye" Vendor="Tommy Lau" Version="${FISHEYE_VERSION}"

# Install git, download and extract Stash and create the required directory layout.
# Try to limit the number of RUN instructions to minimise the number of layers that will need to be created.

# Use the default unprivileged account. This could be considered bad practice
# on systems where multiple processes end up being executed by 'daemon' but
# here we only ever run one process anyway.
ENV RUN_USER            daemon
ENV RUN_GROUP           daemon

# Install Atlassian FishEye and helper tools and setup initial home
# directory structure.
RUN set -x \
    && apt-get update -qq \
    && apt-get install -y --no-install-recommends git ssh-client unzip zip \
    && mkdir -p                         "${FISHEYE_INST}" \
    && chmod -R 700                     "${FISHEYE_INST}" \
    && chown ${RUN_USER}:${RUN_GROUP}   "${FISHEYE_INST}" \
    && mkdir -p                         "${FISHEYE_INSTALL}" \
    && cd ${FISHEYE_INSTALL} \
    && curl -SLO                        "${DOWNLOAD_URL}" \
    && unzip -q fisheye-*.zip \
    && rm fisheye-*.zip \
    && mv fecru-*/* . \
    && rm -fr fecru-* \
    && cd ${FISHEYE_INSTALL}/lib \
    && curl -SLO "https://gist.github.com/TommyLau/8a5ce4629d027f7884e6/raw/37ac5fb1f1d1f780d7c28c7ff24aca77515ee9af/atlassian-extras-2.5.jar" \
    && cd ../plugins/ \
    && curl -SLO "https://gist.github.com/TommyLau/8a5ce4629d027f7884e6/raw/37ac5fb1f1d1f780d7c28c7ff24aca77515ee9af/atlassian-universal-plugin-manager-plugin-2.20.5.jar" \
    && zip -u9 bundled-plugins.zip atlassian-universal-plugin-manager-plugin-2.20.5.jar \
    && rm -fr atlassian-universal-plugin-manager-plugin-2.20.5.jar \
    && chown -R ${RUN_USER}:${RUN_GROUP} ${FISHEYE_INSTALL} \
    && apt-get remove -y unzip zip \
    && apt-get clean autoclean \
    && apt-get autoremove --yes \
    && rm -rf /var/lib/{apt,dpkg,cache,log}

# Use the default unprivileged account. This could be considered bad practice
# on systems where multiple processes end up being executed by 'daemon' but
# here we only ever run one process anyway.
USER ${RUN_USER}:${RUN_GROUP}

# Expose default HTTP connector port.
EXPOSE 8060

# Set volume mount points for installation and home directory. Changes to the
# home directory needs to be persisted as well as parts of the installation
# directory due to eg. logs.
VOLUME ["${FISHEYE_INSTALL}", "${FISHEYE_INST}"]

# Set the default working directory as the FISHEYE installation directory.
WORKDIR ${FISHEYE_INSTALL}

# Run in foreground
CMD ["./bin/run.sh"]
