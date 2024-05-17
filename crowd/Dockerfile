FROM atlassian/crowd:5.3

MAINTAINER Tommy Lau <tommy.lhg@gmail.com>

RUN set -x \
    && cd ${CROWD_INSTALL_DIR}/crowd-webapp/WEB-INF/lib \
    && curl -SLO "https://gist.githubusercontent.com/TommyLau/8a5ce4629d027f7884e6/raw/atlassian-extras-key-manager-3.4.6.jar" \
    && chown ${RUN_USER}:${RUN_GROUP} atlassian-extras-key-manager-3.4.6.jar

