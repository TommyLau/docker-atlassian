FROM atlassian/bitbucket:8.19

MAINTAINER Tommy Lau <tommy.lhg@gmail.com>

RUN set -x \
    && cd ${BITBUCKET_INSTALL_DIR}/app/WEB-INF/lib \
    && curl -SLO "https://gist.githubusercontent.com/TommyLau/8a5ce4629d027f7884e6/raw/atlassian-extras-key-manager-3.4.6.jar" \
    && chown ${RUN_USER}:${RUN_GROUP} atlassian-extras-key-manager-3.4.6.jar

