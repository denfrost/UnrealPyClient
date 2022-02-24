from unreal_global import *


@unreal.uclass()
class SamplePythonBlueprintLibrary(unreal.BlueprintFunctionLibrary):
    @unreal.ufunction(
        static=True, meta=dict(Category="Samples Python BlueprintFunctionLibrary")
    )
    def python_test_bp_action_noinput():
        unreal.log("Executed from Python!")

    @unreal.ufunction(
        params=[int, str],
        static=True,
        meta=dict(Category="Samples Python BlueprintFunctionLibrary"),
    )
    def python_test_bp_action_input(input_num, input_string):
        unreal.log(
            "Execute Bluerprint Action With Inputs {} {}".format(
                input_num, input_string
            )
        )

    @unreal.ufunction(
        ret=str, static=True, meta=dict(Category="Samples Python BlueprintFunctionLibrary")
    )
    def python_test_bp_action_return():
        result = "Success"
        #unreal.log("Execute Bluerprint Action Return")
        return result
