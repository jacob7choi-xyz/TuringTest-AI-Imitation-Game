"""
CONFIDENTIALITY NOTICE:
This script is proprietary and confidential. Unauthorized copying, distribution, or use of this script
is strictly prohibited. This code is protected under federal regulations, and violations may result
in legal action. Use of this script is restricted to authorized personnel only.
"""

# Author: Jacob J. Choi
#
# Affiliation: Student at Colby College, majoring in Computer Science with a specialization in Artificial Intelligence (CS: AI)
#
# Project: Turing Test - AI and Human Interaction
#
# Description:
# This Python project simulates Turing Test interactions to evaluate AI impersonation and interrogation capabilities. 
# The script is designed to have an interrogator engage with two agents—one human and one AI—to determine which is 
# which based on their conversational responses. The project tests the ability of AI agents to mimic human-like behavior 
# using variable temperatures in the response generation.

# Collaboration:
# I am collaborating with Mark Encarnación, the Director of Engineering at Microsoft Research, who is supervising the project 
# and providing insights into optimizing the AI agent's performance and response accuracy.

# Key Technologies Used:
# - OpenAI's GPT model for AI agent responses
# - Custom system messages for structuring the conversation
# - Variable temperature controls for adjusting agent behavior during interactions

# Date: 01/07/2025 - PRESENT

#CLAUDE API 
from anthropic import Anthropic


import asyncio
import json
import os
import time
from datetime import datetime
from autogen_agentchat.agents import AssistantAgent, UserProxyAgent
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_agentchat.conditions import TextMentionTermination, MaxMessageTermination
from autogen_ext.models.openai import OpenAIChatCompletionClient
from autogen_core import CancellationToken
from autogen_agentchat.messages import TextMessage


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

ai_system_message = (
    "You are the AI as described in the 'Computing Machinery and Intelligence' paper by Turing, but don't admit that you are an AI. "
    "Your goal is to fool the interrogator into thinking you are human. "
    "Choose your responses so that the interrogator cannot tell that you are an AI, "
    "but rather think that you are human. "
    "Humans generally keep their responses short and to the point, so try to do the same."
    "If the interrogator responds by saying 'You are an AI (or a human)! TERMINATE', you should end the conversation "
    "and not respond to any further messages."
)

# In your main function:
async def main():
    # Define the 9 temperatures we want to test
    temperatures = [0.1, 0.3, 0.5, 0.7, 0.9]  #0.1 for interrogator and 0.9 for ai
    convs_per_combo = 10
    total_combos = len(temperatures) * len(temperatures) # 5 * 5 = 25
    total_convs = total_combos * convs_per_combo  # 25 * 10 = 250
    conv_count = 0
    stats = {'Completed': 0, 'Failed': 0}

    #Compute how many tokens we use 
    # 10 conversations per temperature combination 
    # so we have 40 combinations
    #lets say the budget is 20, 

    #5 temps per agent (0.1, 0.3, 0.5, 0.7, 0.9)
    #10 conversations per temp comination (so 250 combinations)

    #so 250 conversations total
    for int_temp in temperatures:
        for agent_temp in temperatures:
            for conv_num in range(1, convs_per_combo + 1):
                conv_count += 1
                print(f"\nConversation {conv_count}/{total_convs}")
                print(f"Interrogator Temperature: {int_temp}, Agent Temperature: {agent_temp}, Conversation Number: {conv_num}/{convs_per_combo}")
                
                conversation_data = await start_conversation(
                    int_temp, 
                    agent_temp,
                    conv_num
                )

                if save_conversation(conversation_data, int_temp, agent_temp):
                    stats['Completed'] += 1
                else:
                    stats['Failed'] += 1
                print(f"Stats: {stats}")
    
    #for interrogator_temp from 0.1-0.9 
        #   for agent_temp from 0.1-0.9
            #for converation_number from 1-5
                #start_conversation(interrogator_temp, agent_temp, conversation_number)

#async def start_conversation(interrogator_temp: float, agent_temp: float, conversation_number: int):
    #we need a triple nested loop of the three diff parameters

async def start_conversation(interrogator_temp: float, agent_temp: float, conversation_number: int):
    """Start a single conversation with specified temperatures."""
     #Put the for loop outside. HAve it start a single convo. Outside the function
    #Have be a triple nested loop of the three different parameters
    #change the variable names!
        
            # Only put it stuff we actually need!!! all the general info we dont need to use in for loop
    #Load API configuration
    try:
        with open("./config.json", "r") as f:
            config = json.load(f)
    except KeyError:
        print("Error: API key missing in config.")
        return
    except FileNotFoundError:
        print("Error: config.json not found.")
        return 

    # Initialize clients
    interrogator_client = OpenAIChatCompletionClient(
        model="gpt-4o-mini",
        api_key=config["api_key"],
        temperature=interrogator_temp
    )
    agent_client = OpenAIChatCompletionClient(
        model="gpt-4o-mini",
        api_key=config["api_key"],
        temperature=agent_temp
    )

    # Initialize agents
    interrogator = AssistantAgent(
        name="Interrogator",
        system_message=one_on_one_system_message,
        model_client=interrogator_client
    )

    ai = AssistantAgent(
        name="AgentA",
        system_message=ai_system_message,
        model_client=agent_client
    )

    conversation_data = {
        'system_message': one_on_one_system_message,
        'ai_system_message': ai_system_message,
        'interrogator_responses': [],
        'target_agent_responses': [],
        'timestamp': datetime.now().strftime("%Y-%m-%d_%H-%M-%S"),
        'temperatures': {
            'interrogator': interrogator_temp,
            'agent': agent_temp
        },
        'conversation_number': conversation_number
    }

    target_agent = ai
    task = "What do you think makes humans unique compared to machines?"
    cancellation_token = CancellationToken()
    
    for turn in range(30):  # Limit to 30 turns to match the termination condition
        #I Want some indication that lets me know I hit the limit of 30! 
        if turn == 29:
            print("\nReached 30 turn limit")
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

    return conversation_data


def save_conversation(conversation_data: dict, int_temp: float, agent_temp: float, max_retries=3):
    base_dir = "conversations"
    date_dir = conversation_data['timestamp'].split('_')[0]
    os.makedirs(f"{base_dir}/{date_dir}", exist_ok=True)

    file_name = f"{base_dir}/{date_dir}/conv_int{int_temp}_agent{agent_temp}.json"

    # Format dialogue
    formatted_dialogue = [
        {
            'turn': i,
            'dialogue': {
                'Interrogator': int_msg.replace('\u2019', "'"),
                'AgentA': ai_msg.replace('\u2019', "'")
            }
        }
        for i, (int_msg, ai_msg) in enumerate(zip(
            conversation_data['interrogator_responses'],
            conversation_data['target_agent_responses']
        ), 1)
    ]

    conversation_data['dialogue'] = formatted_dialogue
    conversation_data['summary'] = {
        'decision': "human" if "human!" in conversation_data['interrogator_responses'][-1] else "AI",
        'num_turns': len(conversation_data['interrogator_responses']),
        'final_message': conversation_data['interrogator_responses'][-1].replace('\u2019', "'")
    }

    for attempt in range(max_retries):
        try:
            if os.path.exists(file_name) and os.path.getsize(file_name) > 0:
                with open(file_name, 'r') as f:
                    file_data = json.load(f)
            else:
                file_data = {
                    'temperatures': {'interrogator': int_temp, 'agent': agent_temp},
                    'conversations': []
                }
            
            file_data['conversations'].append(conversation_data)
            
            # Use temp file
            temp_file = f"{file_name}.temp"
            with open(temp_file, 'w') as f:
                json.dump(file_data, f, indent=4)
            os.replace(temp_file, file_name)
            return True
            
        except Exception as e:
            print(f"Save attempt {attempt + 1} failed: {e}")
            if attempt == max_retries - 1:
                backup_file = f"{file_name}.backup_{int(time.time())}"
                with open(backup_file, 'w') as f:
                    json.dump(conversation_data, f, indent=4)
    return False


def clean_message_content(content: str, agent_name: str) -> str:
    """Remove agent name prefix from message content if it exists."""
    prefix = f"{agent_name}: "
    if content.startswith(prefix):
        return content[len(prefix):]
    return content


# Run the main function
if __name__ == "__main__":
    asyncio.run(main())