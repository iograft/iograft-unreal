// Copyright 2023 Fabrica Software, LLC

#include "iograftCoreEngine.h"

#include "Async/Async.h"
#include "IPythonScriptPlugin.h"
#include "Misc/CoreDelegates.h"
#include "Templates/Casts.h"


UIograftCoreEngine*
UIograftCoreEngine::Get()
{
	TArray<UClass*> CoreEngineClasses;
	GetDerivedClasses(UIograftCoreEngine::StaticClass(), CoreEngineClasses);
	int32 NumClasses = CoreEngineClasses.Num();
	if (NumClasses > 0)
	{
		return Cast<UIograftCoreEngine>(
						CoreEngineClasses[NumClasses - 1]->GetDefaultObject());
	}

	return nullptr;
}


static void OnPythonShutdown()
{
	UIograftCoreEngine* engine = UIograftCoreEngine::Get();
	if (engine != nullptr)
	{
		engine->ShutdownCore();
	}
}


void
UIograftCoreEngine::OnIograftInitialized() const
{
	IPythonScriptPlugin::Get()->OnPythonShutdown().AddStatic(OnPythonShutdown);
}


void
UIograftCoreEngine::ExecuteNodeAsync()
{
	AsyncTask(ENamedThreads::GameThread, [this]()
	{
		this->ExecuteQueuedNode();
	});
}
