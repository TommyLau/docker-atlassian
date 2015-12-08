FROM atlassian/bamboo-base-agent

MAINTAINER Tommy Lau <tommy@gen-new.com>

# Install needed packages for building AOSP
RUN apt-get update && apt-get install -y software-properties-common --no-install-recommends \
	&& echo oracle-java6-installer shared/accepted-oracle-license-v1-1 select true | debconf-set-selections \
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
		python-networkx \
		ssh-client \
		unzip \
		zip \
		--no-install-recommends \
	&& apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

# All builds will be done by user aosp
#RUN useradd --create-home aosp

# The persistent data will be in these two directories, everything else is
# considered to be ephemeral
#VOLUME ["/tmp/ccache", "/aosp"]

# Improve rebuild performance by enabling compiler cache
#ENV USE_CCACHE 1
#ENV CCACHE_DIR /tmp/ccache

# Work in the build directory, repo is expected to be init'd here
#USER aosp
#WORKDIR /aosp
