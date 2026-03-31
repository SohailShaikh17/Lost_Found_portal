import re
from collections import Counter
def tokenize(text):
    text = re.sub(r'[^a-zA-Z0-9\s]', ' ', text.lower())
    return {w for w in text.split() if len(w) > 2}

def get_matching_items(current_item, queryset, top_n=5):
    current_keywords = tokenize(f"{current_item.title} {current_item.description} {current_item.location} {current_item.category}")
    scored = []
    for item in queryset:
        item_keywords = tokenize(f"{item.title} {item.description} {item.location} {item.category}")
        overlap = current_keywords & item_keywords
        score = len(overlap)
        if score > 0:
            scored.append((score, overlap, item))
    scored.sort(key=lambda x: x[0], reverse=True)
    return scored[:top_n]
