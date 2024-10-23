import json
import re
import difflib
import matplotlib.pyplot as plt
import numpy as np

# Tokenization function to split code into tokens for similarity calculation
def tokenize(line):
    # Tokenize based on word boundaries and sequences of characters
    return re.findall(r'\b\w+\b', line)

# Similarity calculation between two pieces of code
def calculate_code_similarity(code1, code2):
    # Split the code into lines
    code1_lines = code1.splitlines()
    code2_lines = code2.splitlines()

    print(f"Comparing Code 1 with {len(code1_lines)} lines and Code 2 with {len(code2_lines)} lines")

    total_tokens = 0
    matching_tokens = 0

    # Convert lines to sets for exact match comparison
    code1_lines_set = set(code1_lines)
    code2_lines_set = set(code2_lines)
    
    exact_matches = code1_lines_set & code2_lines_set
    
    print(f"Found {len(exact_matches)} exact matching lines")

    # Count matching tokens from exact matches
    for line in exact_matches:
        tokens = tokenize(line)
        total_tokens += len(tokens)
        matching_tokens += len(tokens)
    
    # Remove exact matches from further comparison
    code1_lines = [line for line in code1_lines if line not in exact_matches]
    code2_lines = [line for line in code2_lines if line not in exact_matches]
    
    # Find approximate matches for remaining lines
    for line in code1_lines:
        tokens_line1 = tokenize(line)
        best_match = difflib.get_close_matches(line, code2_lines, n=1, cutoff=0.1)
        
        if best_match:
            tokens_line2 = tokenize(best_match[0])
            matcher = difflib.SequenceMatcher(None, tokens_line1, tokens_line2)
            matching_blocks = matcher.get_matching_blocks()

            for match in matching_blocks:
                matching_tokens += match.size

            total_tokens += max(len(tokens_line1), len(tokens_line2))
            code2_lines.remove(best_match[0])

    # Add remaining unmatched tokens
    for line in code1_lines + code2_lines:
        tokens = tokenize(line)
        total_tokens += len(tokens)

    similarity_percentage = (matching_tokens / total_tokens) * 100 if total_tokens > 0 else 0

    print(f"Similarity: {similarity_percentage:.2f}%")
    
    return similarity_percentage

# Function to read JSON file and calculate similarity across iterations
def calculate_similarity_over_iterations(json_file):
    with open(json_file, 'r') as f:
        data = json.load(f)['test_data_3_2']

    similarities = []
    
    for i in range(1, len(data)):
        code1 = data[i-1]["Code"]
        code2 = data[i]["Code"]
        similarity = calculate_code_similarity(code1, code2)
        similarities.append(similarity)

    return similarities


def run_similarity(path = 'results/test_data_3_2.json'):
    # Example usage: Replace 'test_data.json' with your actual JSON file path
    similarities = calculate_similarity_over_iterations(path)

    # Generate plot
    iterations = list(range(1, len(similarities) + 1))
    average_similarity = np.mean(similarities)

    plt.figure(figsize=(10, 6))
    plt.plot(iterations, similarities, marker='o', linestyle='-', color='b', label='Similarity')
    plt.axhline(y=average_similarity, color='r', linestyle='--', label=f'Average Similarity ({average_similarity:.2f}%)')
    plt.title('Code Similarity Across Iterations')
    plt.xlabel('Iteration')
    plt.ylabel('Similarity Percentage')
    plt.grid(True)
    plt.legend()

    # Save the plot to a file
    plt.savefig('code_similarity_plot.png')

    # Display the plot
    plt.show()