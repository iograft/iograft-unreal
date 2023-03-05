// Copyright 2023 Fabrica Software, LLC

#pragma once

#include "Engine.h"
#include "iograftCoreEngine.generated.h"

UCLASS(Blueprintable)
class UIograftCoreEngine : public UObject
{
	GENERATED_BODY()

public:
	UFUNCTION(BlueprintCallable, Category = iograft)
	static UIograftCoreEngine* Get();

	// Callback for when iograft has been initialized.
	UFUNCTION(BlueprintCallable, Category = iograft)
	void OnIograftInitialized() const;

public:
	UFUNCTION(BlueprintImplementableEvent, Category = iograft)
	void StartCore() const;

	UFUNCTION(BlueprintImplementableEvent, Category = iograft)
	void ShutdownCore() const;

	UFUNCTION(BlueprintImplementableEvent, Category = iograft)
	void LaunchUi() const;

	UFUNCTION(BlueprintImplementableEvent, Category = iograft)
	void ExecuteQueuedNode() const;

	UFUNCTION(BlueprintImplementableEvent, Category = iograft)
	FString GetCoreName() const;

protected:
	// Function to be called to notify the
	UFUNCTION(BlueprintCallable, meta = (BlueprintProtected), Category = iograft)
	void ExecuteNodeAsync();
};
