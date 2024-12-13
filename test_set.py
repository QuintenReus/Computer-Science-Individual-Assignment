import json

# Input and output file paths
input_file = 'TVs.json'
output_file = 'test_set.json'

# Number of products to include in the test set
num_products = 100

# Load the JSON data
with open(input_file, 'r') as f:
    data = json.load(f)

# Select the first few products
test_set = {key: data[key] for key, _ in zip(data.keys(), range(num_products))}

# Save the test set to a new file
with open(output_file, 'w') as f:
    json.dump(test_set, f, indent=4)

print(f"Test set with {num_products} products created successfully!")