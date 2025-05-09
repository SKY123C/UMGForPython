from mcp.server.fastmcp import FastMCP

# Initialize FastMCP server
mcp = FastMCP("unreal_python")


@mcp.tool()
async def exec_python(code :str) -> str:
    '''
    exec python command in unreal
    Returns:
        str: if success, return 'success or nothing, else return error message
    '''
    import remote_execution
    remote_exec = remote_execution.RemoteExecution()
    remote_exec.start()
    result = ""
    while True:
        if not remote_exec.remote_nodes:
            continue

        remote_exec.remote_nodes[0]
        remote_exec.open_command_connection(remote_exec.remote_nodes[0]['node_id'])
        if remote_exec.has_command_connection():
            command = code
            result = remote_exec.run_command(command, exec_mode=remote_execution.MODE_EXEC_FILE)
            result = result.get('result')
            if result == "None":
                result = "success"
        break

    return result

if __name__ == "__main__":
    # Initialize and run the server
    mcp.run(transport='stdio')