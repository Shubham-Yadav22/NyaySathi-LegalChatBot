import re
import json

# Load the raw text file
with open("BNS_DATASET1.txt", "r", encoding="utf-8") as f:
    raw_text = f.read()

# Split into sections
section_blocks = re.findall(r"## Section (\d+): (.*?)\n\n\*\*Clause\*\*:(.*?)(?=\n## Section|\Z)", raw_text, re.DOTALL)

# Extract chapter titles for categories
chapters = re.findall(r"## Chapter .*?: (.*?) \(Sections (\d+)-(\d+)\)", raw_text)
chapter_map = {}
for title, start, end in chapters:
    for sec_num in range(int(start), int(end)+1):
        chapter_map[str(sec_num)] = title.strip()

# Extract explanations
explanations = dict(re.findall(r"## Section (\d+):.*?\*\*Explanation\*\*: (.*?) Source", raw_text, re.DOTALL))

# Utility to extract keywords
def extract_keywords(text):
    return list(set(re.findall(r"\b[a-zA-Z]{4,}\b", text.lower())))

# Build final dataset
output = []
for sec_num, title, clause in section_blocks:
    key = sec_num.strip()
    clause = clause.strip()
    explanation = explanations.get(key, "").strip()

    section_entry = {
        "section": f"Section {key} BNS",
        "title": title.strip(),
        "keywords": extract_keywords(explanation),
        "explanation": explanation,
        "law_type": "BNS",
        "category": chapter_map.get(key, ""),
        "punishment": "",  # Most BNS procedural sections won't have punishments
        "language": "hinglish"
    }
    output.append(section_entry)

# Save as JSON
with open("section_db1.json", "w", encoding="utf-8") as f:
    json.dump(output, f, ensure_ascii=False, indent=2)

print(f"✅ Converted {len(output)} sections to section_db.json")
