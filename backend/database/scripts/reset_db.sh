#!/bin/bash

if [ ! "$PROJECTS_ROOT" ]; then
    echo "This script must be run with 'sudo -E'"
    exit 1
fi

VOLUME_PATH="$PROJECTS_ROOT/family-tree/backend/database"

echo "Deleting data..."
rm -fr $VOLUME_PATH/data/*
rm -fr $VOLUME_PATH/plugins/*
rm -fr $VOLUME_PATH/logs/*
