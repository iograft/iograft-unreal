// Copyright 2023 Fabrica Software, LLC

#include "iograftModule.h"

#include "ISettingsModule.h"
#include "Misc/MessageDialog.h"
#include "ToolMenus.h"
#include "iograftCommands.h"
#include "iograftCoreEngine.h"
#include "iograftSettings.h"
#include "iograftStyle.h"


#define LOCTEXT_NAMESPACE "iograft"


void
FIograftModule::StartupModule()
{
	if (GIsEditor)
	{
		RegisterSettings();

		if (!IsRunningCommandlet())
		{
			FIograftStyle::Initialize();
			FIograftStyle::ReloadTextures();
			RegisterCommands();

			// Register the iograft toolbar.
			UToolMenus::RegisterStartupCallback(
				FSimpleMulticastDelegate::FDelegate::CreateRaw(
									this, &FIograftModule::RegisterMenus));
		}
	}
}


void
FIograftModule::ShutdownModule()
{
	if (GIsEditor)
	{
		if (!IsRunningCommandlet())
		{
			UToolMenus::UnRegisterStartupCallback(this);
			UToolMenus::UnregisterOwner(this);
			FIograftCommands::Unregister();
			FIograftStyle::Shutdown();
		}

		UnregisterSettings();
	}
}


void
FIograftModule::RegisterSettings()
{
	ISettingsModule* SettingsModule =
					FModuleManager::GetModulePtr<ISettingsModule>("Settings");
	if (SettingsModule != nullptr) {
		SettingsModule->RegisterSettings("Project", "Plugins", "iograft",
			LOCTEXT("iograftSettingsName", "iograft"),
			LOCTEXT("iograftSettingsDescription",
					"Configure the iograft plugin."),
			GetMutableDefault<UIograftSettings>());
	}
}


void
FIograftModule::UnregisterSettings()
{
	ISettingsModule* SettingsModule =
					FModuleManager::GetModulePtr<ISettingsModule>("Settings");
	if (SettingsModule != nullptr) {
		SettingsModule->UnregisterSettings("Project", "Plugins", "iograft");
	}
}


void
FIograftModule::StartIograftButtonClicked()
{
	UIograftCoreEngine* engine = UIograftCoreEngine::Get();
	if (engine == nullptr) {
		UE_LOG(LogTemp, Error,
				TEXT("No iograft Core engine has been registered."));
		return;
	}

	engine->StartCore();
}


void
FIograftModule::StopIograftButtonClicked()
{
	UIograftCoreEngine* engine = UIograftCoreEngine::Get();
	if (engine == nullptr) {
		UE_LOG(LogTemp, Error,
				TEXT("No iograft Core engine has been registered."));
		return;
	}

	engine->ShutdownCore();
}


void
FIograftModule::LaunchUIButtonClicked()
{
	UIograftCoreEngine* engine = UIograftCoreEngine::Get();
	if (engine == nullptr) {
		UE_LOG(LogTemp, Error,
				TEXT("No iograft Core engine has been registered."));
		return;
	}

	engine->LaunchUi();
}


void
FIograftModule::RegisterCommands()
{
	FIograftCommands::Register();

	IograftCommands = MakeShareable(new FUICommandList);
	IograftCommands->MapAction(
		FIograftCommands::Get().StartIograftAction,
		FExecuteAction::CreateRaw(this, &FIograftModule::StartIograftButtonClicked),
		FCanExecuteAction());
	IograftCommands->MapAction(
		FIograftCommands::Get().StopIograftAction,
		FExecuteAction::CreateRaw(this, &FIograftModule::StopIograftButtonClicked),
		FCanExecuteAction());
	IograftCommands->MapAction(
		FIograftCommands::Get().LaunchUIAction,
		FExecuteAction::CreateRaw(this, &FIograftModule::LaunchUIButtonClicked),
		FCanExecuteAction());
}


TSharedRef<SWidget>
FIograftModule::GenerateToolBarMenu()
{
	const bool bShouldCloseWindowAfterMenuSelection = true;
	FMenuBuilder MenuBuilder(bShouldCloseWindowAfterMenuSelection, IograftCommands);
	MenuBuilder.BeginSection(NAME_None, FText::FromString("iograft Automation"));
	MenuBuilder.AddMenuEntry(FIograftCommands::Get().StartIograftAction);
	MenuBuilder.AddMenuEntry(FIograftCommands::Get().StopIograftAction);
	MenuBuilder.AddMenuEntry(FIograftCommands::Get().LaunchUIAction);
	MenuBuilder.EndSection();
	return MenuBuilder.MakeWidget();
}


void
FIograftModule::RegisterMenus()
{
	FToolMenuOwnerScoped OwnerScoped(this);

	{
		UToolMenu* Menu = UToolMenus::Get()->ExtendMenu(
									"LevelEditor.LevelEditorToolBar.User");
		FToolMenuSection& Section = Menu->FindOrAddSection("iograft");
		{
			FToolMenuEntry Entry = FToolMenuEntry::InitComboButton(
				TEXT("iograft"),
				FUIAction(),
				FOnGetContent::CreateRaw(this, &FIograftModule::GenerateToolBarMenu),
				LOCTEXT("iograftCombo_Label", "iograft"),
				LOCTEXT("iograftCombo_Tooltip", "iograft Automation Tools"),
				FSlateIcon(FIograftStyle::GetStyleSetName(), "iograft.Icon"));
			Section.AddEntry(Entry);
		}
	}
}


IMPLEMENT_MODULE(FIograftModule, iograft)

#undef LOCTEXT_NAMESPACE
