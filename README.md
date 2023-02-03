# iograft for Unreal Engine

This repository contains scripts and nodes for running iograft within Unreal Engine. It includes an Unreal Subcore command, and a couple of example nodes for Unreal.

## Getting Started with an Unreal Environment

Below are the steps required to setup a new environment in iograft for executing nodes in an Unreal subprocess:

1. Clone the iograft-unreal repository.
2. Open the iograft Environment Manager and create a new environment for Unreal (i.e. "unreal").
3. Update the **Plugin Path** to include the "nodes" directory of the iograft-unreal repository.
4. Update the **Subcore Launch Command** to "iogunreal_subcore" (matching the subcore executor name in the bin folder of the iograft-unreal repository). Note: On Windows this will automatically resolve to the "iogunreal_subcore.bat" script.
5. Update the **Path** to include the "bin" directory of the iograft-unreal repository.
6. Update the **Path** to include the directory containing the UE4Editor-Cmd.exe executable for UE4 or the UnrealEditor-Cmd.exe executable for UE5 (this is usually in the Engine/Binaries/Win64 directory of the Unreal install).
7. Update the **Python Path** entry for `...\iograft\python39` by switching "python39" to the version of Python used in Unreal: "python37" for UE4 or leave as "python39" for UE5.
8. Add an **Environment variable** named `UE_MAJOR_VERSION` and set to the major version of Unreal being used (i.e. 4 for UE4, 5 for UE5).
9. Set the UE_PROJECT_PATH environment variable to the Unreal project being used with iograft. See: [Setting the Unreal Project Path](#setting-the-unreal-project-path)
10. Save the environment, use the Environment menu to switch to the Unreal environment just created, and start creating nodes to process in Unreal.

## Unreal Subcore for iograft

The Unreal Subcore for iograft (`iogunreal_subcore.py`) defines an iograft Subcore for executing nodes in the Unreal environment. The key feature of this subcore is that it executes all nodes within the main thread using the `iograft.MainThreadSubcore` class. Many of the Unreal Python commands are required to run from the Game Thread, and this MainThreadSubcore ensures that that is the case.

### Setting the Unreal Project Path

When launching the Unreal subcore from iograft, the Unreal project to load is specified via the `UE_PROJECT_PATH` environment variable. There is some flexibility in how this is set. It can be set in the terminal prior to launching iograft, it can be set as an environment variable within iograft's environment json for the Unreal environment, etc.

The project path is set via an environment variable because there is currently a limitation that the subcore launched from iograft cannot directly be passed args from the graph it is running from.
