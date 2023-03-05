// Copyright 2023 Fabrica Software, LLC

#include "iograftCommands.h"

#include "iograftStyle.h"


#define LOCTEXT_NAMESPACE "iograft"


FIograftCommands::FIograftCommands() :
	TCommands<FIograftCommands>(
		TEXT("iograft"),
		NSLOCTEXT("Contexts", "iograft", "iograft Plugin"),
		NAME_None,
		FIograftStyle::GetStyleSetName())
{}


void
FIograftCommands::RegisterCommands()
{
	UI_COMMAND(StartIograftAction,
				"Initialize iograft API",
				"Initialize the iograft API and create an Unreal Core object",
				EUserInterfaceActionType::Button,
				FInputChord());
	UI_COMMAND(StopIograftAction,
				"Shutdown iograft API",
				"Shutdown the iograft API",
				EUserInterfaceActionType::Button,
				FInputChord());
	UI_COMMAND(LaunchUIAction,
				"Launch iograft UI",
				"Launch the iograft UI and connect to the Unreal Core",
				EUserInterfaceActionType::Button,
				FInputChord());
}


#undef LOCTEXT_NAMESPACE
