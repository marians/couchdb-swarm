# CouchDB Demo

We set up two CouchDB instances and let them talk to each other (replicate their data). Then we access the two CouchDB instances via an nginx load balancer.

## Setting up two replicating CouchDB instances

We create our own up-to-date CouchDB Docker image, building CouchDB from source. Also, we build ourselves a little nginx load balancer.

### Building our CouchDB Docker images

The Makefile has all the help you need.

But first, make sure you have logged in with your Giant Swarm account and the `swarm` CLI. Otherwise, adapt the Makefile to match your requirements, especially the `USERNAME` variable in the top.

Then, use these commands to build the images:
	
	cd couchdb
    make docker-build

This will create an image based on Debian Wheezy. Building might take a bit.

### Test the CouchDB image locally

Use this command:

    make docker-run

This will launch a Docker container from your custom CouchDB image. You can connect to it using the IP address of your interface and port 5984.

### Building the nginx image

This works the same way as with the couchdb image, but in a different folder.

    cd ../nginx-couchdb-lb
	make docker-build

### Pushing the images to the registry

Make sure you have logged in before ussing `docker login https://registry.giantswarm.io/`. Then, use these commands to push your images:
	
	cd ../couchdb
    make docker-push

    cd ../nginx-couchdb-lb
    make docker-push

### Creating/starting the Giant Swarm app

Using the provided `swarm.json` file, we will create a Giant Swarm application. We use our username to disambiguate the domain entries.

	swarm up --var=username=`swarm user`

Both CouDBs are accessible by with their own host entry via port 80.

	curl a.couchdemo-`swarm user`.gigantic.io
	curl b.couchdemo-`swarm user`.gigantic.io

### Working with CouchDB

#### 1. Create some content

First, we create a database on A

	curl -X PUT http://admin:THEcouchDBdemo@a.couchdemo.gigantic.io/demo
	curl http://a.couchdemo.gigantic.io/_all_dbs

Then we create a first document:

	curl -X PUT \
		http://admin:THEcouchDBdemo@a.couchdemo.gigantic.io/demo/d516241ea9546cb9bd911f902b000aee \
		-d '{"title": "First test document", "description": "Created on A"}'

#### 2. Create continuous replica from A to B ...

	curl -X POST \
		http://admin:THEcouchDBdemo@a.couchdemo.gigantic.io/_replicate \
		-d '{"source": "demo","target": "http://admin:THEcouchDBdemo@b.couchdemo.gigantic.io/demo", "create_target": true, "continuous": true}' \
		-H "Content-Type: application/json"

#### 3. ... and vice versa

	curl -X POST \
		http://admin:THEcouchDBdemo@b.couchdemo.gigantic.io/_replicate \
		-d '{"source": "demo","target": "http://admin:THEcouchDBdemo@a.couchdemo.gigantic.io/demo", "create_target": true, "continuous": true}' \
		-H "Content-Type: application/json"

#### 4. Adding another document on B

	curl -X PUT \
		http://admin:THEcouchDBdemo@b.couchdemo.gigantic.io/demo/72f5c2e7265683f6f341d7e1b2000ba0 \
		-d '{"title": "Second test document", "description": "Created on B"}'

#### 5. Fetching this document from A

	curl http://a.couchdemo.gigantic.io/demo/72f5c2e7265683f6f341d7e1b2000ba0

#### 6. Stop instance B

	swarm stop couch-demo/couchb

#### 7. Create another document on A

	curl -X PUT \
		http://admin:THEcouchDBdemo@a.couchdemo.gigantic.io/demo/371bd2c52d2bc0ed6b240fa4d6001965 \
		-d '{"title": "Third test document", "description": "Created on A"}'

#### 8. Start B again

    swarm start couch-demo/couchb

#### 9. Get document from B

After B is back up, it should get the new doc created in B's absence form A.

    curl http://b.couchdemo.gigantic.io/demo/371bd2c52d2bc0ed6b240fa4d6001965

## Using the load balancer

If we wanted our clients to be unaware of the number of CouchDB backends and spread load nicely via all instances, a load balancer might be useful.

We already built the image above, but didn't make use of it yet. Here we test it's up:

	curl a.couchdemo-`swarm user`.gigantic.io

Call the above command several times to see that the response is changing slightly. The `uuid` returned should differ between requests, depending by witch host the response is served.

Since both CouchDB instance replicate their content, we don't really care which instance is accessed.

The provided backup script (written in Python) runs a test on both instances directly and then over the load balancer to see if there gains in throughput. Here is how to set it up using `virtualenv` and `pip`.

    virtualenv venv
    source venv/bin/activate
    pip install requests couchdb

Once this is done, call it using

    python benchmark.py

The script creates a database called `benchmark`. When it already exists, the database is deleted and re-created.

Then, documents are created first on one instnce, then on the other instance, then via the load balancer. In the next step, the same documents are read in randomized order from one host, then from the other host, then via the load balancer.

In our tests, the speed gain from using the load balancer is minimal. The benefit that the CouchDB cluster is hidden from the clients is far greater.
