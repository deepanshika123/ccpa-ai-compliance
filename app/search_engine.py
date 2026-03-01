import json

def search_sections(query):

    with open("classified_sections.json", "r", encoding="utf-8") as f:
        data = json.load(f)

    query = query.lower()
    results = []

    for title, details in data.items():
        if query in details["content"].lower():
            results.append({
                "title": title,
                "category": details["category"]
            })

    return results