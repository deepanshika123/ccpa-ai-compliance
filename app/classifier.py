def classify_section(title, content):

    text = content.lower()

    if "penalty" in text or "fine" in text:
        return "Penalty"

    elif "definition" in text:
        return "Definition"

    elif "consumer" in text:
        return "Consumer Rights"

    elif "enforcement" in text:
        return "Enforcement"

    else:
        return "General"