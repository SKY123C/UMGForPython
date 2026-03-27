// Some copyright should be here...

using System.IO;
using UnrealBuildTool;

public class PythonBinding : ModuleRules
{
    public PythonBinding(ReadOnlyTargetRules Target) : base(Target)
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
                "EditorSubsystem",
                "UnrealEd",
                "PythonScriptPlugin",
                "ContentBrowser",
                "ContentBrowserData",
                "AssetRegistry"
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
