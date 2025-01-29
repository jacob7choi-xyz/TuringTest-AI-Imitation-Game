import os
import json
import pandas as pd

def calculate_success_rate(conversations_dir: str):
    """
    Calculate the success rate of the interrogator correctly identifying the AI for each temperature combination.
    The success rate is based on the interrogator's final decision in the conversation.
    """
    # Initialize a 3x3 table for success rates
    temperatures = [0.1, 0.5, 0.9]
    success_matrix = { (int_temp, agent_temp): 0 for int_temp in temperatures for agent_temp in temperatures}
    total_matrix = { (int_temp, agent_temp): 0 for int_temp in temperatures for agent_temp in temperatures}
    
    # Iterate through the files in the provided conversations directory
    for file_name in os.listdir(conversations_dir):
        if file_name.endswith('.json'):
            file_path = os.path.join(conversations_dir, file_name)
            
            with open(file_path, 'r') as f:
                data = json.load(f)
                for conversation in data.get('conversations', []):
                    int_temp = conversation['temperatures']['interrogator']
                    agent_temp = conversation['temperatures']['agent']
                    decision = conversation['summary']['decision']
                    
                    # Update total count for the combination
                    total_matrix[(int_temp, agent_temp)] += 1
                    
                    # Check if the interrogator's final decision was correct
                    if (decision == "human" and "human!" in conversation['interrogator_responses'][-1]) or \
                       (decision == "AI" and "AI!" in conversation['interrogator_responses'][-1]):
                        # Increment the success count for this temperature combination
                        success_matrix[(int_temp, agent_temp)] += 1

    # Calculate the success rate and store it in a new matrix
    success_rate_matrix = {}
    for key in success_matrix:
        success_rate_matrix[key] = success_matrix[key] / total_matrix[key] if total_matrix[key] > 0 else 0

    # Convert the success rate matrix into a 3x3 DataFrame
    success_df = pd.DataFrame(index=temperatures, columns=temperatures, dtype=float)

    for int_temp in temperatures:
        for agent_temp in temperatures:
            success_df.at[int_temp, agent_temp] = success_rate_matrix[(int_temp, agent_temp)]

    return success_df

def save_success_rate_to_csv(success_df: pd.DataFrame, output_file: str):
    """
    Save the success rate DataFrame to a CSV file.
    """
    success_df.to_csv(output_file, index_label="Interrogator Temperature", header=success_df.columns.tolist())
    print(f"Success rates saved to {output_file}")

# Example usage:
def main():
    # Set the directory for the 2025-01-28 folder
    conversations_dir = "conversations/2025-01-28"
    output_file = "success_rate.csv"
    
    # Calculate the success rate matrix
    success_df = calculate_success_rate(conversations_dir)
    
    # Save the result to a CSV file
    save_success_rate_to_csv(success_df, output_file)

if __name__ == "__main__":
    main()
