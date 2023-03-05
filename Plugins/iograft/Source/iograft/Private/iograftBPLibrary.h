// Copyright 2023 Fabrica Software, LLC

#pragma once

#include "Kismet/BlueprintFunctionLibrary.h"
#include "iograftCoreEngine.h"
#include "iograftBPLibrary.generated.h"


UCLASS()
class UIograftBPLibrary : public UBlueprintFunctionLibrary
{
	GENERATED_UCLASS_BODY()

	UFUNCTION(BlueprintCallable, Category = "iograft")
	static void InitializeIograftAPI();

	UFUNCTION(BlueprintCallable, Category = "iograft")
	static void UninitializeIograftAPI();

	UFUNCTION(BlueprintCallable, Category = "iograft")
	static bool IsRunningInGameThread();

	UFUNCTION(BlueprintCallable, Category = "iograft")
	static FString GetIograftEnvironmentName();

	UFUNCTION(BlueprintCallable, Category = "iograft")
	static FString GetIograftInstallRoot();

	UFUNCTION(BlueprintCallable, Category = "iograft")
	static UIograftCoreEngine* GetIograftCoreEngine();

	UFUNCTION(BlueprintCallable, Category = "iograft")
	static void PostNotification(const FString& message, bool IsWarning = false);
};
