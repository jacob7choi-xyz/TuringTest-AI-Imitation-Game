from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_agentchat.ui import Console
from autogen_ext.models.openai import OpenAIChatCompletionClient
import asyncio


# Define a tool
async def get_weather(city: str) -> str:
    return f"The weather in {city} is 73 degrees and Sunny."


async def main() -> None:
    # Define an agent
    weather_agent = AssistantAgent(
        name="weather_agent",
        model_client=OpenAIChatCompletionClient(
            model="gpt-4o-mini",
            api_key="Your_OpenAI_API_Key_Here",
        ),
        tools=[get_weather],
    )

    # Define a team with a single agent and maximum auto-gen turns of 1.
    agent_team = RoundRobinGroupChat([weather_agent], max_turns=1)

    while True:
        try:
            # Get user input from the console.
            user_input = input("Enter a message (type 'exit' to leave'): ")
            if user_input.strip().lower() == "exit":
                print("Exiting...")
                break

            # Run the team and stream messages to the console.
            stream = agent_team.run_stream(task=user_input)
            await Console(stream)

        except EOFError:
            print("\nDetected EOF (Ctrl+D or unexpected input). Exiting gracefully...")
            break

# NOTE: if running this inside a Python script you'll need to use asyncio.run(main()).
asyncio.run(main())