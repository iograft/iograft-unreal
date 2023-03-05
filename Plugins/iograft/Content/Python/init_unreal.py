# Copyright 2023 Fabrica Software, LLC

import os
import sys
import unreal


def _get_iograft_python_dir():
    major_version = sys.version_info[0]
    minor_version = sys.version_info[1]
    return "python{}{}".format(major_version, minor_version)


def _get_iograft_environment_name():
    # First try to get the environment name from the IOGRAFT_ENV environment
    # variable.
    environment_name = os.getenv("IOGRAFT_ENV")
    if environment_name is not None:
        return environment_name

    # Otherwise, get the name from the Unreal settings.
    environment_name = unreal.IograftBPLibrary.get_iograft_environment_name()
    return environment_name


def initialize_iograft():
    iograft_root = unreal.IograftBPLibrary.get_iograft_install_root()
    if not iograft_root or not os.path.exists(iograft_root):
        unreal.log_error("iograft install root not set in settings."
                         " Cannot initialize iograft.")
        return

    # Ensure iograft modules are on PYTHONPATH
    python_dir = _get_iograft_python_dir()
    iograft_python_path = os.path.join(iograft_root, python_dir)
    if iograft_python_path not in sys.path:
        sys.path.append(iograft_python_path)

    # Get the environment name to initialize iograft with.
    environment_name = _get_iograft_environment_name()
    if not environment_name:
        unreal.log_error("iograft environment name is not set. Cannot"
                         " initialize iograft.")
        return

    unreal.log(
        "Initializing iograft with environment: '{}'".format(environment_name))

    import iograft
    try:
        iograft.InitializeEnvironment(environment_name)
    except KeyError as e:
        unreal.log_warning(
            "Failed to initialize iograft environment: '{}': {}".format(
                                                        environment_name, e))

    # Initialize the CoreEngine for executing nodes interactively inside
    # Unreal. Importing the core engine module here registers the iograft
    # engine classes.
    import iograft_core_engine


initialize_iograft()
