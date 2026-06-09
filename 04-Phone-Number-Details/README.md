# Phone Number Details Finder

A simple CLI utility written in Python that fetches geographical location (country), service provider (carrier/operator), and associated time zones for any phone number worldwide. It uses Google's `libphonenumber` library port for Python to parse and validate global phone numbers.

---

## Features

- **Country/Region Name Lookup:** Identify the country or region of the phone number (e.g., "United States", "United Kingdom", "India").
- **Carrier/Operator Detection:** Identify the telecommunications provider (e.g., "Verizon", "Vodafone", "Jio") for mobile numbers.
- **Time Zone Resolution:** Fetch a list of all time zones corresponding to the phone number's prefix.
- **Cross-Platform:** Runs in any terminal environment with Python installed.

---

## How It Works

This project is built using the **`phonenumbers`** library, which is the Python port of Google's open-source `libphonenumber` library:
1. **Parsing:** The script takes raw user input and parses it into an structured object containing the country calling code, national number, and optional extension.
2. **Geocoding:** It checks the country/area code database to resolve the human-readable English name of the location.
3. **Carrier Lookup:** It parses prefix lists against known carrier configurations to determine the operator.
4. **Time Zone Mapping:** It compares the national destination codes/prefixes against a built-in timezone offset mapping to retrieve valid time zone names (e.g., `Europe/London`, `Asia/Kolkata`).

---

## Installation & Setup

### 1. Prerequisites
- Python 3.x

### 2. Install Dependencies
Run the following command in your terminal to install the `phonenumbers` package:
```bash
pip install phonenumbers
```

---

## Usage Instructions

1. Open your terminal or command prompt.
2. Navigate to the project folder:
   ```bash
   cd "C:\Users\DELL\OneDrive\Desktop\Python Projects\04-Phone-Number-Details"
   ```
3. Run the script:
   ```bash
   python main.py
   ```
4. Enter a phone number **with its country code** (must start with `+`). For example:
   - US number: `+14155552671`
   - UK number: `+442079460958`
   - India number: `+919876543210`

### Example Output:
```
Enter your phone number with country code: +14155552671
Country:  San Francisco, CA
Operator:  Saddleback Communications
Timezone:  ('America/Los_Angeles',)
```

---

## Important Notes

- **Country Code Prefix:** You **must** include the plus sign (`+`) and the country code when inputting numbers. If you omit the `+`, the parsing library will not be able to identify the region and will raise a parsing error.
- **Landlines vs. Mobiles:** Carrier detection works best on mobile numbers. For some landlines, the carrier might return blank or default provider names.
