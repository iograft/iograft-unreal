# iograft for Unreal Engine

This repository contains scripts and nodes for running iograft within Unreal Engine. It includes an Unreal Subcore command, example nodes for Unreal, and an Unreal Plugin for using iograft interactively within Unreal Engine.

iograft supports both Unreal 4 and Unreal 5.

## Getting Started with an Unreal Environment

The first step to use iograft with Unreal Engine is to create an Unreal "environment" within iograft. Below are the steps required to setup this environment:

1. Clone the iograft-unreal repository.
2. Open the iograft Environment Manager and create a new environment for Unreal (i.e. "unreal5").
3. Update the **Plugin Path** to include the "nodes" directory of the iograft-unreal repository.
4. Update the **Subcore Launch Command** to "iogunreal_subcore" (matching the subcore executor name in the bin folder of the iograft-unreal repository). Note: On Windows this will automatically resolve to the "iogunreal_subcore.bat" script.
5. Update the **Path** to include the "bin" directory of the iograft-unreal repository.
6. Update the **Path** to include the directory containing the UnrealEditor-Cmd.exe executable for UE5 (this is usually in the Engine/Binaries/Win64 directory of the Unreal install) or the UE4Editor-Cmd.exe executable for UE4.
7. **UE4**: Update the **Python Path** entry for `...\iograft\python39` by switching "python39" to the version of Python used in Unreal 4: "python37" (Unreal 5 uses python39, so no changes are needed).
8. Update the **Python Path** to include the "python" directory of the iograft-unreal repository.
9. **Optional**: Set the UE_PROJECT_PATH environment variable to the Unreal project being used with iograft. See: [Setting the Unreal Project Path](#setting-the-unreal-project-path)
10. Save the environment, use the Environment menu to switch to the Unreal environment just created, and start creating nodes to process in Unreal.

<details>
<summary>A full example "unreal5" environment looks like this:</summary>

```
{
    "plugin_path": [
        "{IOGRAFT_INSTALL_DIR}\\types",
        "{IOGRAFT_INSTALL_DIR}\\nodes",
        "{IOGRAFT_USER_CONFIG_DIR}\\types",
        "{IOGRAFT_USER_CONFIG_DIR}\\nodes",
        "C:\\Projects\\iograft-unreal\\nodes"
    ],
    "subcore": {
        "launch_command": "iogunreal_subcore"
    },
    "path": [
        "{IOGRAFT_INSTALL_DIR}\\bin",
        "C:\\Projects\\iograft-unreal\\bin",
        "C:\\Program Files\\Epic Games\\UE_5.1\\Engine\\Binaries\\Win64"
    ],
    "python_path": [
        "{IOGRAFT_INSTALL_DIR}\\types",
        "{IOGRAFT_INSTALL_DIR}\\python39",
        "C:\\Projects\\iograft-unreal\\python"
    ],
    "environment_variables": {
        "PYTHONDONTWRITEBYTECODE": "1",
        "UE_PROJECT_PATH": "C:\\Projects\\iograftdemo_ue5\\iograftdemo_ue5.uproject"
    },
    "ui": {
        "icon_file_path": "C:\\Program Files\\Epic Games\\UE_5.1\\Engine\\Build\\Windows\\Resources\\Default.ico"
    },
    "appended_environments": [],
    "name": "unreal5"
}
```
</details>

## iograft Plugin for Unreal

This repository includes a plugin for using iograft interactively within Unreal Engine. To install the plugin, copy the `iograft` directory in this repository's "Plugins" directory into the "Plugins" directory of your Unreal project. On the next launch of your project, you will be prompted to build the iograft plugin:

![rebuild iograft plugin](https://user-images.githubusercontent.com/565780/224118721-a6b7e6e1-d20f-40d8-8265-0092e0b61a48.png)

Once built and Unreal has opened, open the Project Settings and go to the "iograft" settings. The two settings that are needed are:
1. The name of the iograft environment to use within this project (i.e. [Getting Started with an Unreal Environment](#getting-started-with-an-unreal-environment)).
2. The iograft install path (by default: `C:/Program Files/iograft`).

![iograft plugin settings](https://user-images.githubusercontent.com/565780/224120288-2650b175-8a7e-4a80-8e38-2c016698d6dd.png)

After updating the settings you will need to restart the Unreal project. When the project is restarted, iograft will be ready to use within Unreal and available on the top toolbar!

![iograft toolbar](https://user-images.githubusercontent.com/565780/224121195-76d0862c-0a11-41b1-b4ac-a5d13ef2f4f6.png)

## Setting the Unreal Project Path

When launching the Unreal subcore from iograft, the Unreal project to load is specified via the `UE_PROJECT_PATH` environment variable. There is some flexibility in how this is set. It can be set in the terminal prior to launching iograft, it can be set as an environment variable within iograft's environment json for the Unreal environment, etc.

## Unreal Subcore for iograft

The Unreal Subcore for iograft (`iogunreal_subcore.py`) defines an iograft Subcore for executing nodes in the Unreal environment. The key feature of this subcore is that it executes all nodes within the main thread using the `iograft.MainThreadSubcore` class. Many of the Unreal Python commands are required to run from the Game Thread, and this MainThreadSubcore ensures that that is the case.

### Full Editor Subcore

In some cases, it might be necessary to launch the FULL Unreal Editor rather than the headless version of Unreal. In these cases, there is an additional subcore available (`iogunreal_editor_subcore`) which launches the full editor, runs the Subcore, and shuts down when the subcore is terminated.
