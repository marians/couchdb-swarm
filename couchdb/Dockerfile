# Taking some inspiration from
# https://github.com/tutumcloud/tutum-docker-couchdb (licensed Apache 2.0)

FROM debian:wheezy

ENV DEBIAN_FRONTEND noninteractive
ENV COUCHDB_VERSION 1.6.1

# install base packages
RUN set -x && \
    apt-get update -qq && \
    apt-get install -qq -y --no-install-recommends \
        curl \
        pwgen \
        build-essential \
        erlang-base-hipe \
        erlang-dev \
        erlang-manpages \
        erlang-eunit \
        erlang-nox \
        libicu-dev \
        libmozjs185-dev \
        libcurl4-openssl-dev \
        python \
        zip \
    && cd / \
    # Build couchdb from source
    && curl -O http://apache.openmirror.de/couchdb/source/$COUCHDB_VERSION/apache-couchdb-$COUCHDB_VERSION.tar.gz \
    && tar xzf apache-couchdb-$COUCHDB_VERSION.tar.gz \
    && rm apache-couchdb-$COUCHDB_VERSION.tar.gz \
    && cd apache-couchdb-$COUCHDB_VERSION \
    && ./configure --prefix=/usr/local --with-js-lib=/usr/local/lib --with-js-include=/usr/local/include \
    && make \
    && make install \
    && cd / \
    # clean up
    && rm -rf apache-couchdb-$COUCHDB_VERSION \
    && apt-get remove -qq -y build-essential libcurl4-openssl-dev erlang-dev libicu-dev python zip \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

VOLUME /usr/local/var/lib/couchdb

# Make CouchDB listen on all addresses
RUN sed -i -r 's/;bind_address = 127.0.0.1/bind_address = 0.0.0.0/' /usr/local/etc/couchdb/local.ini

ADD run.sh /run.sh
RUN chmod 755 /*.sh

EXPOSE 5984

ENTRYPOINT ["/run.sh"]
