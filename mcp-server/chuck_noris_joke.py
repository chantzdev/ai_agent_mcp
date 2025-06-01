import requests
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("Chuck Noris Jokes MCP")


@mcp.tool()
def get_chuck_noris_joke() -> str:
    """
    Get random chuck noris joke
    Returns:
        str: A chuck noris joke
    """
    url = "https://api.chucknorris.io/jokes/random"
    response = requests.get(url)
    response.raise_for_status()
    return response.json()["value"]

if __name__ == "__main__":
    print(get_chuck_noris_joke())
    mcp.run(transport="stdio")
