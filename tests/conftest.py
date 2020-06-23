import os

def pytest_addoption(parser):
    parser.addoption(
        "--publish-pact", type=str, action="store",
        help="Upload generated pact file to pact broker with version"
    )
PACT_DIR = os.path.dirname(os.path.abspath(__file__))
print(PACT_DIR.replace("tests","pacts"))