import re
def normalize_unit(value):
    value = value.lower()
    # Replace units with a regularised form
    value = re.sub(r'\b(inches| inch| inches|-inch|-inches)\b|"', "inch", value)
    value = re.sub(r"\b(hertz|-hz|-hertz| hz| hertz)\b", "hz", value)
    value = re.sub(r"\b( lbs|lb| lb|pounds| pounds)\b", "lbs", value)
    value = re.sub(r"\b( year| years)\b", "year", value)
    return value


def clean_product_data(product_data):
    cleaned_data = []
    for model_id, product_variants in product_data.items():
        for product in product_variants:
            # Normalise the title and attribute values
            title = normalize_unit(product.get("title", ""))
            features_map = {key: normalize_unit(value) for key, value in product.get("featuresMap", {}).items()}

            # Create cleaned product entry
            cleaned_data.append({"title": title, "attributes": features_map, "shop": product.get("shop"), "url": product.get("url"), "modelID": model_id})

    return cleaned_data
