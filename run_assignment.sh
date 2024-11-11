#!/usr/bin/env bash

cd "$(dirname "$0")"

docker build -t cs4115 .
docker run cs4115
