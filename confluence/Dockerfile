FROM atlassian/confluence:10.2.3

LABEL maintainer="Tommy Lau <tommy.lhg@gmail.com>"

RUN set -x \
    && cd ${CONFLUENCE_INSTALL_DIR}/confluence/WEB-INF/lib \
    && curl -SLo com.atlassian.extras.atlassian-extras-key-manager-3.4.6.jar "https://gist.githubusercontent.com/TommyLau/8a5ce4629d027f7884e6/raw/atlassian-extras-key-manager-3.4.6.jar" \
    && chown ${RUN_USER}:${RUN_GROUP} com.atlassian.extras.atlassian-extras-key-manager-3.4.6.jar
