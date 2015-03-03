# encoding: utf8

"""
This is a benchmark script for our CouchDB demo. It runs several tests:

- Create and read documents on/from instance A
- Create and read documents on/from instance B
- Create and read documents on/from both instances via our load balancer
"""

# adjust these to match the actual domains
COUCH_A_HOST = "a.couchdemo-marian.gigantic.io:80"
COUCH_B_HOST = "b.couchdemo-marian.gigantic.io:80"
COUCH_LB_HOST = "lb.couchdemo-marian.gigantic.io:80"

COUCH_USER = "admin"
COUCH_PASS = "THEcouchDBdemo"

import time
import couchdb
import random
import requests
import json
import string

def random_string(length=100):
   return ''.join(random.choice(string.lowercase + string.uppercase) for i in range(length))

def init_dbs(dbname="benchmark"):
	"""
	Deletes the databases and sets them up on both hosts
	"""
	print("Initializing databases")
	coucha = couchdb.Server("http://%s:%s@%s/" % (COUCH_USER, COUCH_PASS, COUCH_A_HOST))
	couchb = couchdb.Server("http://%s:%s@%s/" % (COUCH_USER, COUCH_PASS, COUCH_B_HOST))
	
	# create databases
	if dbname in coucha:
		coucha.delete(dbname)
	if dbname in couchb:
		couchb.delete(dbname)
	
	coucha.create(dbname)
	couchb.create(dbname)

	# set up replica
	headers = {
		"Content-Type": "application/json"
	}
	replica_a_to_b = {
		"source": dbname,
		"target": "http://%s:%s@%s/%s" % (COUCH_USER, COUCH_PASS, COUCH_B_HOST, dbname),
		"continuous": True
	}
	replica_b_to_a = {
		"source": dbname,
		"target": "http://%s:%s@%s/%s" % (COUCH_USER, COUCH_PASS, COUCH_A_HOST, dbname),
		"continuous": True
	}
	r = requests.post("http://%s:%s@%s/_replicate" % (COUCH_USER, COUCH_PASS, COUCH_A_HOST),
		data=json.dumps(replica_a_to_b), headers=headers)
	r.raise_for_status()
	r = requests.post("http://%s:%s@%s/_replicate" % (COUCH_USER, COUCH_PASS, COUCH_B_HOST),
		data=json.dumps(replica_b_to_a), headers=headers)
	r.raise_for_status()


def write_documents(host, dbname="benchmark", num=100):
	"""Writes num documents on host, returns list of IDs"""
	ids = []
	couch = couchdb.Server("http://%s:%s@%s/" % (COUCH_USER, COUCH_PASS, host))
	db = couch[dbname]
	print("Writing %d docs on host %s" % (num, host))
	start = time.time()
	for n in range(num):
		doc = {
			"string": random_string(2000),
			"number": 123,
			"float": 1.234,
			"bool": True
		}
		(docid, ref) = db.save(doc)
		ids.append(docid)
	end = time.time()
	duration = end - start
	print("  Duration: %.3f sec (%.3f docs/sec)" % (duration, float(num)/duration))
	return ids

def read_documents(doc_ids, host, dbname="benchmark"):
	couch = couchdb.Server("http://%s:%s@%s/" % (COUCH_USER, COUCH_PASS, host))
	db = couch[dbname]
	random.shuffle(doc_ids)
	print("Reading docs from host %s" % host)
	start = time.time()
	for doc_id in doc_ids:
		doc = dict(db[doc_id])
	end = time.time()
	duration = end - start
	print("  Duration: %.3f Sec (%.3f docs/sec)" % (duration, float(len(doc_ids))/duration))


if __name__ == "__main__":

	init_dbs()

	ids_a = write_documents(COUCH_A_HOST)
	ids_b = write_documents(COUCH_B_HOST)
	ids_lb = write_documents(COUCH_LB_HOST)

	print("Waiting 10 sec for replicas to catch up")
	time.sleep(10)

	read_documents(ids_a, COUCH_A_HOST)
	read_documents(ids_b, COUCH_B_HOST)
	read_documents(ids_lb, COUCH_LB_HOST)
