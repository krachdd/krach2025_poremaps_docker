# SPDX-FileCopyrightInfo: Copyright © David Krach
# SPDX-License-Identifier: MIT

# ------------------------------------------------------------------------------------------
# Dockerfile for krach2025-poremaps: A Docker container for poremaps simulation environment.
# 
# This Dockerfile builds a container based on `phusion/baseimage:jammy-1.0.4`, 
# which is an Ubuntu LTS image optimized for Docker.
# The container is configured to:
# - Install system dependencies for poremaps and OpenMPI.
# - Set up a Python virtual environment.
# - Install poremaps and its dependencies.
# - Configure a non-root user (`poremaps`) for security and usability.
# - Set up shared volumes for host-container communication.

# Base Image:
# - `phusion/baseimage:jammy-1.0.4`: Ubuntu 22.04 LTS with Docker optimizations.
#   See: https://github.com/phusion/baseimage-docker

# Author:
# - David Krach <david.krach@mib.uni-stuttgart.de>

# ------------------------------------------------------------------------------------------

# Use phusion/baseimage:jammy-1.0.4 as the base image
# This image is Ubuntu LTS optimized for Docker compatibility
FROM phusion/baseimage:jammy-1.0.4

# Set metadata for the image
LABEL org.opencontainers.image.authors="david.krach@mib.uni-stuttgart.de"

# --- System Setup ---
# Configure apt to run non-interactively
ENV DEBIAN_FRONTEND=noninteractive

# Update and upgrade system packages, then clean up to reduce image size
RUN apt-get update \
    && apt-get upgrade -y -o Dpkg::Options::="--force-confold" \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

# --- Install Dependencies ---
# Install essential system packages for poremaps and OpenMPI
RUN apt-get update \
    && apt-get install --no-install-recommends --yes \
    ca-certificates \
    vim \
    python3-dev \
    python3-pip \
    python3-requests \
    python3-venv \
    git \
    pkg-config \
    cmake \
    build-essential \
    gfortran \
    mpi-default-bin \
    mpi-default-dev \
    libsuitesparse-dev \
    libsuperlu-dev \
    libeigen3-dev \
    wget \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

# --- User and Permissions ---
# Copy the script to set permissions for the shared folder
COPY set_poremaps_shared_folder_permissions.sh /etc/my_init.d/set_poremaps_shared_folder_permissions.sh

# Create a non-root user for security and usability
# Add a welcome message to the user's `.bashrc`
# Make the permissions script executable
# Add the user to the `video` group for potential graphics support
RUN useradd -m --home-dir /poremaps poremaps \
    && echo "cat /poremaps/WELCOME" >> /poremaps/.bashrc \
    && chmod +x /etc/my_init.d/set_poremaps_shared_folder_permissions.sh \
    && usermod -a -G video poremaps

# Switch to the non-root user and set the working directory
USER poremaps
WORKDIR /poremaps

# --- Shared Volume ---
# Create a shared directory for host-container communication
RUN mkdir /poremaps/shared
VOLUME /poremaps/shared

# --- Welcome Message ---
# Copy the welcome message to be displayed on container entry
COPY WELCOME /poremaps/WELCOME

# --- Python Environment ---
# Create a Python virtual environment for poremaps
RUN python3 -m venv /poremaps/venv/poremaps

# Activate the virtual environment and install essential Python packages
RUN ["/bin/bash", "-c", "source /poremaps/venv/poremaps/bin/activate"]
RUN pip install numpy pyevtk

# --- Git Configuration ---
# Set Git user for potential patch applications during installation
RUN git config --global user.name "David Krach"
RUN git config --global user.email "david.krach@mib.uni-stuttgart.de"

# --- poremaps Installation ---
# Copy and run the installation script for poremaps
# The script handles cloning, configuring, and installing poremaps
COPY install_Krach2025-poremaps.py /poremaps/install_Krach2025-poremaps.py
RUN ./install_Krach2025-poremaps.py && rm -f /poremaps/install_Krach2025-poremaps.py

# Unset Git user after installation
RUN git config --global --unset user.name
RUN git config --global --unset user.email

# --- Final Configuration ---
# Switch back to root for final setup
WORKDIR /poremaps
USER root

# Set the entry point to initialize the container and start a shell as the non-root user
# This ensures permissions are set correctly and the user environment is loaded
ENTRYPOINT ["/sbin/my_init", "--quiet", "--", "/sbin/setuser", "poremaps", "/bin/bash", "-l", "-c"]

# Start an interactive shell by default
CMD ["/bin/bash", "-i"]

