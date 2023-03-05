// Copyright 2023 Fabrica Software, LLC

#pragma once

#include "CoreMinimal.h"
#include "Framework/Commands/Commands.h"
#include "iograftStyle.h"


class FIograftCommands : public TCommands<FIograftCommands>
{
public:
	FIograftCommands();
	virtual void RegisterCommands() override;

public:
	TSharedPtr<FUICommandInfo> StartIograftAction;
	TSharedPtr<FUICommandInfo> StopIograftAction;
	TSharedPtr<FUICommandInfo> LaunchUIAction;
};
