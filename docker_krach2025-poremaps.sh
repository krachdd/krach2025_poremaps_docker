#!/usr/bin/env bash
# SPDX-FileCopyrightInfo: Copyright © David Krach <david.krach@mib.uni-stuttgart-de>
# SPDX-License-Identifier: MIT


# Docker Script for poremaps: krach2025-poremaps

# This script provides a command-line interface to manage a Docker container
# for the poremaps project. It allows you to open a container with a shared
# directory between the host and the container.

# Usage:
#     docker_krach2025-poremaps.sh <command> [options]

# Commands:
#     open [image]    Run a container from the specified Docker image.
#                     If no image is provided, the default image is used.
#     help            Display this help message.

# Environment Variables:
#     IMAGE_NAME: Default Docker image name (krach2025-poremaps).
#     SHARED_DIR_HOST: Host directory to be shared with the container.
#     SHARED_DIR_CONTAINER: Directory in the container where the host directory is mounted.

# Dependencies:
#     Docker must be installed and running on the host machine.


# Default Docker image name for the poremaps project
IMAGE_NAME="krach2025-poremaps"

# Host directory to be shared with the container.
# Defaults to the current working directory.
SHARED_DIR_HOST="$(pwd)"

# Directory in the container where the host directory is mounted
SHARED_DIR_CONTAINER="/poremaps/shared"

# Function to display help message
help() {
    echo ""
    echo "Usage: docker_krach2025-poremaps.sh <command> [options]"
    echo ""
    echo "Commands:"
    echo "  open [image]    Run a container from the specified Docker image."
    echo "                  If no image is provided, the default image ($IMAGE_NAME) is used."
    echo "  help            Display this help message."
    echo ""
    echo "Example:"
    echo "  docker_krach2025-poremaps.sh open"
    echo "  docker_krach2025-poremaps.sh open my-custom-image"
    echo ""
}

# Function to start a Docker container
# Arguments:
#   $1: Docker image name (optional, defaults to $IMAGE_NAME)
open() {
    local IMAGE="$1"
    # Use default image if none is provided
    IMAGE="${IMAGE:=$IMAGE_NAME}"

    echo "Starting Docker container from image: $IMAGE"
    echo "Shared directory: $SHARED_DIR_HOST (host) -> $SHARED_DIR_CONTAINER (container)"
    echo ""

    # Run the Docker container with:
    # - Interactive terminal (-it)
    # - Host user and group IDs for permission consistency
    # - Shared directory between host and container
    # - Container name: krach2025-poremaps
    docker run -it \
               -e HOST_UID=$(id -u $USER) \
               -e HOST_GID=$(id -g $USER) \
               -v "$SHARED_DIR_HOST:$SHARED_DIR_CONTAINER" \
               --name "krach2025-poremaps" \
               "$IMAGE" /bin/bash
}

# Function to exec a Docker container
# Arguments:
#   $1: Docker image name (optional, defaults to $IMAGE_NAME)
exec() {
    local IMAGE="$1"
    # Use default image if none is provided
    IMAGE="${IMAGE:=$IMAGE_NAME}"

    echo "Exec /bin/bash Docker container from image: $IMAGE"
    echo "Shared directory: $SHARED_DIR_HOST (host) -> $SHARED_DIR_CONTAINER (container)"
    echo ""
    # Run the Docker container with:
    # - Interactive terminal (-it)
    # - Container name: krach2025-poremaps
    # - Host user and group IDs for permission consistency
    docker exec -u poremaps -it $IMAGE /bin/bash
}

# Main script logic
if [ "$1" = "open" ]; then
    # Use provided image or default to IMAGE_NAME
    open "$2"
elif [ "$1" = "exec" ]; then
    exec "$2"
elif [ "$1" = "help" ]; then
    help
else
    echo "Error: Unknown command '$1'"
    help
    exit 1
fi
