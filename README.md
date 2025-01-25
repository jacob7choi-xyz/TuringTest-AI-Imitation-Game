# Turing Test Simulation: AI and Human Interaction

## Author: Jacob Choi

### Affiliation: Student at Colby College, majoring in Computer Science with a specialization in Artificial Intelligence (CS: AI)

### Project Overview
This Python project conducts Turing Test simulations designed to evaluate AI's ability to impersonate human-like behavior and the interrogator's ability to identify the AI. The project involves two agents in a simulated conversation: one human and one AI. The goal is to determine which is human and which is AI based on their responses, testing the AI's conversational capabilities under different settings.

The project leverages OpenAI's GPT model to generate responses from the AI agent and simulates interrogations where the AI must convince the interrogator that it is human. The interrogation process is controlled by adjusting the temperature of the model's responses, providing variations in the conversational style and complexity.

### Key Features
- **Two Agent System**: One agent is human and the other is AI. The AI mimics human behavior during the conversation.
- **Temperature Controls**: The conversation is influenced by the "temperature" setting, which adjusts the randomness of the AI's responses, allowing different styles of interaction.
- **Multiple Conversations**: The script allows running multiple conversations with varying interrogator and AI temperatures to assess performance across scenarios.
- **Data Logging**: All conversations are logged, and the results are stored in JSON format for later analysis.

### Collaboration
This project is developed in collaboration with **Mark Encarnación**, Director of Engineering at Microsoft Research. Mark is providing guidance on optimizing the AI agent's performance and ensuring its conversational responses align more closely with human-like behavior.

### Installation
To run this project locally, you'll need Python 3.7+ and the following dependencies:

1. Clone the repository:
    ```bash
    git clone https://github.com/jacob7choi-xyz/TuringTest-AI-Imitation-Game.git
    cd TuringTest-AI-Imitation-Game
    ```

2. Install required dependencies:
    ```bash
    pip install -r requirements.txt
    ```

    *Note: Make sure you have access to the necessary API keys for using OpenAI's GPT model.*

3. Create a `config.json` file in the project root directory with the following structure:

    ```json
    {
        "api_key": "your-openai-api-key"
    }
    ```

### How to Run
Once the dependencies are installed and the configuration file is set up, you can run the Turing Test simulation using the following command:

```bash
python turingtest.py
