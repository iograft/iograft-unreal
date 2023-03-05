// Copyright 2023 Fabrica Software, LLC

#pragma once

#include "CoreMinimal.h"
#include "iograftSettings.generated.h"

UCLASS(config = iograft)
class UIograftSettings : public UObject
{
	GENERATED_BODY()

public:
	/** The name of the iograft environment to use with Unreal. */
	UPROPERTY(config,
				EditAnywhere,
				Category = Settings,
				meta=(ConfigRestartRequired=true),
				DisplayName = "iograft Environment name for Unreal")
	FString IograftEnvironmentName;

	/** The root directory of the iograft install (i.e. C:\Program Files\iograft). */
	UPROPERTY(config,
				EditAnywhere,
				Category = Settings,
				meta = (ConfigRestartRequired = true),
				DisplayName = "iograft install root directory")
	FString IograftInstallRoot;
};
