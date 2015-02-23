#!/bin/bash

# Based on https://github.com/tutumcloud/tutum-docker-couchdb
# (released under Apache 2.0 license)

# enable job control in script
set -m

# start CouchDB process in background
couchdb &

# set password for admin account
if [ ! -f /.created-admin-password ]; then
    
    # generate pasword (if not set via env COUCHDB_PASS)
    PASS=${COUCHDB_PASS:-$(pwgen -s 12 1)}
    _word=$( [ ${COUCHDB_PASS} ] && echo "preset" || echo "random" )

    RET=7
    while [[ RET -ne 0 ]]; do
        echo "=> Waiting for confirmation of CouchDB service startup"
        sleep 5
        curl -s http://127.0.0.1:5984 >/dev/null 2>&1
        RET=$?
    done

    curl -sS -X PUT http://127.0.0.1:5984/_config/admins/admin -d '"'${PASS}'"'
    touch /.created-admin-password
        
    echo "Your admin password is: $PASS"
fi

# bring couchdb to foreground
fg
