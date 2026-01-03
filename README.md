# LinkedIn Employee Scraper & Email Username Generator

A lightweight OSINT toolkit designed to extract employee names from LinkedIn and generate potential corporate email username formats.

This project is intended for OSINT research, recruitment intelligence, authorized red team simulations, and competitive analysis where understanding organizational naming conventions is required.

---

## Contents

- LinkedIn employee extraction from People Search
- LinkedIn employee extraction from Company People page
- Email username generation using multiple corporate formats

---

## Script Overview

### 1. LinkedIn Employee Extract – People Search

**File:** `LinkedIn Employee Extract from search people.js`  
**Use on:**  
https://www.linkedin.com/search/results/people/

#### Functionality

- Extracts employee names from LinkedIn People Search results
- Automatically navigates multiple result pages
- Stops after a configurable number of pages (`maxPages`)
- Can be manually stopped by pressing `ESC`
- Downloads extracted names as:

---

### 2. LinkedIn Employee Extract – Company People Page

**File:** `LinkedIn Employee Extract from company people.js`  
**Use on:**  
https://www.linkedin.com/company/<company-name>/people/

#### Functionality

- Automatically clicks **Show more results** until all employees are loaded
- Reliably extracts visible employee names

---

### 3. Email Username Generator

**File:** `Make email Address using Different format.py`  
**Run from:** Command Line

#### Functionality

- Accepts a `.txt` file of employee names from either JS script
- Normalizes and sanitizes names by:
  - Removing titles, brackets, and special characters
  - Removing Arabic script
  - Handling multi-part names
- Special handling for surnames starting with **Al**
- Supports names with two or more components

#### Generated Username Formats

Examples include:

- `firstname.lastname`
- `f.lastname`
- `flastname`
- `firstname.lastinitial`
- and additional combinations

---

## Usage

```bash
python generate_email_usernames.py names.txt example.com anotherdomain.com
