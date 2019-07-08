import json

from custodian_es_loader import utils


def test_resource_id():
    with open("tests/files/resources.json") as json_file:
        resource = json.load(json_file)[0]

    assert utils.resource_id("ec2", resource) == "i-0223fccd922f9e5c9"
