import random
import json
from statistics import mean
from data_cleaning import clean_product_data
from model_words import find_all_model_words, generate_binary_vectors
from minhashing import compute_signature_matrix
from lsh import *
from MSM import similarity_algorithm, clustering
import numpy as np
import matplotlib.pyplot as plt

# Load and clean dataset
with open('TVs.json', 'r') as f:
    raw_data = json.load(f)


# Clean product data (using the data cleaning functions)
cleaned_data = clean_product_data(raw_data)

# Compute true duplicates (by modelID)
true_duplicates = []
for i, product_i in enumerate(cleaned_data):
    for j, product_j in enumerate(cleaned_data):
        if i < j and product_i['modelID'] == product_j['modelID']:
            true_duplicates.append((i, j))

# Evaluate with bootstraps
bootstrap_iterations = 5
sample_size = int(.63 * len(cleaned_data))
print("sample_size: ", sample_size)

# Metrics for summary
bootstrap_metrics = {
    "F1": [],
    "PQ": [],
    "PC": [],
    "F1_Star": [],
    "Duplicates_Found": [],
}
t_values = np.arange(0.05, 1.01, 0.1)

# Initialize lists to store metrics per t across bootstraps
all_f1_values = []
all_pq_values = []
all_pc_values = []
all_f1_star_values = []
all_fraction_comparisons = []

for iteration in range(bootstrap_iterations):
    print("Bootstrap iteration: ", iteration)
    # Generate bootstrap sample and test sample, bootstrap without replacement, size of bootstrap = 63% of original data
    train_indices = random.sample(range(len(cleaned_data)), k=sample_size)
    train_data = [cleaned_data[i] for i in train_indices]
    print("train size:", len(train_indices))
    test_indices = list(set(range(len(cleaned_data))) - set(train_indices))
    test_data = [cleaned_data[i] for i in test_indices]
    print("test size:", len(test_indices))

    # Filter true duplicates for the bootstrap sample
    train_true_duplicates = {
        (i, j) for (i, j) in true_duplicates if i in train_indices and j in train_indices
    }
    test_true_duplicates = {
        (i, j) for (i, j) in true_duplicates if i in test_indices and j in test_indices
    }

    # Min-hashing, create signature matrix
    binary_vectors = generate_binary_vectors(train_data, find_all_model_words(train_data))
    signature_matrix = compute_signature_matrix(binary_vectors,
                                                num_hashes=int(len(binary_vectors[0]) / 2))  # 50% of size of
    # signature vector as suggested in MSMP+
    overall_pq, overall_pc, overall_f1_star, overall_fraction_comparisons = [], [], [], []

    # Optimise epsilon for varying LSH thresholds using train set
    optimal_epsilons = {}
    for t in t_values:
        print("Current t: ", t)
        _, r, n = find_b_r(int(len(binary_vectors[0]) / 2), t)
        lsh_candidates, fraction_of_comparisons = apply_lsh(signature_matrix, r, n)

        print("fraction_of_comparisons: ", fraction_of_comparisons)
        print(f"lsh_candidates: {len(lsh_candidates)}")
        best_epsilon, best_f1 = None, -1
        distance_matrix = similarity_algorithm(lsh_candidates,train_data)
        # Iterate over a range of epsilon values
        for epsilon in np.arange(0.1, 1.1, 0.1):
            detected_duplicates = clustering(distance_matrix, epsilon)
            # Evaluation for MSM performance
            true_positives = len(set(detected_duplicates) & set(train_true_duplicates))
            false_positives = len(detected_duplicates) - true_positives
            false_negatives = len(train_true_duplicates) - true_positives

            # Metrics for MSM performance
            precision = true_positives / len(detected_duplicates) if len(detected_duplicates) > 0 else 0
            recall = true_positives / len(train_true_duplicates)
            f1 = (2 * precision * recall) / (precision + recall) if precision + recall > 0 else 0
            if f1 > best_f1:
                best_f1 = f1
                best_epsilon = epsilon

        optimal_epsilons[t] = best_epsilon

    print("---- Starting test phase -----")
    # Min-hashing, create signature matrix for the test data
    binary_vectors = generate_binary_vectors(test_data, find_all_model_words(test_data))
    signature_matrix = compute_signature_matrix(binary_vectors,
                                                num_hashes=int(len(binary_vectors[0]) / 2))  # 50% of size of

    # binary signature vector as suggested in MSMP+
    bootstrap_f1, bootstrap_pq, bootstrap_pc, bootstrap_f1_star, bootstrap_fraction_comparisons = [], [], [], [], []
    for t, best_epsilon in optimal_epsilons.items():
        print("Current t: ", t)
        _, r, n = find_b_r(int(len(binary_vectors[0]) / 2), t)
        lsh_candidates, fraction_of_comparisons = apply_lsh(signature_matrix, r, n)
        pq, pc, f1_star = evaluate_lsh_performance(test_true_duplicates, lsh_candidates)
        distance_matrix = similarity_algorithm(lsh_candidates,test_data)
        detected_duplicates = clustering(distance_matrix, best_epsilon)

        # Calculate MSM metrics
        true_positives = len(set(detected_duplicates) & set(test_true_duplicates))
        precision = true_positives / len(detected_duplicates) if len(detected_duplicates) > 0 else 0
        recall = true_positives / len(test_true_duplicates) if len(test_true_duplicates) > 0 else 0
        f1 = (2 * precision * recall) / (precision + recall) if precision + recall > 0 else 0

        # Collect metrics for this threshold
        bootstrap_f1.append(f1)     # should have length 20 after all t's
        bootstrap_pq.append(pq)
        bootstrap_pc.append(pc)
        bootstrap_f1_star.append(f1_star)
        bootstrap_fraction_comparisons.append(fraction_of_comparisons)

    # Collect metrics for this bootstrap for all values of t
    all_f1_values.append(bootstrap_f1)
    all_pq_values.append(bootstrap_pq)
    all_pc_values.append(bootstrap_pc)
    all_f1_star_values.append(bootstrap_f1_star)
    all_fraction_comparisons.append(bootstrap_fraction_comparisons)

# Combine metrics from all bootstraps
average_f1 = [mean(values) for values in zip(*all_f1_values)]
print("average f1 values per t across all bootstraps: ", average_f1)
average_pq = [mean(values) for values in zip(*all_pq_values)]
print("average pq values per t across all bootstraps: ", average_pq)
average_pc = [mean(values) for values in zip(*all_pc_values)]
print("average pc values per t across all bootstraps: ", average_pc)
average_f1_star = [mean(values) for values in zip(*all_f1_star_values)]
print("average f1 values per t across all bootstraps: ", average_f1_star)
average_fraction_of_comparisons = [mean(values) for values in zip(*all_fraction_comparisons)]
print(average_fraction_of_comparisons)

# Initialize the figure
fig, axes = plt.subplots(4, 1, figsize=(10, 20))

# Plot Average F1
axes[0].plot(average_fraction_of_comparisons, average_f1, marker='o', linestyle='-', color='blue', label='Average F1')
axes[0].set_xlabel('Fraction of Comparisons')
axes[0].set_ylabel('F1')
axes[0].set_title('Average F1 vs. Average Fraction of Comparisons')
axes[0].grid(True)
axes[0].legend()

# Plot Average PQ
axes[1].plot(average_fraction_of_comparisons, average_pq, marker='o', linestyle='-', color='green', label='Average PQ')
axes[1].set_xlabel('Fraction of Comparisons')
axes[1].set_ylabel('PQ')
axes[1].set_title('PQ vs. Average Fraction of Comparisons')
axes[1].grid(True)
axes[1].legend()

# Plot Average PC
axes[2].plot(average_fraction_of_comparisons, average_pc, marker='o', linestyle='-', color='orange', label='Average PC')
axes[2].set_xlabel('Fraction of Comparisons')
axes[2].set_ylabel('PC')
axes[2].set_title('Average PC vs. Average Fraction of Comparisons')
axes[2].grid(True)
axes[2].legend()

# Plot Average F1-Star
axes[3].plot(average_fraction_of_comparisons, average_f1_star, marker='o', linestyle='-', color='red', label='Average F1-Star')
axes[3].set_xlabel('Fraction of Comparisons')
axes[3].set_ylabel('F1-Star')
axes[3].set_title('Average F1-Star vs. Average Fraction of Comparisons')
axes[3].grid(True)
axes[3].legend()

# Adjust layout and show
plt.tight_layout()
plt.show()