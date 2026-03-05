from fastmcp import Client
import asyncio
from fastmcp.client.transports import StdioTransport

URL = "http://localhost:8000/mcp"

transport = StdioTransport(command="python",args=["server.py"])

async def main():
    async with Client(transport) as client:
        # tools = await client.list_tools()
        # print(tools)

        # resource = await client.list_resources()
        # print(resource)
        # print("="*100)
        # resource_template = await client.list_resource_templates()
        # print(resource_template)
        # resource_read = await client.read_resource("docs://document/plan.md")
        # print(resource_read[0].text)

        # prompt= await client.list_prompts()
        # print(prompt)

        prompt_get = await client.get_prompt("format", {"doc_id": "spec.txt"})
        print(prompt_get)


asyncio.run(main())
