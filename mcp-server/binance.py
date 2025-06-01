from typing import Any

import requests
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("Binance MCP")

SYMBOL_MAP = {
    "bitcoin": "BTCUSDT",
    "btc": "BTCUSDT",
    "ethereum": "ETHUSDT",
    "eth": "ETHUSDT",
    "bnb": "BNBUSDT",
    "solana": "SOLUSDT",
    "sol": "SOLUSDT",
}

@mcp.tool()
def get_price(symbol: str) -> Any:
    """
    Get the latest price for a cryptocurrency from Binance.

    This tool accepts either a common name (like "bitcoin" or "ethereum") or a Binance trading symbol (like "BTCUSDT" or "ETHUSDT").
    It returns the most recent price for the specified cryptocurrency in USDT.

    Args:
        symbol (str): The name or symbol of the cryptocurrency (e.g., "bitcoin", "btc", "BTCUSDT").

    Returns:
        dict: A dictionary containing the symbol and its latest price, for example: {"symbol": "BTCUSDT", "price": "68000.00"}
    """
    symbol_upper = symbol.lower()
    binance_symbol = SYMBOL_MAP.get(symbol_upper, symbol.upper())
    url = f"https://api.binance.com/api/v3/ticker/price?symbol={binance_symbol}"
    response = requests.get(url)
    response.raise_for_status()
    return response.json()


if __name__ == "__main__":
    mcp.run(transport="stdio")
