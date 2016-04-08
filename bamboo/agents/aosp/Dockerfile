FROM atlassian/bamboo-base-agent

MAINTAINER Tommy Lau <tommy@gen-new.com>

# Install needed packages for building AOSP
RUN apt-get update && apt-get install -y software-properties-common --no-install-recommends \
	&& echo oracle-java6-installer shared/accepted-oracle-license-v1-1 select true | debconf-set-selections \
	&& echo oracle-java8-installer shared/accepted-oracle-license-v1-1 select true | debconf-set-selections \
	&& apt-add-repository -y ppa:webupd8team/java \
	&& apt-get update && apt-get install -y \
		bison \
		build-essential \
		flex \
		git \
		gperf \
		g++-multilib \
#		lib32stdc++6 \
		lib32z1-dev \
		libxml2-utils \
		oracle-java6-installer \
		oracle-java8-installer \
		python-networkx \
		ssh-client \
		unzip \
		zip \
		--no-install-recommends \
	&& apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

# Use bash shell instead of dash
RUN echo "dash dash/sh boolean false" | debconf-set-selections && DEBIAN_FRONTEND=noninteractive dpkg-reconfigure dash

ENV LANG C.UTF-8

