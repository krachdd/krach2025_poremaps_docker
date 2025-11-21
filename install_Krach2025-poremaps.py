#!/usr/bin/env python3

# SPDX-FileCopyrightInfo: Copyright © David Krach <david.krach@mib.uni-stuttgart-de>
# SPDX-License-Identifier: MIT

"""
Installs OpenMPI and poremaps, and updates the `.bashrc` file for environment setup.

This script performs the following steps:
1. Installs OpenMPI (if requested) and retrieves the compiler, executable path, and version.
2. Installs poremaps using the OpenMPI compiler and executable.
3. Updates the `.bashrc` file to include the Python virtual environment and OpenMPI paths.

Functions Used:
- `run_ompi_install`: Installs OpenMPI and returns the compiler, executable path, and version.
- `run_pormaps_install`: Installs poremaps using the provided OpenMPI compiler and executable.

Environment Variables:
- `GET_OPENMPI`: Boolean flag to determine if OpenMPI should be installed.
- `ompi_src`: Source directory for OpenMPI installation.
- `poremaps_src`: Source directory for poremaps installation.
- `poremaps_GIT_URL`: Git repository URL for poremaps.

Output:
- Prints the OpenMPI compiler and executable path.
- Updates the `.bashrc` file to source the poremaps virtual environment and OpenMPI paths.
"""

# HEADER --------------------------------------------------------------------------------
import os
import sys
import subprocess
import requests
import tarfile
# END HEADER ----------------------------------------------------------------------------

# Global variable for verbose output, etc....
GET_OPENMPI  = True
VERBOSE      = True
POREMAPSTEST = True

# We use https to clone
POREMAPS_GIT_URL = 'https://git.rwth-aachen.de/david.krach/poremaps.git'
cwd = os.getcwd()
poremaps_src = "poremaps_Krach2025"
os.makedirs(poremaps_src, exist_ok=True)
poremaps_src = os.path.join(cwd, poremaps_src)
ompi_src = "OpenMPI"
os.makedirs(ompi_src, exist_ok=True)
ompi_src = os.path.join(cwd, ompi_src)


def run_ompi_install(_GET_OMPI, _ompi_src, ompi_version = "5.0.9"):
    """
    Installs OpenMPI from source if requested, or falls back to 
    the system's OpenMPI. This function automates the process of 
    downloading, extracting, configuring, building, and installing 
    OpenMPI. If installation fails or is not requested, it 
    defaults to the system's OpenMPI.

    Args:
        _GET_OMPI (bool):
            Flag to determine whether to fetch and install 
            OpenMPI from source.
            If `True`, attempts to download and install OpenMPI.
            If `False`, uses the system's OpenMPI.
        _ompi_src (str):
            Path to the directory where OpenMPI source will be 
            downloaded and extracted.
        ompi_version (str, optional):
            Version of OpenMPI to install. Defaults to "5.0.9".
            Expected format: "X.Y.Z" (e.g., "5.0.9").

    Returns:
        tuple:
            A tuple containing three elements:
            - ompi_compiler (str): Path to the OpenMPI C++ 
              compiler (`mpiCC`).
            - ompi_exec (str): Path to the OpenMPI execution 
              wrapper (`mpirun`).
            - ompi_version (str): Version of OpenMPI used 
              (either installed or system default).

    Raises:
        Exception:
            If the download or extraction fails, the function will 
            print a warning and fall back to the system's OpenMPI.
            No exception is raised explicitly, but errors during 
            installation will be caught and handled gracefully :).

    Example:
        >>> run_ompi_install(True, "/path/to/src", "5.0.9")
        ('/path/to/src/openmpi-5.0.9/build/bin/mpiCC',
         '/path/to/src/openmpi-5.0.9/build/bin/mpirun',
         '5.0.9')
    """

    if _GET_OMPI:
        # Change to the source directory
        os.chdir(_ompi_src)

        # Construct the download URL for the specified OpenMPI version
        ompi_url = f"https://download.open-mpi.org/release/open-mpi/v{ompi_version[0]}.{ompi_version[2]}/openmpi-{ompi_version}.tar.gz"

        try:
            # Download the tarball
            print(f'### DOWNLOADING OpenMPI {ompi_version} ###')
            tarball = requests.get(ompi_url, stream=True)

            # Extract the tarball
            print(f'### EXTRACTING TARBALL ###')
            file = tarfile.open(fileobj=tarball.raw, mode="r|gz")
            file.extractall(path=".")

            # Set paths for the OpenMPI compiler and execution wrapper
            ompi_compiler = os.path.join(os.getcwd(), f"openmpi-{ompi_version}/build/bin/mpiCC")
            ompi_exec = os.path.join(os.getcwd(), f"openmpi-{ompi_version}/build/bin/mpirun")

            # Navigate to the OpenMPI source directory
            os.chdir(f'openmpi-{ompi_version}')

            # Create a build directory if it doesn't exist
            os.makedirs('build', exist_ok=True)
            os.chdir('build')

            # Configure OpenMPI
            print(f'### CONFIGURING OpenMPI ###')
            if VERBOSE:
                os.system(f'../configure --prefix=$PWD')
            else:
                os.system(f'../configure --prefix=$PWD > ompi_config.log')

            # Build and install OpenMPI
            print(f'### BUILDING & INSTALLING OpenMPI ###')
            if VERBOSE:
                os.system(f'make -j4; make install')
            else:
                os.system(f'make -j4 > ompi_build.log; make install > ompi_install.log')

        except Exception as e:
            # Fall back to system OpenMPI if installation fails
            print(f"### ERROR: {e}\n### Using the system's OpenMPI version.\n### It is advised to install your own version.\n### See https://www.open-mpi.org/software/ompi/v5.0/ for available versions.")
            ompi_compiler = '/usr/bin/mpiCC'
            ompi_exec     = '/usr/bin/mpirun'
    else:
        # Use system OpenMPI if installation is not requested
        print(f"### Using the system's OpenMPI version.\n### It is advised to install your own version.\n### See https://www.open-mpi.org/software/ompi/v5.0/ for available versions.")
        ompi_compiler = '/usr/bin/mpiCC'
        ompi_exec     = '/usr/bin/mpirun'


    return ompi_compiler, ompi_exec, ompi_version


def _ompi_sanity(_exec):
    """
    Perform sanity checks on an executable file to ensure it 
    exists and is executable.  If the file does not exist 
    or is not executable, the function will terminate the 
    program with an appropriate error message.

    Args:
        _exec (str): The path to the executable file to be checked.

    Raises:
        SystemExit: Exits the program with an error message if:
            - The file does not exist.
            - The file is not executable.

    Example:
        >>> _ompi_sanity("/usr/bin/mpirun")
        # Exits with an error if "/usr/bin/mpirun" does not exist 
        or is not executable.
    """
    try:
        if not os.path.isfile(_exec):
            raise FileNotFoundError(f"{_exec} does not exist")
    except Exception as e:
        sys.exit(f"ERROR: {_exec} does not exist\n error {e}")

    try:
        if not os.access(_exec, os.X_OK):
            raise PermissionError(f"{_exec} is not executable")
    except Exception as e:
        sys.exit(f'ERROR: {_exec} is not executable\n error {e}')

def run_pormaps_install(_ompi_compiler, _ompi_exec, _poremaps_src, poremaps_git_url):
    """
    """
    _ompi_sanity(_ompi_compiler)
    _ompi_sanity(_ompi_exec)
    os.chdir(_poremaps_src)
    
    try:
        os.system(f'git clone {poremaps_git_url}')
    except Exception as e:
        sys.exit(f'ERROR: cloning {poremaps_git_url} failed.\n error-> {e}')

    os.chdir('poremaps/src')
    # Replace the compiler exec in the makefile
    os.system(f"sed -i 's|CLINKER=.*|CLINKER={_ompi_compiler}|' makefile")
    os.system('make')


def run_pormaps_install(_ompi_compiler, _ompi_exec, _poremaps_src, poremaps_git_url):
    """
    Installs the poremaps software from a Git repository and compiles it using OpenMPI.

    This function performs the following steps:
    1. Validates the OpenMPI compiler and executable paths.
    2. Changes the working directory to the specified poremaps source directory.
    3. Clones the poremaps repository from the provided Git URL.
    4. Navigates into the poremaps source directory.
    5. Updates the Makefile to use the specified OpenMPI compiler.
    6. Compiles the poremaps software using the updated Makefile.

    Args:
        _ompi_compiler (str): Path to the OpenMPI compiler (e.g., `mpicc`).
        _ompi_exec (str): Path to the OpenMPI executable (e.g., `mpiexec`).
        _poremaps_src (str): Path to the directory where poremaps will be installed.
        poremaps_git_url (str): Git repository URL for poremaps.

    Raises:
        SystemExit: If the Git repository cannot be 
                    cloned or if the Makefile update fails.
        Exception: For any unexpected errors during the installation process.

    Note:
        - Ensure the system has `git`, `make`, and OpenMPI installed.
        - The function assumes the Makefile contains a `CLINKER` variable.
    """


    # Validate OpenMPI compiler and executable paths
    _ompi_sanity(_ompi_compiler)
    _ompi_sanity(_ompi_exec)

    # Change to the specified poremaps source directory
    os.chdir(_poremaps_src)

    try:
        # Clone the poremaps repository
        os.system(f'git clone {poremaps_git_url}')
    except Exception as e:
        sys.exit(f'ERROR: Cloning {poremaps_git_url} failed.\nError: {e}')

    # Navigate into the poremaps source directory
    os.chdir('poremaps/src')

    # Update the Makefile to use the specified OpenMPI compiler
    os.system(f"sed -i 's|CLINKER=.*|CLINKER={_ompi_compiler}|' makefile")

    # Compile poremaps using the updated Makefile
    os.system('make')


# Install OpenMPI and retrieve the compiler, executable, and version
ompi_compiler, ompi_exec, ompi_version = run_ompi_install(GET_OPENMPI, ompi_src)
print(ompi_compiler, ompi_exec)

# Install poremaps using the OpenMPI compiler and executable
pormaps_success = run_pormaps_install(ompi_compiler, ompi_exec, poremaps_src, POREMAPS_GIT_URL)

# Add the poremaps virtual environment to `.bashrc` for automatic activation
os.system(f"echo 'source /poremaps/venv/poremaps/bin/activate' >> /poremaps/.bashrc")

# If OpenMPI was installed and the executable is not the system default,
# update `.bashrc` to include OpenMPI's binary and library paths
if GET_OPENMPI and ompi_exec != '/usr/bin/mpirun':
    # Add OpenMPI's binary directory to the PATH environment variable
    os.system(f"echo 'export PATH={ompi_src}/openmpi-{ompi_version}/build/bin:$PATH' >> /poremaps/.bashrc")
    # Add OpenMPI's library directory to the LD_LIBRARY_PATH environment variable
    os.system(f"echo 'export LD_LIBRARY_PATH={ompi_src}/openmpi-{ompi_version}/build/lib:$LD_LIBRARY_PATH' >> /poremaps/.bashrc")





