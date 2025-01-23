# pip install -U autogen-agentchat autogen-ext[openai,web-surfer]
# playwright install

import asyncio
import autogen_agentchat as autogen
from autogen_agentchat.agents import AssistantAgent, UserProxyAgent
from autogen_agentchat.conditions import TextMentionTermination
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_agentchat.ui import Console
from autogen_ext.models.openai import OpenAIChatCompletionClient
from autogen_ext.agents.web_surfer import MultimodalWebSurfer
import os
import json

# In the Bash terminal, type this to set the OPENAI_API_KEY environment variable in your system 
# and let the library fetch it automatically:
# 
# export OPENAI_API_KEY="your_openai_api_key_here"


# Set OpenAI API key if not using environment variable
os.environ["OPENAI_API_KEY"] = "Your_OpenAI_API_Key_Here" 

# Load the configuration from the JSON file
OAI_CONFIG_LIST = "./config.json"
with open(OAI_CONFIG_LIST, "r") as f:
    config_list = json.load(f)

async def main():
    model_client = None
    try:
        model_client = OpenAIChatCompletionClient(model="gpt-4o-mini")
        assistant = AssistantAgent("assistant", model_client)
        web_surfer = MultimodalWebSurfer("web_surfer", model_client)
        user_proxy = UserProxyAgent("user_proxy")
        termination = TextMentionTermination("TERMINATE")
        team = RoundRobinGroupChat([web_surfer, assistant, user_proxy], termination_condition=termination)
        await Console(team.run_stream(task="Find information about AutoGen and write a short summary."))
    except Exception as e:
        print(f"Error: {e}")
    finally:
        # Properly close resources if needed
        if model_client:
            await model_client.close()  # Example of explicit cleanup

# Run the asyncio event loop
asyncio.run(main())
