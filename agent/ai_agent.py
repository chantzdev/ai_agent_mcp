import asyncio
# from pathlib import Path
from dotenv import load_dotenv
from langchain_core.messages import HumanMessage
from langchain_ollama import ChatOllama
from langchain_openai import ChatOpenAI
from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.prebuilt import create_react_agent
import httpx

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
all_tools_config = {
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

def filter_available_tools(config):
    available = {}
    for name, tool in config.items():
        try:
            url = tool["url"]
            
            r = httpx.head(url, timeout=2.0)
            if r.status_code < 500:
                available[name] = tool
            else:
                print(f"Tool '{name}' at {url} returned status {r.status_code}, skipping.")
        except Exception:
            print(f"Tool '{name}' at {tool['url']} is not available, skipping.")
    return available

mcp_config = filter_available_tools(all_tools_config)

async def main():
    try:
        if mcp_config:
            async with MultiServerMCPClient(mcp_config) as client:
                tools = client.get_tools()
                system_message = (
                    "You are an AI assistant with access to the following tools: {tools}. "
                    "Before executing any tool, you must ask the user for permission. "
                    "Prompt the user with a yes/no question in this format: "
                    "'Do you want me to execute the tool <tool_name>? (y/n)'. "
                    "Accept 'y', 'Y', 'n', or 'N' as valid responses. "
                    "If the user replies with 'y' or 'Y', proceed to execute the tool. "
                    "If the user replies with 'n' or 'N', do not execute the tool and continue the conversation. "
                    "If the user replies with anything else, repeat the question until a valid answer is given."
                )
                agent = create_react_agent(model, tools, prompt=system_message)
                print("Type your question (type '/exit' to quit):")
                history = []
                while True:
                    user_input = input("> ")
                    if user_input.strip().lower() == "/exit":
                        break
                    message = HumanMessage(content=user_input)
                    history.append(message)
                    try:
                        response = await agent.ainvoke({"messages": history})
                        answer = response["messages"][-1].content
                    except Exception as e:
                        answer = f"Error calling tool: {e}"
                    print(answer)
                    
                    history.append(HumanMessage(content=answer))
        else:
            print("No MCP tools are available. Running in LLM-only mode.")
            print("Type your question (type '/exit' to quit):")
            history = []
            while True:
                user_input = input("> ")
                if user_input.strip().lower() == "/exit":
                    break
                history.append(HumanMessage(content=user_input))
                try:
                    response = await model.ainvoke(history)
                    answer = response.content
                except Exception as e:
                    answer = f"Error: {e}"
                print(answer)
                history.append(HumanMessage(content=answer))
    except Exception as e:
        print(f"Could not start agent: {e}")

if __name__ == "__main__":
    asyncio.run(main())