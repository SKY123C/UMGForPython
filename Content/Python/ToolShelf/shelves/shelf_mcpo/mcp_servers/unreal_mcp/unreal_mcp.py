from mcp.server.fastmcp import FastMCP
from mcp.types import CallToolResult, TextContent
# Initialize FastMCP server
mcp = FastMCP("unreal_python")


@mcp.tool()
async def exec_python(code :str) -> CallToolResult:
    '''
    exec python command in unreal
    Returns:
        str: if success, return 'success or nothing, else return error message
    '''
    import remote_execution
    remote_exec = remote_execution.RemoteExecution()
    remote_exec.start()
    result = None

    while True:
        if not remote_exec.remote_nodes:
            continue
        remote_exec.remote_nodes[0]
        remote_exec.open_command_connection(remote_exec.remote_nodes[0]['node_id'])
        if remote_exec.has_command_connection():
            command = code
            output_res = remote_exec.run_command(command, exec_mode=remote_execution.MODE_EXEC_FILE)
            is_success = output_res.get("success")
            error_message = output_res.get('result')
            with open('output.txt', 'w', encoding="utf-8") as f:
                f.write(str(output_res))
            
            if is_success:
                result = CallToolResult(
                    isError= False,
                    content=[
                        TextContent(
                            type="text",
                            text="success"
                        ),
                        TextContent(
                            type="text",
                            text=output_res.get("output")
                        )

                    ])
            else:
                result = CallToolResult(
                    isError= True,
                    content=[
                        TextContent(
                            type="text",
                            text="error," + error_message
                        )
                    ])
        break
    return result

if __name__ == "__main__":
    # Initialize and run the server
    mcp.run(transport='stdio')