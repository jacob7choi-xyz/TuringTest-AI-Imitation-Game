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

