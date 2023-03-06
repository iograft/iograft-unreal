@echo off

:: Build the iograft subcore python script command.
set IOGRAFT_SUBCORE_COMMAND=%~dp0\iogunreal_subcore.py %*

:: Set which UnrealEditor command to use based on the UE major version.
set UE_EDITOR_CMD="UE4Editor-Cmd.exe"

:: Check for Unreal 5
set FOUND=
for %%X in (UnrealEditor-Cmd.exe) do (
    set "FOUND=%%~$PATH:X"
)
if defined FOUND (
    set UE_EDITOR_CMD="UnrealEditor-Cmd.exe"
)

:: Launch the Unreal Editor in headless mode. This retrieves the project
:: from the environment and executes the iograft subcore python script.
%UE_EDITOR_CMD% "%UE_PROJECT_PATH%" -run=pythonscript -script="%IOGRAFT_SUBCORE_COMMAND%"
