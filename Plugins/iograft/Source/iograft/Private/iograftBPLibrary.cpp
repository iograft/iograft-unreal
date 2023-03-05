// Copyright 2023 Fabrica Software, LLC

#include "iograftBPLibrary.h"

#include "CoreGlobals.h"
#include "EditorStyleSet.h"
#include "Framework/Notifications/NotificationManager.h"
#include "Widgets/Notifications/SNotificationList.h"
#include "iograftCoreEngine.h"
#include "iograftSettings.h"
#include "iograftStyle.h"


UIograftBPLibrary::UIograftBPLibrary(
							const FObjectInitializer& ObjectInitializer)
	: Super(ObjectInitializer)
{}


void 
UIograftBPLibrary::InitializeIograftAPI() {
	UIograftCoreEngine* engine = UIograftCoreEngine::Get();
	if (engine != nullptr)
	{
		engine->StartCore();
	}
	else 
	{
		UE_LOG(LogTemp, Error,
				TEXT("No iograft Core engine has been registered."));
	}
}


void
UIograftBPLibrary::UninitializeIograftAPI() {
	UIograftCoreEngine* engine = UIograftCoreEngine::Get();
	if (engine != nullptr)
	{
		engine->ShutdownCore();
	}
	else
	{
		UE_LOG(LogTemp, Error,
			TEXT("No iograft Core engine has been registered."));
	}
}


bool
UIograftBPLibrary::IsRunningInGameThread()
{
	return IsInGameThread();
}


FString
UIograftBPLibrary::GetIograftEnvironmentName()
{
	return GetDefault<UIograftSettings>()->IograftEnvironmentName;
}


FString
UIograftBPLibrary::GetIograftInstallRoot()
{
	return GetDefault<UIograftSettings>()->IograftInstallRoot;
}


UIograftCoreEngine*
UIograftBPLibrary::GetIograftCoreEngine()
{
	return UIograftCoreEngine::Get();
}


void
UIograftBPLibrary::PostNotification(const FString& message, bool IsWarning)
{
	FNotificationInfo Info(FText::FromString(message));
	Info.ExpireDuration = 5.0f;

	if (IsWarning) {
		Info.Image = FEditorStyle::GetBrush("Icons.Warning");
	}
	else {
		Info.Image = FIograftStyle::Get().GetBrush("iograft.Icon");
	}

	FSlateNotificationManager::Get().AddNotification(Info);
}
