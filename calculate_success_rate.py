import os
import json
import csv


def analyze_conversations(conversations_folder, int_temp, agent_temp):
    success_tracker = {
        int_temp: {agent_temp: 0}
    }

    print(f"\nAnalyzing conversations for Int: {int_temp}, Agent: {agent_temp}...")

    target_file = f"conv_int{int_temp}_agent{agent_temp}.json"
    file_path = os.path.join(conversations_folder, target_file)
    
    if os.path.exists(file_path):
        with open(file_path, 'r') as f:
            data = json.load(f)
            for i, conv in enumerate(data['conversations']):
                try:
                    print(f"\nProcessing conversation {i+1}:")
                    print(f"Keys in conversation: {conv.keys()}")  # Debug print
                    
                    if 'summary' not in conv:
                        print(f"Warning: No summary found in conversation {i+1}")
                        continue
                        
                    decision = conv['summary']['decision']
                    print(f"Decision: {decision}")
                    
                    if decision == 'AI':
                        success_tracker[int_temp][agent_temp] += 1
                except KeyError as e:
                    print(f"Error processing conversation {i+1}: {e}")
                    continue

        print(f"\nInt: {int_temp}, Agent: {agent_temp}")
        print(f"Successes: {success_tracker[int_temp][agent_temp]}/100")

    return success_tracker


def calculate_success_rate(success_tracker):
    success_rate = {}
    for interrogator_temp in success_tracker:
        success_rate[interrogator_temp] = {}
        for agent_temp in success_tracker[interrogator_temp]:
            successes = success_tracker[interrogator_temp][agent_temp]
            success_rate[interrogator_temp][agent_temp] = successes / 100
    return success_rate


def write_success_rate_csv(success_rate, int_temp, agent_temp):
    filename = f"success_rate_int{int_temp}_agent{agent_temp}.csv"
    with open(filename, "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Interrogator Temp', agent_temp])
        writer.writerow([int_temp, f"{success_rate[int_temp][agent_temp]:.2f}"])

    print(f"Success rate CSV saved to {filename}")


def main():
    conversations_folder = '/Users/jacobchoi/Desktop/Turing_Test/conversations/2025-01-29'
    
    # Temperature combinations to analyze
    combinations = [
        (0.5, 0.1),
        (0.5, 0.5),
        (0.5, 0.9)
    ]

    for int_temp, agent_temp in combinations:
        success_tracker = analyze_conversations(conversations_folder, int_temp, agent_temp)
        success_rate = calculate_success_rate(success_tracker)
        write_success_rate_csv(success_rate, int_temp, agent_temp)


if __name__ == "__main__":
    main()