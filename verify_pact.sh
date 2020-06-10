#!/bin/bash
VERSION=$1
if [ -x $VERSION ]; then
    echo "ERROR: You must specify a provider version"
    exit
fi

pipenv pactman-verifier -b http://pactbroker:pactbroker@127.0.0.1/pacts/provider/UserService/consumer/UserServiceClient/latest \
UserService http://localhost:5001 http://localhost:5001/_pact/provider_states -r -p $VERSION