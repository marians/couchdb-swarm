# Taking some inspiration from
# https://github.com/tutumcloud/tutum-docker-couchdb (licensed Apache 2.0)

FROM debian:wheezy

MAINTAINER Marian Steinbach <marian@giantswarm.io>


ENV DEBIAN_FRONTEND noninteractive

#install CouchDB
RUN apt-get update -q && \
    apt-get install -q -y --no-install-recommends \
    	curl \
    	pwgen \
    	build-essential \
		erlang-base-hipe \
		erlang-dev \
		erlang-manpages \
		erlang-eunit \
		erlang-nox \
		libicu-dev \
		libmozjs-dev \
		libcurl4-openssl-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Build SpiderMonkey rom source
RUN curl -O http://ftp.mozilla.org/pub/mozilla.org/js/js-1.8.0-rc1.tar.gz \
	&& tar xzf js-1.8.0-rc1.tar.gz \
	&& cd js/src \
	&& make BUILD_OPT=1 -f Makefile.ref \
	&& make BUILD_OPT=1 JS_DIST=/usr/local -f Makefile.ref export

# Build couchdb from source
RUN curl -O http://apache.openmirror.de/couchdb/source/1.6.1/apache-couchdb-1.6.1.tar.gz \
	&& tar xzf apache-couchdb-1.6.1.tar.gz \
	&& cd apache-couchdb-1.6.1 \
	&& ./configure --prefix=/usr/local --with-js-lib=/usr/local/lib --with-js-include=/usr/local/include \
	&& make \
	&& make install

VOLUME /usr/local/var/lib/couchdb

# Make CouchDB listen on all addresses
RUN sed -i -r 's/;bind_address = 127.0.0.1/bind_address = 0.0.0.0/' /usr/local/etc/couchdb/local.ini

ADD run.sh /run.sh
RUN chmod 755 /*.sh

EXPOSE 5984

ENTRYPOINT ["/run.sh"]
