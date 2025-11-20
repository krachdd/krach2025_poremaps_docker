#!/usr/bin/env bash
# SPDX-FileCopyrightInfo: Copyright © David Krach
# SPDX-License-Identifier: MIT


echo "Setting permissions for poremaps shared folder"

# if HOST_UID or HOST_GID are passed to the container
# as environment variables, e.g. by calling
# docker run -e HOST_UID=$(id -u $USER) -e HOST_GID=$(id -g $USER),
# then we set the permissions of the files in the shared folder
if [ "$HOST_UID" ]; then
    echo "Changing user id to the provided one"
    usermod -u $HOST_UID poremaps
fi
if [ "$HOST_GID" ]; then
    echo "Changing group id to the provided one"
    groupmod -g $HOST_GID poremaps
fi

# Change permissions only if both user and group id were passed.
# Otherwise, this would change ownership to the default id of poremaps,
# which could lead to permission issues with the host user.
if [ "${HOST_UID}" -a "${HOST_GID}" ]; then
    # find all data in /poremaps/shared/ and transfer ownership.
    # sed "1d" removes the /poremaps/shared folder itself (first line) that
    # is within the results of the find command. If no files are present,
    # chown returns an error because arguments are missing. Therefore, errors
    # are redirected into /dev/null. Still, the script might return with an error
    # in this case, and we guarantee successful execution with the || true trick at the end
    find /poremaps/shared/ | sed "1d" | xargs chown -R poremaps:poremaps 2> /dev/null || true
else
    echo "Skipping ownership transfer as host user and/or group id were not provided"
fi

