import unreal


@unreal.uclass()
class MCPManager(unreal.Object):
    unreal_python = unreal.uproperty(bool, meta={"Category": "MCP Servers", "DisplayName": "unreal_python"})