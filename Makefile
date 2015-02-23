IMAGE = registry.giantswarm.io/marian/couchdb

build:
	docker build -t $(IMAGE) .

run-local-couchdb:
	docker run -ti -p 5984:5984 -e COUCHDB_PASS="mypass" $(IMAGE)
