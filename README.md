# CouchDB Demo

We set up two CouchDB instances and let them talk to each other.

We create our own up-to-date CouchDB Docker image, building CouchDB from source.

## Building our Docker image

The Makefile has all the help you need.

But first, make sure you have logged in with your Giant Swarm account and the `swarm` CLI. Otherwise, adapt the Makefile to match your requirements, especially the `USERNAME` variable in the top.

Then, use this command to build the image:

    make docker-build

This will create an image based on Debian Wheezy. Building might take a bit.

## Test the image locally

Use this command:

    make docker-run

This will launch a Docker container from your custom CouchDB image. You can connect to it using the IP address of your interface and port 5984.

## Pushing the image to the registry

Make sure you have logged in before ussing `docker login https://registry.giantswarm.io/`. Then, use this command to push your image:

    make docker-push

## Creating/starting the Giant Swarm app

Using the provided `swarm.json` file, we will create an application with two CouchDB instances. Both are accessigble by with their own host entry via port 80.

	curl a.couchdemo.gigantic.io
	curl b.couchdemo.gigantic.io

## Working with CouchDB

### 1. Create some content

First, we create a database on A

	curl -X PUT http://admin:THEcouchDBdemo@a.couchdemo.gigantic.io/demo
	curl http://a.couchdemo.gigantic.io/_all_dbs

Then we create a first document:

	curl -X PUT http://admin:THEcouchDBdemo@a.couchdemo.gigantic.io/demo/d516241ea9546cb9bd911f902b000aee -d '{"title": "First test document", "description": "Created on A"}'

### 2. Create continuous replica from A to B ...

	curl -X POST http://admin:THEcouchDBdemo@a.couchdemo.gigantic.io/_replicate -d '{"source": "demo","target": "http://admin:THEcouchDBdemo@b.couchdemo.gigantic.io/demo", "create_target": true, "continuous": true}' -H "Content-Type: application/json"

### 3. ... and vice versa

	curl -X POST http://admin:THEcouchDBdemo@b.couchdemo.gigantic.io/_replicate -d '{"source": "demo","target": "http://admin:THEcouchDBdemo@a.couchdemo.gigantic.io/demo", "create_target": true, "continuous": true}' -H "Content-Type: application/json"

### 4. Adding another document on B

	curl -X PUT http://admin:THEcouchDBdemo@b.couchdemo.gigantic.io/demo/72f5c2e7265683f6f341d7e1b2000ba0 -d '{"title": "Second test document", "description": "Created on B"}'

### 5. Fetching this document from A

	curl http://a.couchdemo.gigantic.io/demo/72f5c2e7265683f6f341d7e1b2000ba0

### 6. Stop instance B

	swarm stop couch-demo/couchb

### 7. Create another document on A

	curl -X PUT http://admin:THEcouchDBdemo@a.couchdemo.gigantic.io/demo/371bd2c52d2bc0ed6b240fa4d6001965 -d '{"title": "Third test document", "description": "Created on A"}'

### 8. Start B again

    swarm start couch-demo/couchb

### 9. Get document from B

After B is back up, it should get the new doc created in B's absence form A.

    curl http://b.couchdemo.gigantic.io/demo/371bd2c52d2bc0ed6b240fa4d6001965
