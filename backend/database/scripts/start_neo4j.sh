#!/bin/bash

if [ $(id -u) -ne 0 ]; then
    echo "This script must be run as root."
    exit 1
fi

CONTAINER_NAME="family_tree_db"
HTTP_PORT=7474

STATE=$(docker container ls -a -f "name=$CONTAINER_NAME" --format "{{.State}}")

if [ "$STATE" == "running" ]; then
    echo "Database already running."
    exit 0
elif [ "$STATE" == "restarting" ]; then
    echo "Database restarting. Run 'docker container ls -a' for more information."
    exit 0
elif [ "$STATE" == "dead" ]; then
    echo "Database cannot be started. Run 'docker container ls -a' for more information."
    exit 1
fi

if [ "$STATE" == 'paused' ]; then
    echo "Database paused. Unpausing..."
    CONTAINER_START_CMD="docker unpause $CONTAINER_NAME"
elif [ "$STATE" == "exited" -o "$STATE" == "created" ]; then
    CONTAINER_START_CMD="docker start $CONTAINER_NAME"
fi


echo "Database starting background..."
echo "Container: $($CONTAINER_START_CMD)"
echo "Dashboard at http://localhost:$HTTP_PORT/"
