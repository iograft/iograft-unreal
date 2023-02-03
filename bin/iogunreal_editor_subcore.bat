@echo off
SETLOCAL EnableDelayedExpansion

:: Build the iograft subcore python script command.
set IOGRAFT_SUBCORE_COMMAND=%~dp0\iogunreal_subcore.py %*

:: Set which UnrealEditor command to use based on the UE major version.
set UE4_EDITOR_CMD="UE4Editor-Cmd.exe"
set UE5_EDITOR_CMD="UnrealEditor-Cmd.exe"

:: Default to Unreal 4.
set UE_EDITOR_CMD=%UE4_EDITOR_CMD%
if defined UE_MAJOR_VERSION (
    if !UE_MAJOR_VERSION!==5 (
        set UE_EDITOR_CMD=%UE5_EDITOR_CMD%
    ) else (
        set UE_EDITOR_CMD=%UE4_EDITOR_CMD%
    )
)

:: Launch the full Unreal Editor (not in batch mode). This retrieves the
:: project from the environment and executes the iograft subcore python script.
%UE_EDITOR_CMD% "%UE_PROJECT_PATH%" -ExecutePythonScript="%IOGRAFT_SUBCORE_COMMAND%"
