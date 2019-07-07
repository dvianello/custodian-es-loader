import json
from smart_open import open
from elasticsearch import Elasticsearch
import elasticsearch.exceptions

import hashlib
import datetime
import sys

import custodian_es_loader.utils as utils


def load_metadata(metadata_path):
    with open(metadata_path) as file:
        metadata = json.load(file)

    return metadata


def load_resources(resources_path):
    with open(resources_path) as file:
        resources = json.load(file)

    return resources


def generate_id(resource, metadata):
    resource_type = metadata['policy']['resource']

    id = "{}-{}-{}".format(
        metadata['policy'],
        metadata['execution']['start'],
        utils.resource_id(resource_type, resource)
    )
    id = hashlib.sha3_256(id.encode('utf-8')).hexdigest()

    return id


def process_resources(resources, metadata):
    policy = metadata['policy']
    execution = metadata['execution']
    resource_type = metadata['policy']['resource']
    region = metadata['config']['region']

    es_client = Elasticsearch(['localhost'], sniff_on_connection_fail=True, port=32775, http_auth=('elastic', 'changeme'))

    for resource in resources:
        resource_doc = dict(
            resource,
            **{
               'id': execution['id'],
                'policy_name': policy['name'],
                'start_time': datetime.datetime.fromtimestamp(execution['start']),
                'end_time': datetime.datetime.fromtimestamp(execution['end_time']),
                'duration': execution['duration'],
                'region': region
            }
        )

        document_id = generate_id(resource, metadata)

        try:
            result = es_client.index(index=resource_type, body=resource_doc, id=document_id)

        except elasticsearch.exceptions.TransportError:
            print("Something went wrong with the connection to ElasticSearch. Aborting.")
            sys.exit()

        if result['result'] == "updated":
            print("Record {} already existed. Updated.".format(document_id))
        else:
            print("Record {} created.".format(document_id))






