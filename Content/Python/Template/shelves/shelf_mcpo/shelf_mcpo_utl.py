

def get_interpreter_executable_path():
    result = ""
    try:
        import unreal
        result = unreal.get_interpreter_executable_path()
    except:
        pass
    return result