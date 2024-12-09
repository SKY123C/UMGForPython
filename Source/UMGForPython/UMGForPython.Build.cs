// Some copyright should be here...

using System.IO;
using UnrealBuildTool;

public class UMGForPython : ModuleRules
{
	public UMGForPython(ReadOnlyTargetRules Target) : base(Target)
	{
		PCHUsage = ModuleRules.PCHUsageMode.UseExplicitOrSharedPCHs;
        string EngineDir = Path.GetFullPath(Target.RelativeEnginePath);
        PublicIncludePaths.AddRange(
			new string[] {
				// ... add public include paths required here ...
			}
			);


        PrivateIncludePaths.AddRange(
            new string[] {
                
            });


        PublicDependencyModuleNames.AddRange(
			new string[]
			{
				"Core",
				// ... add other public dependencies that you statically link with here ...
			}
			);
			
		
		PrivateDependencyModuleNames.AddRange(
			new string[]
			{
				"CoreUObject",
				"Engine",
				"Slate",
				"SlateCore",
                "ToolMenus",
                "Projects",
				"UnrealEd",
                "PythonScriptPlugin",
                "UMG",
                "Blutility",
				"InputCore",
                "Python3"
				// ... add private dependencies that you statically link with here ...	
			}
			);
		
		
		DynamicallyLoadedModuleNames.AddRange(
			new string[]
			{
				// ... add any modules that your module loads dynamically here ...
			}
			);
	}
}
