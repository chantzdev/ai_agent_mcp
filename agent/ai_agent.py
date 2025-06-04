import asyncio
# from pathlib import Path
from dotenv import load_dotenv
from langchain_core.messages import HumanMessage
from langchain_ollama import ChatOllama
from langchain_openai import ChatOpenAI
from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.prebuilt import create_react_agent

load_dotenv()

#model = ChatOllama(model="qwen2.5:7b", temperature=0)
model = ChatOpenAI(model="gpt-4.1", temperature=0)
# local
# ROOT_FOLDER = Path(__file__).parent.parent.absolute()
# MCP_SERVER_PATH = str(ROOT_FOLDER / "mcp-server")

# mcp_config = {
#     "binance": {
#         "command": "python",
#         "args": [MCP_SERVER_PATH+"/binance.py"],
#         "transport": "stdio",
#     },
#     "cat-fact": {
#         "command": "python",
#         "args": [MCP_SERVER_PATH+"/cat_fact.py"],
#         "transport": "stdio",
#     },
#     "chuck-noris-joke": {
#         "command": "python",
#         "args": [MCP_SERVER_PATH+"/chuck_noris_joke.py"],
#         "transport": "stdio",
#     }
# }

# remote
mcp_config = {
    "binance": {
        "url": "http://localhost:8001/sse",
        "transport": "sse",
    },
    "cat-fact": {
        "url": "http://localhost:8002/sse",
        "transport": "sse",
    },
    "chuck-noris-joke": {
        "url": "http://localhost:8003/sse",
        "transport": "sse",
    }
}

async def chat():
    async with MultiServerMCPClient(mcp_config) as client:
        tools = client.get_tools()
        agent = create_react_agent(model, tools)
        print("Type your question (type '/exit' to quit):")
        history = []
        while True:
            user_input = input("> ")
            if user_input.strip().lower() == "/exit":
                break
            message = HumanMessage(content=user_input)
            history.append(message)
            response = await agent.ainvoke({"messages": history})
            answer = response["messages"][-1].content
            print(answer)
            # Add the agent's reply to history for context in the next turn
            history.append(response["messages"][-1])

if __name__ == "__main__":
    asyncio.run(chat())