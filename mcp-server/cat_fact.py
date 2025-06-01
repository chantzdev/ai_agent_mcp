import requests
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("Cat Facts MCP")


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
    print(get_cat_fact())
    mcp.run(transport="stdio")
