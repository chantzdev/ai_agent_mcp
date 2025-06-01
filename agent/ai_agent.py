import asyncio
from pathlib import Path
from dotenv import load_dotenv
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_ollama import ChatOllama
from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.prebuilt import create_react_agent

load_dotenv()

model = ChatOllama(model="qwen2.5:7b", temperature=0)
ROOT_FOLDER = Path(__file__).parent.parent.absolute()
MCP_SERVER_PATH = str(ROOT_FOLDER / "mcp-server")

mcp_config = {
    "binance": {
        "command": "python",
        "args": [MCP_SERVER_PATH+"/binance.py"],
        "transport": "stdio",
    },
    "cat-fact": {
        "command": "python",
        "args": [MCP_SERVER_PATH+"/cat_fact.py"],
        "transport": "stdio",
    },
    "chuck-noris-joke": {
        "command": "python",
        "args": [MCP_SERVER_PATH+"/chuck_noris_joke.py"],
        "transport": "stdio",
    }
}

async def chat():
    async with MultiServerMCPClient(mcp_config) as client:
        tools = client.get_tools()
        agent = create_react_agent(model, tools)
        print("Type your question (type '/exit' to quit):")
        while True:
            user_input = input("> ")
            if user_input.strip().lower() == "/exit":
                break
            message = HumanMessage(content=user_input)
            response = await agent.ainvoke({"messages": [message]})
            answer = response["messages"][-1].content
            print(answer)

if __name__ == "__main__":
    asyncio.run(chat())