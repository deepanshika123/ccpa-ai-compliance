import json

def search_sections(query):

    with open("classified_sections.json", "r", encoding="utf-8") as f:
        data = json.load(f)

    query_words = query.lower().split()
    results = []

    for title, details in data.items():
        content = details["content"].lower()

        match_count = 0

        for word in query_words:
            if word in content:
                match_count += 1

        # If at least 2 words match → consider relevant
        if match_count >= 2:
            results.append(title)

    return results