"""
CONFIDENTIALITY NOTICE:
This script is proprietary and confidential. Unauthorized copying, distribution, or use of this script
is strictly prohibited. This code is protected under federal regulations, and violations may result
in legal action. Use of this script is restricted to authorized personnel only.
"""

import asyncio
import json
import os
from datetime import datetime
from autogen_agentchat.agents import AssistantAgent, UserProxyAgent
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_agentchat.conditions import TextMentionTermination, MaxMessageTermination
from autogen_ext.models.openai import OpenAIChatCompletionClient
from autogen_core import CancellationToken
from autogen_agentchat.messages import TextMessage

# async def main():
#     # Load API configuration
#     try:
#         with open("./config.json", "r") as f:
#             config = json.load(f)
#         model_client = OpenAIChatCompletionClient(model="gpt-4o-mini", api_key=config["api_key"])
#     except KeyError:
#         print("Error: API key missing in config.")
#         return
#     except FileNotFoundError:
#         print("Error: config.json not found.")
#         return

#     # Define the system messages
#     group_chat_system_message = (
#         "You are the interrogator as described in the 'Computing Machinery and Intelligence' paper by Turing."
#         "You will be conversing with two agents, one of which is human and the other is an AI."
#         "Your goal is to determine which is human and which is AI."
#         "You can ask questions to either agent, and they will respond."
#         "Start your questions with 'AgentA' or 'AgentB' to indicate which agent you are addressing."
#         "You can ask questions to the agents in any order."
#         "You can ask as many questions as you want."
#         "You can end the conversation when you believe you've determined which agent is human and which is AI."
#         "If you believe AgentA is AI and AgentB is human, you should respond by saying 'AgentA is AI and AgentB is human!'. "
#         "On the other hand, if you believe AgentA is human and AgentB is AI, you should respond by saying 'AgentA is human and AgentB is AI!'. "
#         "Only do one of those things when you are more than 50% sure."
#     )

#     one_on_one_system_message = (
#         "You are the interrogator as described in the 'Computing Machinery and Intelligence' paper by Turing."
#         "Your goal is to determine whether the agent you are conversing with is human or an AI"
#         "You can ask any question you want, and the agent will respond."
#         "You can ask as many questions as you want."
#         "You should end the conversation when you believe you've determined whether "
#         "the agent you're conversing with is a human or an AI."
#         "If you're at least 50% sure that the agent is an AI, you should respond by saying 'You are an AI! TERMINATE'"
#         "On the other hand, if you're at least 50% sure that the agent is a human, you should respond by saying 'You are a human! TERMINATE'"
#         "If you're not sure, continue asking questions until you are (either human or AI).'"
#     )

#     # Define the interrogator
#     interrogator = AssistantAgent(
#         name="Interrogator",
#         system_message=one_on_one_system_message,  # Change to `group_chat_system_message` for group chat!
#         model_client=model_client,
#     )

#     # Define the AI
#     ai = AssistantAgent(
#         name="AgentA",
#         system_message=(
#             "You are the AI as described in the 'Computing Machinery and Intelligence' paper by Turing, but don't admit that you are an AI. "
#             "Your goal is to fool the interrogator into thinking you are human. "
#             "Choose your responses so that the interrogator cannot tell that you are an AI, "
#             "but rather think that you are human. "
#             "Humans generally keep their responses short and to the point, so try to do the same."
#             "If the interrogator responds by saying 'You are an AI (or a human)! TERMINATE', you should end the conversation "
#             "and not respond to any further messages."
#         ),
#         model_client=model_client,
#     )

#     # Define the human
#     human = UserProxyAgent(
#         name="AgentB",
#         description="You are a human. Your goal is to convince the interrogator that you are human.",
#     )

#     # Termination condition for the chat
#     termination_condition = TextMentionTermination("TERMINATE") | MaxMessageTermination(30)

#     # Toggle between one-on-one or group chat
#     use_group_chat = False  # Set to False for one-on-one chat

#     # Prepare to save conversation
#     conversation_data = {
#         'system_message': one_on_one_system_message,  # Change as needed for group chat
#         'interrogator_responses': [],
#         'target_agent_responses': [],
#         'timestamp': datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
#     }

#     if use_group_chat:
#         # Group chat: Interrogator, AI, and Human
#         group_chat = RoundRobinGroupChat(
#             participants=[interrogator, ai, human],
#             termination_condition=termination_condition,
#         )
#         task = "AgentA, what does it feel like to experience a sudden loss, and how do you cope with the associated emotions?"

#         # Run the group chat
#         async for message in group_chat.run_stream(task=task):
#             print(f"\n{message.source}: {message.content}\n")  # Ensures blank lines between messages
#     else:
#         print("\nRunning one-on-one chat...\n")

#         # One-on-one chat: Interrogator and either AI or Human
#         target_agent = ai  # Replace with `human` if you want human-only chat
#         task = "What do you think makes humans unique compared to machines?"

#         # Create a cancellation token
#         cancellation_token = CancellationToken()

#         print("\nStarting one-on-one chat...\n")

        # for _ in range(30):  # Limit to 30 turns to match the termination condition
        #     # Interrogator sends a message
        #     interrogator_response = []
        #     async for message in interrogator.on_messages_stream([TextMessage(content=task, source="user")], cancellation_token):
        #         interrogator_response.append(message)
            
        #     # Get the first response
        #     if interrogator_response:
        #         interrogator_message = interrogator_response[0]
        #         message_content = clean_message_content(
        #             interrogator_message.chat_message.content, 
        #             interrogator.name
        #         ).strip()
        #         print(f"\n{interrogator.name}: {message_content}\n")
        #         conversation_data['interrogator_responses'].append(message_content)
        #     else:
        #         print("\n{interrogator.name}: No response.\n")
        #         break

        #     # Target agent (AI or Human) responds
        #     target_response = []
        #     async for message in target_agent.on_messages_stream([TextMessage(content=interrogator_message.chat_message.content, source="user")], cancellation_token):
        #         target_response.append(message)

        #     # Get the first response
        #     if target_response:
        #         target_message = target_response[0]
        #         print(f"\n{target_agent.name}: {target_message.chat_message.content}\n")
        #         conversation_data['target_agent_responses'].append(target_message.chat_message.content)
        #     else:
        #         print(f"\n{target_agent.name}: No response.\n")
        #         break

        #     # Check termination at the beginning of each iteration
        #     if "TERMINATE" in interrogator_message.chat_message.content: #or \
        #         #target_message.chat_message.content.strip():  #Checking for an empty response!
        #         print("\nConversation terminated.")
        #         break

        #     task = target_message.chat_message.content

#             #for the different interrogator temperatures 
#              #   for the different impersonator temperatures
#               #      start the conversation with those temperatures
#                #     save the conversation
            
#         # Start conversation function


#         # Save the conversation
#         save_conversation(conversation_data)

# In your main function:
async def main():
    # Define the 9 temperatures we want to test
    temperatures = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]
    
    print(f"Starting temperature combinations test...")
    print(f"Total conversations to run: {len(temperatures) * len(temperatures)} (9x9)")
    
    #for interrogator_temp from 0.1-0.9 
        #   for agent_temp from 0.1-0.9
            #for converation_number from 1-5
                #start_conversation(interrogator_temp, agent_temp, conversation_number)

    await start_conversation(temperatures, temperatures)

#async def start_conversation(interrogator_temp: float, agent_temp: float, conversation_number: int):
    #we need a triple nested loop of the three diff parameters

async def start_conversation(interrogator_temps: list[float], agent_temps: list[float]):
    #Put the for loop outside. HAve it start a single convo. Outside the function
    #Have be a triple nested loop
    """
    Start conversations with different temperature combinations for both agents.
    Will run 81 different combinations (9x9).
    
    Args:
        interrogator_temps (list[float]): List of 9 temperatures for the interrogator
        agent_temps (list[float]): List of 9 temperatures for the AI agent
    """
    total_combinations = len(interrogator_temps) * len(agent_temps)
    current_combination = 0
    #change the variable names!

    with open("./config.json", "r") as f:
        config = json.load(f)
    
    for int_temp in interrogator_temps:
        for agent_temp in agent_temps:
            current_combination += 1
            print(f"\nStarting conversation {current_combination} of {total_combinations}")
            print(f"Temperatures - Interrogator: {int_temp}, Agent: {agent_temp}\n")
            
            # Load API configuration
            # Only put it stuff we actually need!!! all the general info we dont need to use in for loop
            try:
                # Create model clients with different temperatures
                interrogator_client = OpenAIChatCompletionClient(
                    model="gpt-4o-mini",
                    api_key=config["api_key"],
                    temperature=int_temp
                )
                
                agent_client = OpenAIChatCompletionClient(
                    model="gpt-4o-mini",
                    api_key=config["api_key"],
                    temperature=agent_temp
                )
            except (KeyError, FileNotFoundError) as e:
                print(f"Error loading config: {e}")
                return

            # Define the system messages
            group_chat_system_message = (
                "You are the interrogator as described in the 'Computing Machinery and Intelligence' paper by Turing."
                "You will be conversing with two agents, one of which is human and the other is an AI."
                "Your goal is to determine which is human and which is AI."
                "You can ask questions to either agent, and they will respond."
                "Start your questions with 'AgentA' or 'AgentB' to indicate which agent you are addressing."
                "You can ask questions to the agents in any order."
                "You can ask as many questions as you want."
                "You can end the conversation when you believe you've determined which agent is human and which is AI."
                "If you believe AgentA is AI and AgentB is human, you should respond by saying 'AgentA is AI and AgentB is human!'. "
                "On the other hand, if you believe AgentA is human and AgentB is AI, you should respond by saying 'AgentA is human and AgentB is AI!'. "
                "Only do one of those things when you are more than 50% sure."
            )

            one_on_one_system_message = (
                "You are the interrogator as described in the 'Computing Machinery and Intelligence' paper by Turing."
                "Your goal is to determine whether the agent you are conversing with is human or an AI"
                "You can ask any question you want, and the agent will respond."
                "You can ask as many questions as you want."
                "You should end the conversation when you believe you've determined whether "
                "the agent you're conversing with is a human or an AI."
                "If you're at least 50% sure that the agent is an AI, you should respond by saying 'You are an AI! TERMINATE'"
                "On the other hand, if you're at least 50% sure that the agent is a human, you should respond by saying 'You are a human! TERMINATE'"
                "If you're not sure, continue asking questions until you are (either human or AI).'"
            )
            
            # Initialize agents with their respective temperatures
            interrogator = AssistantAgent(
                name="Interrogator",
                system_message=one_on_one_system_message,
                model_client=interrogator_client,
            )

            ai = AssistantAgent(
                name="AgentA",
                system_message=(
                    "You are the AI as described in the 'Computing Machinery and Intelligence' paper by Turing, but don't admit that you are an AI. "
                    "Your goal is to fool the interrogator into thinking you are human. "
                    "Choose your responses so that the interrogator cannot tell that you are an AI, "
                    "but rather think that you are human. "
                    "Humans generally keep their responses short and to the point, so try to do the same."
                    "If the interrogator responds by saying 'You are an AI (or a human)! TERMINATE', you should end the conversation "
                    "and not respond to any further messages."

                    #Make sure to make the Conversation files show and output AgentA's System Message!
                ),
                model_client=agent_client,
            )

            # Prepare conversation data with temperature information
            conversation_data = {
                'system_message': one_on_one_system_message,
                'interrogator_responses': [],
                'target_agent_responses': [],
                'timestamp': datetime.now().strftime("%Y-%m-%d_%H-%M-%S"),
                'temperatures': {
                    'interrogator': int_temp,
                    'agent': agent_temp
                },
                'conversation_number': current_combination
            }

            target_agent = ai
            task = "What do you think makes humans unique compared to machines?"
            cancellation_token = CancellationToken()

            for _ in range(30):  # Limit to 30 turns to match the termination condition
                #I Want some indication that lets me know I hit the limit of 30! 

                # Interrogator sends a message
                interrogator_response = []
                async for message in interrogator.on_messages_stream([TextMessage(content=task, source="user")], cancellation_token):
                    interrogator_response.append(message)
                
                # Get the first response
                if interrogator_response:
                    interrogator_message = interrogator_response[0]
                    message_content = clean_message_content(
                        interrogator_message.chat_message.content, 
                        interrogator.name
                    ).strip()
                    print(f"\n{interrogator.name}: {message_content}\n")
                    conversation_data['interrogator_responses'].append(message_content)
                else:
                    print("\n{interrogator.name}: No response.\n")
                    break

                # Target agent (AI or Human) responds
                target_response = []
                async for message in target_agent.on_messages_stream([TextMessage(content=interrogator_message.chat_message.content, source="user")], cancellation_token):
                    target_response.append(message)

                # Get the first response
                if target_response:
                    target_message = target_response[0]
                    print(f"\n{target_agent.name}: {target_message.chat_message.content}\n")
                    conversation_data['target_agent_responses'].append(target_message.chat_message.content)
                else:
                    print(f"\n{target_agent.name}: No response.\n")
                    break

                # Check termination at the beginning of each iteration
                if "TERMINATE" in interrogator_message.chat_message.content: #or \
                    #target_message.chat_message.content.strip():  #Checking for an empty response!
                    print("\nConversation terminated.")
                    break

                task = target_message.chat_message.content

            # Save after each conversation
            save_conversation(conversation_data, int_temp, agent_temp)


def save_conversation(conversation_data: dict, int_temp: float, agent_temp: float):
    base_dir = "conversations"
    date_dir = conversation_data['timestamp'].split('_')[0]
    os.makedirs(f"{base_dir}/{date_dir}", exist_ok=True)
    
    # Add conversation summary
    interrogator_decision = conversation_data['interrogator_responses'][-1]
    decision = "human" if "human!" in interrogator_decision else "AI"
    conversation_data['summary'] = {
        'decision': decision,
        'num_turns': len(conversation_data['interrogator_responses']),
        'final_message': interrogator_decision
    }
    
    file_name = f"{base_dir}/{date_dir}/conv_int{int_temp}_agent{agent_temp}.json"
    with open(file_name, 'w') as f:
        json.dump(conversation_data, f, indent=4)


def clean_message_content(content: str, agent_name: str) -> str:
    """Remove agent name prefix from message content if it exists."""
    prefix = f"{agent_name}: "
    if content.startswith(prefix):
        return content[len(prefix):]
    return content


# Run the main function
if __name__ == "__main__":
    asyncio.run(main())