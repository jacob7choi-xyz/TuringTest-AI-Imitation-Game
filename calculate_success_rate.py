import os
import json
import csv


def analyze_conversations(conversations_folder):
    success_tracker = {
        0.1: {0.1: 0, 0.5: 0, 0.9: 0},
        0.5: {0.1: 0, 0.5: 0, 0.9: 0},
        0.9: {0.1: 0, 0.5: 0, 0.9: 0}
    }

    print("\nAnalyzing conversations...")

    for filename in os.listdir(conversations_folder):
        if filename.endswith(".json"):
            print(f"\nFile: {filename}")
            with open(os.path.join(conversations_folder, filename), 'r') as f:
                data = json.load(f)
                for conv in data['conversations']:
                    int_temp = conv['temperatures']['interrogator'] 
                    agent_temp = conv['temperatures']['agent']
                    decision = conv['summary']['decision']
                    
                    print(f"Temps (Int, Agent): ({int_temp}, {agent_temp})")
                    print(f"Decision: {decision}")
                    
                    # Count correct AI identifications
                    if decision == 'AI':  # Success is when AI is correctly identified
                        success_tracker[int_temp][agent_temp] += 1

    for int_temp in success_tracker:
        for agent_temp in success_tracker[int_temp]:
            print(f"\nInt: {int_temp}, Agent: {agent_temp}")
            print(f"Successes: {success_tracker[int_temp][agent_temp]}/10")

    return success_tracker


def calculate_success_rate(success_tracker):
    success_rate = {}
    for interrogator_temp in success_tracker:
        success_rate[interrogator_temp] = {}
        for agent_temp in success_tracker[interrogator_temp]:
            total_conversations = 10  # Total conversations per combination
            successes = success_tracker[interrogator_temp][agent_temp]
            success_rate[interrogator_temp][agent_temp] = successes / total_conversations
    return success_rate


def write_success_rate_csv(success_rate):
    temperatures = [0.1, 0.5, 0.9]
    with open("success_rate_results.csv", "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        
        # Write header
        writer.writerow(['Interrogator Temp'] + temperatures)
        
        # Write data rows
        for int_temp in temperatures:
            row = [int_temp]
            for agent_temp in temperatures:
                row.append(f"{success_rate[int_temp][agent_temp]:.2f}")
            writer.writerow(row)

    print("Success rate CSV saved to success_rate_results.csv")


def main():
    # Path to your conversations folder
    conversations_folder = '/Users/jacobchoi/Desktop/Turing_Test/conversations/2025-01-29'

    # Analyze the conversations
    success_tracker = analyze_conversations(conversations_folder)

    # Calculate the success rate
    success_rate = calculate_success_rate(success_tracker)

    # Write the results to a CSV file
    write_success_rate_csv(success_rate)

if __name__ == "__main__":
    main()