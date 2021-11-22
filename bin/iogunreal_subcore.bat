@echo off

:: Build the iograft subcore python script command.
set IOGRAFT_SUBCORE_COMMAND=%~dp0\iogunreal_subcore.py %*

:: Launch the Unreal Editor in headless mode. This retrieves the project
:: from the environment and executes the iograft subcore python script.
UE4Editor-Cmd.exe "%UE_PROJECT_PATH%" -run=pythonscript -script="%IOGRAFT_SUBCORE_COMMAND%"
