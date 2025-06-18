#!/bin/bash

if [ $(id -u) -ne 0 ]; then
    echo "This script must be run as root."
    exit 1
fi

CONTAINER_NAME="family_tree_db"
HTTP_PORT=7474
VOLUME_PATH="$PROJECTS_ROOT/family-tree/backend/database"

state=$(docker container ls -a -f "name=$CONTAINER_NAME" --format "{{.State}}")

if [ ! "$state" ]; then
    echo "Database has not been created. Creating..."
    docker container create --name $CONTAINER_NAME \
        -p7474:7474 \
        -p7687:7687 \
        -v $VOLUME_PATH/data:/data \
        -v $VOLUME_PATH/logs:/logs \
        -v $VOLUME_PATH/conf:/conf \
        -v $VOLUME_PATH/import:/import \
        -v $VOLUME_PATH/plugins:/plugins \
        --env NEO4J_PLUGINS=[\"apoc\",\"apoc-extended\"] \
        neo4j:latest
    state="created"
elif [ "$state" == "running" ]; then
    echo "Database already running."
    exit 0
elif [ "$state" == "restarting" ]; then
    echo "Database restarting. Run 'docker container ls -a' for more information."
    exit 0
elif [ "$state" == "dead" ]; then
    echo "Database cannot be started. Run 'docker container ls -a' for more information."
    exit 1
fi

if [ "$state" == "paused" ]; then
    echo "Database paused. Unpausing..."
    CONTAINER_START_CMD="docker unpause $CONTAINER_NAME"
elif [ "$state" == "exited" -o "$state" == "created" ]; then
    CONTAINER_START_CMD="docker start $CONTAINER_NAME"
fi


echo "Database starting background..."
echo "Container: $($CONTAINER_START_CMD)"
echo "Dashboard at http://localhost:$HTTP_PORT/"
