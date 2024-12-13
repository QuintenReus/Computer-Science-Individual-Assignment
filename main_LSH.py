import random
import json
from statistics import mean
import matplotlib.pyplot as plt
from data_cleaning import clean_product_data
from model_words import find_all_model_words, generate_binary_vectors
from minhashing import compute_signature_matrix
from lsh import *
import numpy as np

# Load and clean dataset
with open('TVs.json', 'r') as f:
    raw_data = json.load(f)

# Clean product data (using the data cleaning functions)
cleaned_data = clean_product_data(raw_data)

# Compute global true duplicates (by modelID)
true_duplicates = []
for i, product_i in enumerate(cleaned_data):
    for j, product_j in enumerate(cleaned_data):
        if i < j and product_i['modelID'] == product_j['modelID']:
            true_duplicates.append((i, j))

# Evaluate with bootstraps
bootstrap_iterations = 5
sample_size = int(.63 * len(cleaned_data))

t_values = np.arange(0.05, 1, 0.05)

all_pq_values = []
all_pc_values = []
all_f1_star_values = []
all_fraction_comparisons = []

for iteration in range(bootstrap_iterations):
    print("Bootstrap iteration: ", iteration)
    # Generate bootstrap sample
    bootstrap_indices = random.sample(range(len(cleaned_data)), k=sample_size)
    bootstrap_data = [cleaned_data[i] for i in bootstrap_indices]
    # Filter true duplicates for the bootstrap sample
    bootstrap_true_duplicates = {
        (i, j) for (i, j) in true_duplicates if i in bootstrap_indices and j in bootstrap_indices
    }
    print("bootstrap true duplicates: ", bootstrap_true_duplicates)

    # Min-hashing, create signature matrix
    binary_vectors = generate_binary_vectors(bootstrap_data, find_all_model_words(bootstrap_data))
    signature_matrix = compute_signature_matrix(binary_vectors, num_hashes=int(len(binary_vectors[0]) / 2))

    # Metrics for this bootstrap
    bootstrap_pq, bootstrap_pc, bootstrap_f1_star, bootstrap_fraction_comparisons = [], [], [], []

    for t in t_values:
        print("Current t:", t)
        b, r, n = find_b_r(len(signature_matrix), t)
        lsh_candidates, fraction_of_comparisons = apply_lsh(signature_matrix, r, n)
        pq, pc, f1_star = evaluate_lsh_performance(bootstrap_true_duplicates, lsh_candidates)

        # Collect metrics for this threshold
        bootstrap_pq.append(pq)
        bootstrap_pc.append(pc)
        bootstrap_f1_star.append(f1_star)
        bootstrap_fraction_comparisons.append(fraction_of_comparisons)

    # Collect metrics for this bootstrap for all values of t
    all_pq_values.append(bootstrap_pq)
    all_pc_values.append(bootstrap_pc)
    all_f1_star_values.append(bootstrap_f1_star)
    all_fraction_comparisons.append(bootstrap_fraction_comparisons)

# Combine metrics from all bootstraps
average_pq = [mean(values) for values in zip(*all_pq_values)]
print("average pq values per t across all bootstraps: ", average_pq)
average_pc = [mean(values) for values in zip(*all_pc_values)]
print("average pc values per t across all bootstraps: ", average_pc)
average_f1_star = [mean(values) for values in zip(*all_f1_star_values)]
print("average f1 values per t across all bootstraps: ", average_f1_star)
average_fraction_of_comparisons = [mean(values) for values in zip(*all_fraction_comparisons)]
print("average fraction of comparisons: ",average_fraction_of_comparisons)

# Initialise the figure
fig, axes = plt.subplots(3, 1, figsize=(10, 20))

# Plot Average PQ
axes[0].plot(average_fraction_of_comparisons, average_pq, marker='o', linestyle='-', color='green', label='Average PQ')
axes[0].set_xlabel('Average Fraction of Comparisons')
axes[0].set_ylabel('Average PQ')
axes[0].set_title('LSH: Average PQ vs. Average Fraction of Comparisons')
axes[0].grid(True)
axes[0].legend()

# Plot Average PC
axes[1].plot(average_fraction_of_comparisons, average_pc, marker='o', linestyle='-', color='orange', label='Average PC')
axes[1].set_xlabel('Average Fraction of Comparisons')
axes[1].set_ylabel('Average PC')
axes[1].set_title('LSH: Average PC vs. Average Fraction of Comparisons')
axes[1].grid(True)
axes[1].legend()

# Plot Average F1-Star
axes[2].plot(average_fraction_of_comparisons, average_f1_star, marker='o', linestyle='-', color='red',
           label='Average F1-Star')
axes[2].set_xlabel('Average Fraction of Comparisons')
axes[2].set_ylabel('Average F1-Star')
axes[2].set_title('LSH: Average F1-Star vs. Average Fraction of Comparisons')
axes[2].grid(True)
axes[2].legend()

# Adjust layout and show
plt.tight_layout()
plt.show()