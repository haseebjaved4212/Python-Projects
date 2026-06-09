# Email Validator CLI Tool

An interactive, command-line utility written in Python that validates email addresses. Unlike basic checks that only look for a single character, this tool performs an exhaustive, step-by-step validation checking structure, character sets, and Top-Level Domains (TLD) using regular expressions (Regex), and reports the specific failure reason if an email is invalid.

---

## Improvements Made

The original script had several logical bugs (e.g. `if "@" and "." in email:` evaluated incorrectly, printed duplicate invalid warnings, did not check ordering or characters, and didn't support checking multiple emails without restarting). 

The project has been upgraded with:
1. **Descriptive Explanations:** Explains *why* the email was rejected (e.g., "Username must start with a letter or number", "Missing the '@' symbol", "Too short").
2. **Standard Regex Verification:** Utilizes the regular expression `^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$` to enforce standard syntax rules (RFC 5322).
3. **Interactive Test Loop:** Runs in an interactive loop allowing users to test multiple emails successively without relaunching the script.
4. **Clean Code Structure:** Modularized validation rules into a dedicated helper function, making the code testable and extensible.

---

## How Validation Works

The validator passes the input email through eight consecutive rules:

1. **Length Verification:** Ensures the email is at least 6 characters long.
2. **Symbol Count:** Verifies that the email contains exactly one `@` symbol.
3. **Empty Fields Check:** Confirms that neither the username (local part before `@`) nor the domain (part after `@`) is empty.
4. **First Character Check:** Ensures the username starts with an alphanumeric character (letter or number).
5. **Username Characters:** Ensures characters are letters, numbers, or standard punctuation (`.`, `_`, `%`, `+`, `-`).
6. **Domain Dot Check:** Checks that the domain part contains at least one dot (e.g., `gmail.com`).
7. **Domain Characters:** Ensures the domain only contains letters, numbers, dots, and hyphens.
8. **Top-Level Domain (TLD) Verification:** Verifies the last segment of the domain (e.g., `com` or `org`) is at least 2 characters long and contains only letters.

---

## Installation & Setup

### 1. Prerequisites
- Python 3.x

### 2. Download and Run
No external libraries are required (uses the built-in `re` module).
1. Open your terminal or command prompt.
2. Navigate to the project directory:
   ```bash
   cd "C:\Users\DELL\OneDrive\Desktop\Python Projects\01-email-Validation-"
   ```
3. Run the script:
   ```bash
   python main.py
   ```

---

## Example Usage

```
=========================================
       Email Validator CLI Tool          
=========================================
Type 'exit' or 'q' to quit.
-----------------------------------------
Enter email to validate: myemail@gmail.com
[+] SUCCESS: 'myemail@gmail.com' is a valid email address!
-----------------------------------------
Enter email to validate: test@com
[-] INVALID: Domain part must contain a dot (e.g., '.com', '.org').
-----------------------------------------
Enter email to validate: user@domain.c
[-] INVALID: Top-level domain (e.g. '.com', '.in') must be at least 2 characters long.
-----------------------------------------
Enter email to validate: exit
Goodbye!
```
