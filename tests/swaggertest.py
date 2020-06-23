import json
import logging
import os
import sys

import pytest
import requests
from requests.auth import HTTPBasicAuth

from pact_python_demo.client import UserClient
from pactman import Consumer, Like, Provider, Term

log = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


PACT_UPLOAD_URL = (
    "http://127.0.0.1/pacts/provider/PetService/consumer"
    "/PetServiceClient/version"
)
h = {'Content-Type': 'application/json'}

PACT_FILE = "PetServiceClient-PetService-pact.json"
PACT_BROKER_USERNAME = "pactbroker"
PACT_BROKER_PASSWORD = "pactbroker"

PACT_MOCK_HOST = 'localhost'
PACT_MOCK_PORT = 1234
PACT_DIR = os.path.dirname(os.path.abspath(__file__)).replace("tests","pacts")

@pytest.fixture
def client():
    return UserClient(
        'http://{host}:{port}'
        .format(host=PACT_MOCK_HOST, port=PACT_MOCK_PORT)
    )


def push_to_broker(version):
    """TODO: see if we can dynamically learn the pact file name, version, etc."""
    with open(os.path.join(PACT_DIR, PACT_FILE), 'rb') as pact_file:
        pact_file_json = json.load(pact_file)

    basic_auth = HTTPBasicAuth(PACT_BROKER_USERNAME, PACT_BROKER_PASSWORD)

    log.info("Uploading pact file to pact broker...")
    r = requests.put(
        "{}/{}".format(PACT_UPLOAD_URL, version),
        auth=basic_auth,
        json=pact_file_json
    )
    if not r.ok:
        log.error("Error uploading: %s", r.content)
        r.raise_for_status()


@pytest.fixture(scope='session')
def pact(request):
    pact = Consumer('PetServiceClient').has_pact_with(
        Provider('PetService'), host_name=PACT_MOCK_HOST, port=PACT_MOCK_PORT,
        pact_dir=PACT_DIR,version="3.0.0")
    pact.start_service()
    yield pact
    pact.stop_service()

    version = request.config.getoption('--publish-pact')
    if not request.node.testsfailed and version:
        push_to_broker(version)


def test_pet_as_default(pact, client):
    expected = {
        'id': 0,
        'petId': 0,
        'shipDate': Term(
            r'\d+-\d+-\d+T\d+:\d+:\d+.\d+Z',
            '1944-02-07T13:54:19.92Z'
        ),
        'quantity': 0,
        'status': Term(
            r'\w+',
            'placed'
        ),
        'complete': False
    }
    (pact
     .given('Pet Order is Ready')
     .upon_receiving('a request for order')
     .with_request('get', '/store/order/3')
     .will_respond_with(200, headers={'Content-Type': 'application/json'},body=Like(expected)))

    with pact:
        result = client.get_order('3')

    # assert something with the result, for ex, did I process 'result' properly?
    # or was I able to deserialize correctly? etc.

