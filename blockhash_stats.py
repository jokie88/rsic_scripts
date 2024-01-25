import subprocess
from collections import defaultdict

# File to save the results
output_file = 'blockhashes.txt'

# Dictionary to count occurrences of each hex character
hex_char_counts = defaultdict(int)
total_blocks = 0
start_block = 826767
#end_block = 827274
halvening_block = 840000
try:
    end_block = subprocess.check_output(['bitcoin-cli', 'getblockcount']).decode().strip()
    end_block = int(end_block)
    for height in range(start_block, end_block):
        # Execute the bitcoin-cli command
        result = subprocess.check_output(['bitcoin-cli', 'getblockhash', str(height)])
        blockhash = result.decode().strip()

        # Increment the count for the rightmost hex character
        hex_char_counts[blockhash[-1]] += 1
        total_blocks += 1

        if height % 10000 == 0:
            print(f"Processed {height} blocks.")
            for hex_char, count in hex_char_counts.items():
                percentage = (count / total_blocks) * 100
                print(f"{hex_char}: {percentage:.2f}%")

except subprocess.CalledProcessError as e:
    print(f"Error at height {height}: {e}")

# Calculate and print the percentages
print(f"Range: {start_block} to {end_block}. {total_blocks} mined. {840000 - end_block} more until halvening")
print("Count of each hex character as rightmost digit in blockhashes:")
for hex_char, count in sorted(hex_char_counts.items(), key=lambda item: item[1], reverse=True):
    percentage = (count / total_blocks) * 100
    print(f"{hex_char}\t{count}\t{percentage:.2f}%")


