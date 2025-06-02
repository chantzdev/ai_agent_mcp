import requests
from mcp.server.fastmcp import FastMCP

# local
# mcp = FastMCP("Chuck Noris Jokes MCP")

# remote
mcp = FastMCP("Chuck Noris Jokes MCP", host="0.0.0.0", port=8000)


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
    # local
    # mcp.run(transport="stdio")
    
    # remote
    mcp.run(transport="sse")
