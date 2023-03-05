// Copyright 2023 Fabrica Software, LLC

#pragma once

#include "Modules/ModuleInterface.h"
#include "Modules/ModuleManager.h"

#define IOGRAFT_MODULE_NAME TEXT("iograft")


class IIograftModule : public IModuleInterface
{
 public:
    static inline IIograftModule& Get() {
        return FModuleManager::LoadModuleChecked<IIograftModule>(
                                                        IOGRAFT_MODULE_NAME);
    }

    static inline bool IsAvailable()
    {
        return FModuleManager::Get().IsModuleLoaded(IOGRAFT_MODULE_NAME);
    }
};
