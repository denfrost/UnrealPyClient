import unreal

@unreal.uclass()
class RemoteClass(unreal.BlueprintFunctionLibrary):
    @unreal.ufunction(
        ret=str, static=True
    )
    def py_RPC_Call():
        result = "Success Remote call!!!"
        unreal.log("Execute Remote Procedure Call")
        return result
