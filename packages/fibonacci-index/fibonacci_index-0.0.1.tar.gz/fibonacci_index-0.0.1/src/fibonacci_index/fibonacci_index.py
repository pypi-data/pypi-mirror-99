import json

def sum(fibonacci_index):
    fibonacci_sequence = []

    if(len(fibonacci_sequence) <= fibonacci_index):
        for i in range(len(fibonacci_sequence), fibonacci_index + 1):
            next_number = fibonacci_sequence[i-2] + fibonacci_sequence[i - 1] if len(
                fibonacci_sequence) > 1 else i + 1

            fibonacci_sequence.insert(i, next_number)

    return json.dumps(fibonacci_sequence[fibonacci_index])
