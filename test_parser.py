import json
from app.statute_parser import extract_sections
from app.classifier import classify_section   # make sure classifier.py app folder me ho
from app.search_engine import search_sections

# Step 1: Extract Sections
sections = extract_sections("data/ccpa_statute.pdf")

print("Total Sections Found:", len(sections))

for key in list(sections.keys())[:5]:
    print(key)

# Step 2: Save Raw Sections to JSON
with open("sections_output.json", "w", encoding="utf-8") as f:
    json.dump(sections, f, indent=4)

print("Raw sections saved to sections_output.json")

# Step 3: Classification
classified = {}

for title, content in sections.items():
    category = classify_section(title, content)
    classified[title] = {
        "category": category,
        "content": content
    }

# Step 4: Save Classified Output
with open("classified_sections.json", "w", encoding="utf-8") as f:
    json.dump(classified, f, indent=4)

print("Classified sections saved to classified_sections.json")



# adding Query test for search engine
query = "penalty"
results = search_sections(query)

print("\nSearch Results for:", query)
for r in results[:5]:
    print(r)

