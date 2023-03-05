// Copyright 2023 Fabrica Software, LLC

using UnrealBuildTool;

public class iograft : ModuleRules
{
	public iograft(ReadOnlyTargetRules Target) : base(Target)
	{
		PCHUsage = ModuleRules.PCHUsageMode.UseExplicitOrSharedPCHs;

		PrivateDependencyModuleNames.AddRange(
			new string[]
			{
				"Core",
				"CoreUObject",
				"EditorStyle",
				"Engine",
				"InputCore",
				"Projects",
				"PythonScriptPlugin",
				"Settings",
				"Slate",
				"SlateCore",
				"ToolMenus",
				"UnrealEd"
			}
			);
	}
}
