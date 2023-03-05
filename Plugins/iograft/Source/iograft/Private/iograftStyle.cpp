// Copyright 2023 Fabrica Software, LLC

#include "iograftStyle.h"

#include "Framework/Application/SlateApplication.h"
#include "Interfaces/IPluginManager.h"
#include "Styling/SlateStyle.h"
#include "Styling/SlateStyleRegistry.h"


const FVector2D Icon40x40(40.0f, 40.0f);
#define IMAGE_BRUSH(RelativePath, ...) FSlateImageBrush(Style->RootToContentDir(RelativePath, TEXT(".png")), __VA_ARGS__)

TSharedPtr<FSlateStyleSet> FIograftStyle::IograftStyleInstance = nullptr;


void
FIograftStyle::Initialize()
{
	if (!IograftStyleInstance.IsValid())
	{
		IograftStyleInstance = Create();
		FSlateStyleRegistry::RegisterSlateStyle(*IograftStyleInstance);
	}
}


void
FIograftStyle::Shutdown()
{
	if (IograftStyleInstance.IsValid())
	{
		FSlateStyleRegistry::UnRegisterSlateStyle(*IograftStyleInstance);
		ensure(IograftStyleInstance.IsUnique());
		IograftStyleInstance.Reset();
	}
}


const ISlateStyle&
FIograftStyle::Get()
{
	return *IograftStyleInstance;
}


FName
FIograftStyle::GetStyleSetName()
{
	static FName StyleSetName(TEXT("iograftStyle"));
	return StyleSetName;
}


void
FIograftStyle::ReloadTextures()
{
	if (FSlateApplication::IsInitialized())
	{
		FSlateApplication::Get().GetRenderer()->ReloadTextureResources();
	}
}



TSharedRef<FSlateStyleSet>
FIograftStyle::Create()
{
	TSharedRef<FSlateStyleSet> Style =
							MakeShareable(new FSlateStyleSet("iograftStyle"));
	Style->SetContentRoot(
		IPluginManager::Get().FindPlugin("iograft")->GetBaseDir() /
															TEXT("Resources"));

	Style->Set("iograft.Icon", new IMAGE_BRUSH(TEXT("iograft_40x"), Icon40x40));
	return Style;
}
