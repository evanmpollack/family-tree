#!/bin/bash

if [ $(id -u) -ne 0 ]; then
    echo "This script must be run as root."
    exit 1
fi

CONTAINER_NAME="family_tree_db"
state=$(docker container ls -a -f "name=$CONTAINER_NAME" --format "{{.State}}")

if [ ! "$state" -o "$state" == "exited" -o "$state" == "created" -o "$state" == "dead" ]; then
    echo "Database not running."
    exit 0
fi

# Restarting container case?

echo "Stopping database..."
echo "Container: $(docker container stop $CONTAINER_NAME)"

docker container ls -a -f "name=$CONTAINER_NAME" --format "{{.State}}"
