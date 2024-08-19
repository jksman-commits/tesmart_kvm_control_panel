#!/bin/sh

# Ensure the /config directory exists
mkdir -p /config

# If config.json does not exist, create it
if [ ! -f /config/config.json ]; then
    touch /config/config.json
fi

# Execute the CMD passed from the Dockerfile
exec "$@"

