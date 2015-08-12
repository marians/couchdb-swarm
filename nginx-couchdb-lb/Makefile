PROJECT = nginx-couchdb-lb
REGISTRY = registry.giantswarm.io
USERNAME := $(shell swarm user)

docker-build:
	docker build -t $(REGISTRY)/$(USERNAME)/$(PROJECT) .

docker-push:
	docker push $(REGISTRY)/$(USERNAME)/$(PROJECT)
