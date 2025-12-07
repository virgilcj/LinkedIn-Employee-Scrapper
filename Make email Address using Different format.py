import re
import sys
import ast
import os
import zipfile

REMOVE_WORDS = {
    "mr", "mrs", "ms", "miss", "dr", "eng", "engr",
    "phd", "mphil", "msc", "mba", "pmp", "mrics", "cism", "ceh",
    "beng", "be", "me", "cert", "hons"
}

def contains_arabic(text):
    return any('\u0600' <= c <= '\u06FF' for c in text)

def clean_name(name):
    name = name.lower()
    name = re.sub(r"\(.*?\)", "", name)
    name = re.sub(r"[^a-zA-Z\s-]", " ", name)
    name = name.replace("-", " ").replace("_", " ")
    name = re.sub(r"\s+", " ", name).strip()
    parts = name.split()
    parts = [p for p in parts if p not in REMOVE_WORDS]
    if contains_arabic(name):
        return []
    return parts

def generate_username_formats(parts):
    formats = {
        "firstname_dot_lastname": set(),
        "f_dot_lastname": set(),
        "flastname": set()
    }

    if len(parts) < 2:
        return formats

    firstname = parts[0]
    secondname = parts[1]
    lastname = parts[-1]

    # Skip invalid short initials (e.g., a.s)
    if len(firstname) == 1 and len(lastname) == 1:
        return formats

    # Main formats
    formats["firstname_dot_lastname"].add(f"{firstname}.{lastname}")
    formats["f_dot_lastname"].add(f"{firstname[0]}.{lastname}")
    formats["flastname"].add(f"{firstname[0]}{lastname}")

    # Extra: if 3 parts, use secondname variations
    if len(parts) >= 3:
        formats["firstname_dot_lastname"].add(f"{firstname}.{secondname}")
        formats["f_dot_lastname"].add(f"{firstname[0]}.{secondname}")
        formats["flastname"].add(f"{firstname[0]}{secondname}")

    # Handle "Al" logic
    for i in range(len(parts) - 1):
        if parts[i] == "al":
            al_last = "al" + parts[i + 1]
            if al_last != "al":  # Don't allow "rand.al"
                formats["firstname_dot_lastname"].add(f"{firstname}.{al_last}")
                formats["f_dot_lastname"].add(f"{firstname[0]}.{al_last}")
                formats["flastname"].add(f"{firstname[0]}{al_last}")

    return formats

# ===== MAIN =====
if len(sys.argv) < 3:
    print("Usage: python script.py <file.txt> <domain1> [domain2] ...")
    sys.exit(1)

filename = sys.argv[1]
domains = sys.argv[2:]

try:
    with open(filename, "r", encoding="utf-8") as f:
        raw = f.read().strip()
        if raw.startswith("["):
            names = ast.literal_eval(raw)
        else:
            names = [line.strip() for line in raw.splitlines() if line.strip()]
except Exception as e:
    print("Error reading file:", e)
    sys.exit(1)

# Initialize all formats
combined_formats = {
    "firstname_dot_lastname": set(),
    "f_dot_lastname": set(),
    "flastname": set()
}

# Parse each name
for raw_name in names:
    parts = clean_name(raw_name)
    if not parts or len(parts) < 2:
        continue
    formats = generate_username_formats(parts)
    for fmt in formats:
        combined_formats[fmt].update(formats[fmt])

# Save per domain
for domain in domains:
    folder = f"usernames_{domain}"
    os.makedirs(folder, exist_ok=True)
    all_domain_emails = []

    for fmt, usernames in combined_formats.items():
        emails = sorted([f"{u}@{domain}" for u in usernames])
        all_domain_emails.extend(emails)
        with open(os.path.join(folder, f"{fmt}.txt"), "w") as f:
            f.write("\n".join(emails))

    with open(os.path.join(folder, "all.txt"), "w") as f:
        f.write("\n".join(sorted(all_domain_emails)))

    # Zip the folder
    zip_filename = f"{folder}.zip"
    with zipfile.ZipFile(zip_filename, 'w') as zipf:
        for root, _, files in os.walk(folder):
            for file in files:
                zipf.write(os.path.join(root, file), arcname=os.path.join(folder, file))

    print(f"✅ Saved and zipped: {zip_filename}")
