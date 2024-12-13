import re

# Adjusted regex to avoid capturing groups
TITLE_MODEL_WORD_REGEX = r'[a-zA-Z0-9]*(?:[0-9]+[^0-9, ]+|[^0-9, ]+[0-9]+)[a-zA-Z0-9]*'
# This is in paper 7
KEY_VALUE_MODEL_WORD_REGEX = r'\d+(?:\.\d+)?[a-zA-Z]+$|^\d+(?:\.\d+)?$'
KEY_VALUE_MODEL_WORD_REGEX_Extension = r'^\d+\:\d+'

def extract_title_model_words(text):
    return set(re.findall(TITLE_MODEL_WORD_REGEX, text))

def extract_key_value_model_words(text):
    # Regular expression for ModelWordkey_valuepairs
    set_regular = set(re.findall(KEY_VALUE_MODEL_WORD_REGEX, text))
    set_extension = set(re.findall(KEY_VALUE_MODEL_WORD_REGEX_Extension, text))
    matches = set_regular | set_extension

    # Clean up matches
    cleaned_model_words = []

    for word in matches:
        # Extract numeric parts as strings
        cleaned_word = re.sub(r'[a-zA-Z]+', "", word)
        cleaned_model_words.append(cleaned_word)

    return cleaned_model_words

def find_all_model_words(products):
    title_model_words = set()
    key_value_model_words = set()

    for product in products:
        # Extract from titles
        title_model_words.update(extract_title_model_words(product['title']))
        # Extract from key-value pairs
        for value in product['attributes'].values():
            key_value_model_words.update(extract_key_value_model_words(value))

    return title_model_words | key_value_model_words


def generate_binary_vectors(products, all_model_words):
    # Step 1: Initialize MW as an empty set
    binary_vectors = []

    # Step 1: Collect model words from titles and attributes for all products
    for product in products:
        # Step 2: Initialize a set for the model words of the current product
        product_model_words = set()

        # Add model words from the title of the product
        product_model_words.update(extract_title_model_words(product['title']))
        # Add model words from the attribute values of the product
        for attr in product['attributes'].values():
            product_model_words.update(extract_key_value_model_words(attr))

        # Step 3: Create a binary vector for the current product
        vector = []
        for mw in all_model_words:
            if mw in extract_title_model_words(product['title']) or \
                    any(mw in extract_key_value_model_words(value) for value in product['attributes'].values()):
                vector.append(1)
            else:
                vector.append(0)
        binary_vectors.append(vector)

    # Step 4: Return binary vectors for all products
    return binary_vectors
