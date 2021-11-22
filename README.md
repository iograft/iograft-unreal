# iograft Plugin for Unreal Engine

This repository contains scripts and nodes for running iograft within Unreal Engine. It includes an Unreal Subcore command, and a couple of example nodes for Unreal.

## Unreal Subcore for iograft

The Unreal Subcore for iograft (`iogunreal_subcore.py`) defines an iograft Subcore for executing nodes in the Unreal environment. The key feature of this subcore is that it executes all nodes within the main thread using the `iograft.MainThreadSubcore` class. Many of the Unreal Python commands are required to run from the Game Thread, and this MainThreadSubcore ensures that that is the case.

### Setting the Unreal Project Path

When launching the Unreal subcore from iograft, the Unreal project to load is specified via the `UE_PROJECT_PATH` environment variable. There is some flexibility in how this is set. It can be set in the terminal prior to launching iograft, it can be set as an environment variable within iograft's environment json for the Unreal environment, etc.

The project path is set via an environment variable because there is currently a limitation that the subcore launched from iograft cannot directly be passed args from the graph it is running from.
