from unreal_global import *
import unreal_utils
import unreal

@unreal.uclass()
class SamlePythonUnrealLibrary(unreal.SystemLibrary):

        @unreal.ufunction(
            static=True,
            meta=dict(CallInEditor=True, Category="Samle PythonUnrealLibrary"),
        )
        def python_testfunction():
            unreal.log("Execute SystemLibrary Function")