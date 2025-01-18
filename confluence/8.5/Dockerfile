FROM atlassian/confluence:8.5

MAINTAINER Tommy Lau <tommy.lhg@gmail.com>

RUN set -x \
    && cd ${CONFLUENCE_INSTALL_DIR}/confluence/WEB-INF/lib \
    && rm -f com.atlassian.extras_atlassian-extras-key-manager-3.4.6.jar \
    && curl -SLO "https://gist.githubusercontent.com/TommyLau/8a5ce4629d027f7884e6/raw/atlassian-extras-key-manager-3.4.6.jar" \
    && chown ${RUN_USER}:${RUN_GROUP} atlassian-extras-key-manager-3.4.6.jar

