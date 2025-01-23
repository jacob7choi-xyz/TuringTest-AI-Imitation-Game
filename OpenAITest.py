#DONE! This is a test file to test the OpenAI API. It is working fine.

import asyncio
from autogen_core import CancellationToken
from autogen_ext.models.openai import OpenAIChatCompletionClient
from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.messages import TextMessage


async def main() -> None:
    model_client = OpenAIChatCompletionClient(
        model="gpt-4o-mini",
        api_key = "YOUR_API_KEY"
    )
    agent = AssistantAgent(name="assistant", model_client=model_client)

    response = await agent.on_messages(
        [TextMessage(content="What is the capital of both Koreas?", source="user")], CancellationToken()
    )
    print(response)


asyncio.run(main())