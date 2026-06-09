# Website Blocker CLI Tool

A lightweight, interactive command-line utility written in Python that allows you to block access to specific websites for a customized duration. The tool automatically handles operating system differences, verifies administrator permissions, displays a live countdown timer, and cleanly restores access when the block duration expires or the program is interrupted.

---

## Features

- **Interactive Inputs:** Prompt-driven setup lets you specify which websites to block and for how long.
- **Flexible Durations:** Supports units like seconds (`s`), minutes (`m`), or hours (`h`) (e.g., `30s`, `45m`, `1.5h`, or integers which default to minutes).
- **Safe Block Boundaries:** Uses special marker comments (`# BEGIN WEBSITE BLOCKER` and `# END WEBSITE BLOCKER`) to safely inject and remove blocked domain rules without touching any pre-existing rules.
- **Cross-Platform:** Automatically locates the standard `hosts` file on Windows (`C:\Windows\System32\drivers\etc\hosts`) and Unix-like OSes (`/etc/hosts`).
- **Permission Guard:** Checks for Administrative (Windows) or Root (macOS/Linux) privileges on startup and warns the user if they are missing.
- **Graceful Termination:** Restores site access automatically when the countdown finishes or if you interrupt the process (e.g., hitting `Ctrl+C`).

---

## How It Works

Operating systems resolve domain names (like `facebook.com`) into IP addresses using local lookup rules before checking online DNS servers. The first place the OS checks is the local `hosts` file.

When you run this script:
1. It requests admin privileges (needed to edit system configurations).
2. It parses your input websites and the blocking duration.
3. It appends redirect entries (e.g., `127.0.0.1 facebook.com` and `127.0.0.1 www.facebook.com`) into your system's `hosts` file.
4. Any requests made to those domains are redirected to your local machine (`127.0.0.1`), effectively blocking access.
5. Once the timer ends or you interrupt the script via `Ctrl+C`, the script cleanly removes the block lines and restores the original `hosts` file content.

---

## Prerequisites

- **Python 3.x** must be installed.
- **Administrative Privileges:** The terminal or console running the script **must** be run as Administrator (Windows) or with `sudo` (macOS/Linux).

---

## Usage Instructions

### 1. Open Terminal as Administrator

- **Windows:**
  - Press the `Windows Key`, search for `Command Prompt` or `PowerShell`.
  - Right-click it and select **Run as administrator**.
  - Navigate to the project directory:
    ```powershell
    cd "C:\Users\DELL\OneDrive\Desktop\Python Projects\06-Website-Blocker"
    ```

- **macOS / Linux:**
  - Open your Terminal.
  - Navigate to the directory:
    ```bash
    cd "/path/to/Python Projects/06-Website-Blocker"
    ```

### 2. Run the Script

- **Windows:**
  ```powershell
  python main.py
  ```

- **macOS / Linux:**
  ```bash
  sudo python3 main.py
  ```

### 3. Enter Inputs

1. **Websites:** Type a comma-separated list of domains to block.
   ```
   Enter the websites to block (comma-separated, e.g., facebook.com, youtube.com):
   > facebook.com, youtube.com
   ```
2. **Duration:** Specify how long to block the websites.
   ```
   Enter duration to block (e.g., '45m' for 45 minutes, '2h' for 2 hours, or just '45'):
   > 1.5h
   ```

### 4. Countdown and Termination

The console will display a real-time countdown timer:
```
Remaining Time: 01:29:55
```
- **To unblock early:** Press `Ctrl+C` at any time. The script will automatically clean up the `hosts` file and exit.
- **To unblock automatically:** Let the countdown reach `00:00`. The script will restore access and exit.

---

## Troubleshooting & Notes

- **DNS Caching:** Some browsers cache DNS lookups for a few minutes. If a blocked website is still loading immediately after starting the blocker, try opening an incognito/private window, restarting the browser, or flushing your DNS cache:
  - **Windows:** Open Command Prompt and run `ipconfig /flushdns`
  - **macOS:** Open Terminal and run `sudo dscacheutil -flushcache; sudo killall -HUP mDNSResponder`
- **Manual Cleanup:** If the script or your machine crashes unexpectedly while websites are blocked, your hosts file may retain the block entries. Simply open your `hosts` file in a text editor (as Admin) and remove the lines between `# BEGIN WEBSITE BLOCKER` and `# END WEBSITE BLOCKER`.
