from mcp.client.session import ClientSession
from mcp.client.streamable_http import streamable_http_client
import asyncio
from contextlib import AsyncExitStack

URL = "http://localhost:8000/mcp"


async def main():
    async with streamable_http_client(URL) as (read_stream, write_stream, _):
        async with ClientSession(read_stream, write_stream) as client_session:
            await client_session.initialize()
            tools = await client_session.list_tools()
            print(tools)
    
    print("="*100)
    
    async with streamable_http_client(URL) as (read_stream, write_stream, _):
        async with ClientSession(read_stream, write_stream) as client_session:
            await client_session.initialize()
            tools = await client_session.call_tool("get_weather",{"city":"karachi"})
            print(tools)

asyncio.run(main())