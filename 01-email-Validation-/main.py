import re

def validate_email(email):
    """
    Validates an email address and returns a tuple (is_valid, reason).
    """
    email = email.strip()
    
    # 1. Check length
    if len(email) < 6:
        return False, "Email must be at least 6 characters long."
        
    # 2. Check for the '@' symbol
    if "@" not in email:
        return False, "Email is missing the '@' symbol."
        
    if email.count("@") > 1:
        return False, "Email must contain exactly one '@' symbol."
        
    # Split into local part and domain part
    local_part, domain_part = email.split("@", 1)
    
    # 3. Check for empty local or domain parts
    if not local_part:
        return False, "Username part before '@' cannot be empty."
    if not domain_part:
        return False, "Domain part after '@' cannot be empty."
        
    # 4. Check local part starting character
    if not local_part[0].isalnum():
        return False, "Username must start with an alphanumeric character (letter or number)."
        
    # 5. Check local part characters
    # Allowed: alphanumeric, dot, underscore, percent, plus, hyphen
    if not re.match(r"^[a-zA-Z0-9._%+-]+$", local_part):
        return False, "Username contains invalid characters. Only letters, numbers, and . _ % + - are allowed."
        
    # 6. Check domain part for dot
    if "." not in domain_part:
        return False, "Domain part must contain a dot (e.g., '.com', '.org')."
        
    # 7. Check domain part characters
    # Allowed: alphanumeric, dot, hyphen
    if not re.match(r"^[a-zA-Z0-9.-]+$", domain_part):
        return False, "Domain contains invalid characters. Only letters, numbers, dots, and hyphens are allowed."
        
    # 8. Check top-level domain (TLD) length and characters
    # It must be the part after the last dot
    parts = domain_part.split(".")
    tld = parts[-1]
    
    if len(tld) < 2:
        return False, "Top-level domain (e.g. '.com', '.in') must be at least 2 characters long."
        
    if not tld.isalpha():
        return False, "Top-level domain must only contain letters."
        
    # If all manual checks pass, let's verify with the overall standard regex
    regex = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    if not re.match(regex, email):
        return False, "Email format is invalid according to standard validation rules."
        
    return True, "Email is valid!"

def main():
    print("=========================================")
    print("       Email Validator CLI Tool          ")
    print("=========================================")
    print("Type 'exit' or 'q' to quit.")
    print("-----------------------------------------")
    
    while True:
        email_input = input("Enter email to validate: ").strip()
        if email_input.lower() in ('exit', 'q'):
            print("Goodbye!")
            break
            
        if not email_input:
            print("[!] Please enter a value.")
            continue
            
        is_valid, reason = validate_email(email_input)
        
        if is_valid:
            print(f"[+] SUCCESS: '{email_input}' is a valid email address!")
        else:
            print(f"[-] INVALID: {reason}")
        print("-----------------------------------------")

if __name__ == "__main__":
    main()
