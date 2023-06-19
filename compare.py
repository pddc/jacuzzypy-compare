import sys
import re
import time
from colorama import init, Fore, Back, Style

# Initialize colorama
init(autoreset=True)

# Define the positions and their labels
position_labels = {
    6: 'H',
    8: 'P2',
    10: 'P1*',
    12: 'UV',
    15: 'WT',
    19: 'd',
    20: 'm',
    21: 'Set',
    24: 'yr',
    27: 'min'
}

def compare_lines(line1, line2):
    # Ignore the last 4 characters
    line1 = line1[:-4]
    line2 = line2[:-4]

    # Ensure lines have the same length
    if len(line1) != len(line2):
        print("Error: Lines have different lengths.")
        return

    # Compare pairs of characters and highlight differences
    highlighted_line = [
        f"{Fore.BLACK}{Back.GREEN}{line2[i:i+2]}{Style.RESET_ALL}"
        if i // 2 in position_labels.keys() and line1[i:i+2] != line2[i:i+2]
        else f"{Fore.LIGHTYELLOW_EX}{Back.BLUE}{line2[i:i+2]}{Style.RESET_ALL}"
        if line1[i:i+2] != line2[i:i+2]
        else line2[i:i+2]
        for i in range(0, len(line1), 2)
    ]

    # Prepare the highlighted line
    highlighted_line_str = ''.join(highlighted_line)

    # Find the positions of the highlighted character pairs
    highlighted_positions = [i // 2 for i in range(0, len(line2), 2) if line1[i:i+2] != line2[i:i+2]]

    # Prepare the positions with labels and colorize the position numbers
    positions_with_labels = [
        f"{Fore.GREEN}{pos} {position_labels.get(pos, '')}{Style.RESET_ALL}"
        if pos in position_labels.keys()
        else f"{Fore.LIGHTYELLOW_EX}{Back.BLUE}{pos}{Style.RESET_ALL} {position_labels.get(pos, '')}"
        for pos in highlighted_positions
    ]

    # Print the highlighted line with the positions and labels
    print(f"{timestamp} - {highlighted_line_str}  ({', '.join(positions_with_labels)})")

# Get the log file path from command-line argument
if len(sys.argv) != 2:
    print("Error: Please provide the log file path as a command-line argument.")
    sys.exit(1)

log_file = sys.argv[1]

try:
    # Read the log file
    with open(log_file, 'r') as file:
        line1 = None  # Initialize line1 variable

        # Get the initial file position
        current_position = file.tell()

        while True:
            # Check for new lines added to the log file
            file.seek(current_position)
            new_lines = file.readlines()
            if new_lines:
                for line in new_lines:
                    line = line.strip()
                    if re.search(r"7e26ffafc4", line):
                        if "New msg:" in line:
                            # Extract the timestamp and message after "New msg:"
                            match = re.search(r'(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}).*New msg: (.+)', line)
                            if match:
                                timestamp = match.group(1).split()[1]  # Extract the time portion
                                msg = match.group(2)
                                if line1 is not None:
                                    # Compare the lines and highlight differences
                                    compare_lines(line1, msg)
                                line1 = msg
                    elif "Sending:" in line:
                        # Extract the timestamp and message after "Sending:"
                        match = re.search(r'(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}).*Sending: (.+)', line)
                        if match:
                            timestamp = match.group(1).split()[1]  # Extract the time portion
                            msg = match.group(2)
                            print(f"{timestamp} - {msg}")

                # Update the current file position
                current_position = file.tell()

            # Wait for 1 second before checking for new lines
            time.sleep(1)

except FileNotFoundError:
    print("Error: Log file not found.")
except Exception as e:
    print(f"Error: An error occurred: {str(e)}")
