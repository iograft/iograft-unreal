#!/usr/bin/env python3
# Copyright 2021 Fabrica Software, LLC

import argparse
import iograft


def parse_args():
    parser = argparse.ArgumentParser(
            description="Start an iograft subcore to process in Unreal Engine")
    parser.add_argument("--core-address", dest="core_address", required=True)
    return parser.parse_args()


def StartSubcore(core_address):
    # Initialize iograft.
    iograft.Initialize()

    # Create the Subcore object and listen for nodes to be processed. Use
    # the MainThreadSubcore to ensure that all nodes are executed in the
    # main thread.
    subcore = iograft.MainThreadSubcore(core_address)
    subcore.ListenForWork()

    # Uninitialize iograft.
    iograft.Uninitialize()


if __name__ == "__main__":
    args = parse_args()

    # Start the subcore.
    StartSubcore(args.core_address)
