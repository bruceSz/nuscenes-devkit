#!/bin/bash
set -eux

image_name=$1
dockerfile=$2

unittest_container_name=test_container

function clean_up(){
    echo "Cleaning up docker containers and volumes if they already exist"
    docker rm -f ${unittest_container_name} || { echo "test container does not exist"; }
}

trap clean_up EXIT

clean_up

echo "Building image containing nuscenes-devkit"
docker build -t ${image_name} -f ${dockerfile} . || { echo "Failed to build main Docker image"; exit 1; }

# Run baseline unit tests.
docker run --name=${unittest_container_name} -v /data:/data \
    -e NUSCENES=/data/sets/nuscenes ${image_name} \
    /bin/bash -c "set -eux; source activate nuenv && cd python-sdk && python -m unittest"

clean_up
