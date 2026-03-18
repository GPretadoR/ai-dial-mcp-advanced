import asyncio
import json
import os

from agent.clients.custom_mcp_client import CustomMCPClient
from agent.clients.mcp_client import MCPClient
from agent.clients.dial_client import DialClient
from agent.models.message import Message, Role


async def main():
    # 1. Take a look what applies DialClient
    # DialClient integrates with OpenAI-compatible API and manages tool calls via MCP clients
    
    # 2. Create empty list where you save tools from MCP Servers later
    tools = []
    
    # 3. Create empty dict where where key is str (tool name) and value is instance of MCPClient or CustomMCPClient
    tool_name_client_map = {}
    
    # 4. Create UMS MCPClient, url is `http://localhost:8006/mcp` (use static method create and don't forget that its async)
    ums_client = await MCPClient.create("http://localhost:8006/mcp")
    
    # 5. Collect tools and dict [tool name, mcp client]
    ums_tools = await ums_client.get_tools()
    for tool in ums_tools:
        tools.append(tool)
        tool_name = tool["function"]["name"]
        tool_name_client_map[tool_name] = ums_client
    
    # 6. Do steps 4 and 5 for `https://remote.mcpservers.org/fetch/mcp`
    remote_client = await MCPClient.create("https://remote.mcpservers.org/fetch/mcp")
    remote_tools = await remote_client.get_tools()
    for tool in remote_tools:
        tools.append(tool)
        tool_name = tool["function"]["name"]
        tool_name_client_map[tool_name] = remote_client
    
    # 7. Create DialClient, endpoint is `https://ai-proxy.lab.epam.com`
    api_key = os.getenv("DIAL_API_KEY")
    if not api_key:
        raise ValueError("DIAL_API_KEY environment variable is required")
    
    dial_client = DialClient(
        api_key=api_key,
        endpoint="https://ai-proxy.lab.epam.com",
        tools=tools,
        tool_name_client_map=tool_name_client_map
    )
    
    # 8. Create array with Messages and add there System message with simple instructions for LLM that it should help to handle user request
    messages = [
        Message(
            role=Role.SYSTEM,
            content="You are a helpful AI assistant. Use the available tools to help users with their requests."
        )
    ]
    
    # 9. Create simple console chat (as we done in previous tasks)
    print("Chat started. Type 'exit' to quit.\n")
    
    while True:
        user_input = input("👤: ")
        
        if user_input.lower() in ["exit", "quit"]:
            print("Goodbye!")
            break
        
        messages.append(Message(role=Role.USER, content=user_input))
        
        ai_response = await dial_client.get_completion(messages)
        
        messages.append(ai_response)
        
        print()  # Add spacing between interactions

if __name__ == "__main__":
    asyncio.run(main())


# Check if Arkadiy Dobkin present as a user, if not then search info about him in the web and add him