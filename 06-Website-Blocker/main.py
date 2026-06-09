import sys
import os
import time
import datetime
import ctypes
import re

# Marker comments to easily identify and clean up block rules we add
MARKER_START = "# BEGIN WEBSITE BLOCKER"
MARKER_END = "# END WEBSITE BLOCKER"
REDIRECT_IP = "127.0.0.1"

def is_admin():
    """Check if the script is running with administrative privileges."""
    try:
        if sys.platform.startswith("win"):
            return ctypes.windll.shell32.IsUserAnAdmin() != 0
        else:
            return os.getuid() == 0
    except Exception:
        return False

def get_hosts_path():
    """Get path to the OS hosts file."""
    if sys.platform.startswith("win"):
        return r"C:\Windows\System32\drivers\etc\hosts"
    else:
        return "/etc/hosts"

def parse_duration(duration_str):
    """Parse duration string like '30s', '10m', '1.5h', or '120' to seconds.
    Returns None if parsing fails.
    """
    duration_str = duration_str.strip().lower()
    
    # Try simple integer first (default to minutes)
    if duration_str.isdigit():
        return int(duration_str) * 60
        
    # Match pattern like 1.5h, 30m, 10s, etc.
    match = re.match(r"^([\d.]+)\s*([a-z]+)$", duration_str)
    if not match:
        return None
        
    value_str, unit = match.groups()
    try:
        val = float(value_str)
    except ValueError:
        return None
        
    if unit in ('s', 'sec', 'secs', 'second', 'seconds'):
        return int(val)
    elif unit in ('m', 'min', 'mins', 'minute', 'minutes'):
        return int(val * 60)
    elif unit in ('h', 'hr', 'hrs', 'hour', 'hours'):
        return int(val * 3600)
    else:
        return None

def remove_block_markers(content):
    """Remove the blocked content between and including our markers."""
    pattern = re.compile(rf"{re.escape(MARKER_START)}.*?{re.escape(MARKER_END)}\n?", re.DOTALL)
    return re.sub(pattern, "", content)

def block_websites(hosts_path, websites):
    """Add redirect entries to the hosts file."""
    try:
        with open(hosts_path, "r", encoding="utf-8") as file:
            content = file.read()
    except Exception as e:
        print(f"Error reading hosts file: {e}")
        return False

    # Check if the block markers are already present and clean them first
    if MARKER_START in content:
        content = remove_block_markers(content)

    # Prepare new block content
    block_lines = [MARKER_START]
    for site in websites:
        # Strip protocols or slashes if any
        site = re.sub(r"^https?://", "", site)
        site = site.split('/')[0].strip()
        if not site:
            continue
        
        # Add main website and the www version
        block_lines.append(f"{REDIRECT_IP} {site}")
        if not site.startswith("www."):
            block_lines.append(f"{REDIRECT_IP} www.{site}")
    
    block_lines.append(MARKER_END)
    block_block = "\n".join(block_lines)

    # Append to the end of the hosts file (or insert)
    # Ensure there's a newline before our block if hosts file doesn't end with one
    separator = "\n" if content and not content.endswith("\n") else ""
    new_content = content + separator + block_block + "\n"
    
    try:
        with open(hosts_path, "w", encoding="utf-8") as file:
            file.write(new_content)
        return True
    except Exception as e:
        print(f"Error writing to hosts file: {e}")
        return False

def unblock_websites(hosts_path):
    """Remove redirect entries from the hosts file."""
    try:
        with open(hosts_path, "r", encoding="utf-8") as file:
            content = file.read()
            
        if MARKER_START not in content:
            return True # Nothing to remove
            
        cleaned_content = remove_block_markers(content)
        
        with open(hosts_path, "w", encoding="utf-8") as file:
            file.write(cleaned_content)
        return True
    except Exception as e:
        print(f"Error removing blocks from hosts file: {e}")
        return False

def main():
    print("=========================================")
    print("       Website Blocker CLI Tool          ")
    print("=========================================")
    
    # Check privileges
    if not is_admin():
        print("[!] ERROR: This script requires administrative privileges.")
        if sys.platform.startswith("win"):
            print("    Please re-run this Command Prompt or PowerShell as Administrator.")
        else:
            print("    Please run this script using 'sudo python main.py'.")
        print("=========================================")
        sys.exit(1)

    hosts_path = get_hosts_path()
    
    # Get websites to block
    websites_input = input("Enter the websites to block (comma-separated, e.g., facebook.com, youtube.com):\n> ")
    websites = [w.strip() for w in websites_input.split(",") if w.strip()]
    if not websites:
        print("[!] No valid websites entered. Exiting.")
        sys.exit(0)

    # Get blocking duration
    while True:
        duration_input = input("Enter duration to block (e.g., '45m' for 45 minutes, '2h' for 2 hours, or just '45'):\n> ")
        duration_secs = parse_duration(duration_input)
        if duration_secs is not None and duration_secs > 0:
            break
        print("[!] Invalid duration format. Please try again.")

    end_time = datetime.datetime.now() + datetime.timedelta(seconds=duration_secs)
    print(f"\n[*] Target end time: {end_time.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"[*] Blocking: {', '.join(websites)}")
    print("[*] Applying block...")
    
    if not block_websites(hosts_path, websites):
        print("[!] Failed to block websites. Exiting.")
        sys.exit(1)
        
    print("[+] Websites blocked successfully!")
    print("[*] Press Ctrl+C to unblock websites and exit early.")
    print("-----------------------------------------")
    
    try:
        while True:
            remaining = end_time - datetime.datetime.now()
            if remaining.total_seconds() <= 0:
                break
                
            # Pretty print remaining time
            total_seconds = int(remaining.total_seconds())
            hours, remainder = divmod(total_seconds, 3600)
            mins, secs = divmod(remainder, 60)
            
            time_str = f"{mins:02d}:{secs:02d}"
            if hours > 0:
                time_str = f"{hours:02d}:{time_str}"
                
            sys.stdout.write(f"\rRemaining Time: {time_str}   ")
            sys.stdout.flush()
            time.sleep(1)
            
        print("\n\n[+] Time's up! Unblocking websites...")
        
    except KeyboardInterrupt:
        print("\n\n[*] Interrupted by user. Cleaning up and unblocking websites...")
    finally:
        if unblock_websites(hosts_path):
            print("[+] Cleanup complete. Websites are now accessible.")
        else:
            print("[!] Warning: Cleanup failed. Please check your hosts file manually.")
        print("=========================================")

if __name__ == "__main__":
    main()