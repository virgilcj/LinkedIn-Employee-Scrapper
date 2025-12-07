LinkedIn Employee Scraper & Email Username Generator

This toolkit contains three powerful scripts designed to automate the collection and transformation of LinkedIn employee data into potential corporate email formats. Ideal for OSINT, recruiting, red teaming, and competitive intelligence tasks.

📁 Contents
1. LinkedIn Employee Extract from search people.js

Use on:
🔍 LinkedIn People Search
https://www.linkedin.com/search/results/people/

Functionality:

Automatically scrapes employee names from search results across multiple pages.

Stops after a set number of pages (maxPages) or manually by pressing ESC.

Downloads the names as a .txt file (linkedin_employees.txt), one name per line.

2. LinkedIn Employee Extract from company people.js

Use on:
🏢 LinkedIn Company People Tab
https://www.linkedin.com/company/<company-name>/people/

Functionality:

Automatically clicks “Show more results” until all visible employees are loaded.

Extracts employee names reliably.

Downloads names into company_employees.txt.

3. Make email Address using Different format.py

Use on:
🧠 Command line
Requires a .txt file of names from either of the above scripts.

Functionality:

Parses and sanitizes names (removing titles, brackets, special characters, and Arabic script).

Handles complex formats including “Al” (e.g., f.alzaabi, falzaabi, first.alzaabi).

Supports names with 2+ parts (e.g., first.second, f.second, flastname, etc.).

Generates all possible combinations and saves to domain-specific files:

firstname.lastname@domain

f.lastname@domain

flastname@domain

and more...

Usage:

python generate_email_usernames.py names.txt example.com anotherdomain.com


Creates:

/example.com/
  - usernames_firstname.lastname.txt
  - usernames_f.lastname.txt
  - usernames_flastname.txt
  - usernames_all.txt

/anotherdomain.com/
  ...

🔧 Requirements

Chrome (for running JS in DevTools Console)

Python 3+ (for generate_email_usernames.py)
