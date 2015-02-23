# CouchDB Demo

We set up two CouchDB instances and let them talk to each other.

	curl a.couchdemo.gigantic.io
	curl b.couchdemo.gigantic.io

## Creating admins (TODO: this shouldn't be necessary)

	curl -sS -X PUT http://a.couchdemo.gigantic.io/_config/admins/admin -d '"THEcouchDBdemo"'
	curl -sS -X PUT http://b.couchdemo.gigantic.io/_config/admins/admin -d '"THEcouchDBdemo"'

## List databases

	curl http://a.couchdemo.gigantic.io/_all_dbs
	curl http://b.couchdemo.gigantic.io/_all_dbs

## Futon

	http://a.couchdemo.gigantic.io/_utils/
	http://b.couchdemo.gigantic.io/_utils/

## Create some content

First, we create a database on A

	curl -X PUT http://admin:THEcouchDBdemo@a.couchdemo.gigantic.io/demo
	curl http://a.couchdemo.gigantic.io/_all_dbs

Let's get a UUIDs for a new document

	http://a.couchdemo.gigantic.io/_uuids

Then we create a first document:

	curl -X PUT http://admin:THEcouchDBdemo@a.couchdemo.gigantic.io/demo/d516241ea9546cb9bd911f902b000aee -d '{"title": "First test document", "description": "Created on A"}'


## Create continous replica on B (pushing from A)

	curl -X POST http://admin:THEcouchDBdemo@a.couchdemo.gigantic.io/_replicate -d '{"source": "demo","target": "http://admin:THEcouchDBdemo@b.couchdemo.gigantic.io/demo", "create_target": true, "continuous": true}' -H "Content-Type: application/json"

## Vice versa

	curl -X POST http://admin:THEcouchDBdemo@b.couchdemo.gigantic.io/_replicate -d '{"source": "demo","target": "http://admin:THEcouchDBdemo@a.couchdemo.gigantic.io/demo", "create_target": true, "continuous": true}' -H "Content-Type: application/json"


## Testing with new documents

Create a test document on B:

	curl -X PUT http://admin:THEcouchDBdemo@b.couchdemo.gigantic.io/demo/72f5c2e7265683f6f341d7e1b2000ba0 -d '{"title": "Second test document", "description": "Created on B"}'

Fetch this document from A:

	curl http://a.couchdemo.gigantic.io/demo/72f5c2e7265683f6f341d7e1b2000ba0

Now we stop server B

	swarm stop couch-demo/couchb

And we create another doc on A

	curl -X PUT http://admin:THEcouchDBdemo@a.couchdemo.gigantic.io/demo/371bd2c52d2bc0ed6b240fa4d6001965 -d '{"title": "Third test document", "description": "Created on A"}'

TODO: test what happens when B is back.
