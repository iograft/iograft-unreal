// Copyright 2023 Fabrica Software, LLC

#pragma once

#include "CoreMinimal.h"
#include "Styling/SlateStyle.h"


class FIograftStyle
{
public:
	static void Initialize();
	static void Shutdown();
	static const ISlateStyle& Get();
	static FName GetStyleSetName();
	static void ReloadTextures();

private:
	static TSharedRef<class FSlateStyleSet> Create();
	static TSharedPtr<class FSlateStyleSet> IograftStyleInstance;
};
