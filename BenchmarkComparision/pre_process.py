import json
import re

def load_jsonl_file(filename):
    """
    Load data from a JSONL file (JSON Lines format) where each line is a separate JSON object.
    
    Args:
        filename: Path to the JSONL file
        
    Returns:
        list: List of JSON objects
    """
    data = []
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            for line_num, line in enumerate(file, 1):
                line = line.strip()
                if line:  # Skip empty lines
                    try:
                        json_obj = json.loads(line)
                        data.append(json_obj)
                    except json.JSONDecodeError as e:
                        print(f"Error parsing JSON on line {line_num}: {e}")
                        continue
    except FileNotFoundError:
        print(f"File {filename} not found.")
        return []
    except Exception as e:
        print(f"Error reading file: {e}")
        return []
    
    return data

def extract_high_level_instructions(data):
    """
    Extract high-level instructions from the conversations in the JSON data.
    
    Args:
        data: JSON data (single object or list of objects)
        
    Returns:
        list: List of extracted high-level instructions
    """
    instructions = []
    
    # Check if data is a single object or a list
    if isinstance(data, dict):
        data = [data]  # Convert single object to list for uniform processing
    
    for item in data:
        if 'conversations' in item:
            for conversation in item['conversations']:
                if conversation.get('from') == 'human':
                    # Get the value content
                    value = conversation.get('value', '')
                    
                    # Look for "High-level instruction:" pattern (case insensitive)
                    lines = value.split('\n')
                    for line in lines:
                        line = line.strip()
                        # Match various patterns for high-level instruction
                        if re.match(r'^high-?level\s+instruction\s*:', line, re.IGNORECASE):
                            # Extract the instruction text after the colon
                            instruction = re.sub(r'^high-?level\s+instruction\s*:\s*', '', line, flags=re.IGNORECASE)
                            if instruction:  # Only add non-empty instructions
                                instructions.append(instruction)
                            break
    
    return instructions

def save_instructions_to_json(instructions, output_filename):
    """
    Save instructions list to a JSON file.
    
    Args:
        instructions: List of instruction strings
        output_filename: Name of the output JSON file
    """
    try:
        with open(output_filename, 'w', encoding='utf-8') as f:
            json.dump(instructions, f, indent=2, ensure_ascii=False)
        print(f"Instructions saved to '{output_filename}'")
    except Exception as e:
        print(f"Error saving to file: {e}")

# Example usage with the provided JSON object


# Method 1: Process from a file
# Replace 'your_file.jsonl' with your actual file path
filename = '/mnt/home-ldap/vkharsh_ldap/Research/EnterpriseBench/BenchmarkComparision/ac_high_processing.jsonl'  # Change this to your file name

try:
    with open(filename, 'r') as file:
        json_data = [json.loads(line) for line in file if line.strip()]
except Exception as e:
    print(f"Error loading JSON file: {e}")
    json_data = []

# Process file data if available
if json_data:
    print(f"\nProcessing data from file '{filename}':")
    instructions_from_file = extract_high_level_instructions(json_data)
    
    print("Extracted high-level instructions:")
    for i, instruction in enumerate(instructions_from_file, 1):
        print(f"{i}. {instruction}")
    
    print(f"\nTotal instructions found: {len(instructions_from_file)}")
    
    # Save to JSON file
    save_instructions_to_json(instructions_from_file, 'extracted_high_level_instructions.json')
    
    # Also save as a text file for easy reading
    with open('extracted_high_level_instructions.txt', 'w', encoding='utf-8') as f:
        for i, instruction in enumerate(instructions_from_file, 1):
            f.write(f"{i}. {instruction}\n")
    
    print("Instructions also saved to 'extracted_high_level_instructions.txt'")
else:
    print("No file data to process. Only sample data was processed.")

print("\nDone!")