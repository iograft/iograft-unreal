// Copyright 2023 Fabrica Software, LLC

#pragma once

#include "IIograftModule.h"

#include "Modules/ModuleInterface.h"
#include "Modules/ModuleManager.h"


class FToolBarBuilder;
class FMenuBuilder;

class FIograftModule : public IModuleInterface
{
public:
	virtual void StartupModule() override;
	virtual void ShutdownModule() override;

	void StartIograftButtonClicked();
	void StopIograftButtonClicked();
	void LaunchUIButtonClicked();

private:
	void RegisterMenus();
	TSharedRef<SWidget> GenerateToolBarMenu();

	void RegisterCommands();
	void RegisterSettings();
	void UnregisterSettings();

private:
	TSharedPtr<class FUICommandList> IograftCommands;
};
