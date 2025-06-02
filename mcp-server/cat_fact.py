import requests
from mcp.server.fastmcp import FastMCP

# local
# mcp = FastMCP("Cat Facts MCP")

# remote
mcp = FastMCP("Cat Facts MCP", host="0.0.0.0", port=8000)


@mcp.tool()
def get_cat_fact() -> str:
    """
    Get random cat fact
    Returns:
        str: A random cat fact
    """
    url = "https://catfact.ninja/fact"
    response = requests.get(url)
    response.raise_for_status()
    return response.json()["fact"]

if __name__ == "__main__":
    # local
    # cp.run(transport="stdio")
    
    # remote
    mcp.run(transport="sse")
