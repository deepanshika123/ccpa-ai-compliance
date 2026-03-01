import pdfplumber
import re

def extract_sections(pdf_path):
    full_text = ""

    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            if text:
                full_text += text + "\n"

    pattern = r"(Section 1798\.\d+)"
    parts = re.split(pattern, full_text)

    sections = {}

    for i in range(1, len(parts), 2):
        section_title = parts[i].strip()
        section_content = parts[i + 1].strip()
        sections[section_title] = section_content

    return sections


