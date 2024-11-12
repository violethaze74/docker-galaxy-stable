#!/bin/bash
if ! docker build -t bioblend_test .; then
    echo "Bioblend docker image build failed."
    exit 1
fi

if ! docker run --link galaxy -v /tmp/:/tmp/ bioblend_test; then
    echo "Bioblend tests failed."
    exit 1
fi
