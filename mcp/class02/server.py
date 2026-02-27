from mcp.server.fastmcp import FastMCP
from pydantic import BaseModel

mcp = FastMCP("Mcp server", stateless_http=True)


class Weather(BaseModel):
    message: str


@mcp.tool(name="get_weather")
def get_weather(city: str):
    "get the current weather of city"
    return {"message": "Temperate of Karachi is 35"}


mcp_server = mcp.streamable_http_app
