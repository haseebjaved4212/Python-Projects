# Instagram Automation CLI Tool

An interactive, command-line interface (CLI) application built in Python that leverages the `instabot` library to automate common Instagram tasks. The tool secure-prompts for login credentials and provides a menu-driven interface to perform actions like following/unfollowing accounts, sending direct messages, uploading photos, and automatically liking user posts.

---

## Features

- **Secure Login:** Uses the Python standard library `getpass` module to hide your password input as you type, preventing shoulder surfing.
- **Interactive Menu:** Simple numbered menu system to execute specific tasks without restarting the script.
- **Task Automation:**
  1. **Follow User:** Automatically follow any target account by username.
  2. **Unfollow User:** Automatically unfollow any target account.
  3. **Direct Messaging (DM):** Send a text message to a specified user.
  4. **Photo Upload:** Upload `.jpg` images with custom captions.
  5. **Auto-Liking:** Automatically like posts on a target user's feed.
- **Clean Session Teardown:** Performs a proper logout sequence on exit.

---

## How It Works

Under the hood, the project uses the **`instabot`** package. 
1. **API Simulation:** `instabot` mimics the requests made by the official Instagram Android app (acting as a mobile device).
2. **Session Persistence:** When you successfully log in, `instabot` creates a directory named `config/` in the script's folder. This directory stores session tokens and cookies.
3. **Execution:** When you pick a menu action, the bot makes the corresponding API request using the stored active session.
4. **Logout:** When choosing option `6`, the script calls `bot.logout()`, which invalidates the session token on Instagram's server and cleanly exits.

---

## Installation & Setup

### 1. Prerequisites
- Python 3.6 to 3.9 is recommended (some newer versions of Python might require additional troubleshooting due to dependency issues with older versions of `instabot`).

### 2. Install Dependencies
Install the required `instabot` package using `pip`:
```bash
pip install instabot
```

*Note: If you run into issues installing `instabot`, make sure your `pip` is up to date (`python -m pip install --upgrade pip`) and that you have a C++ compiler installed (e.g., Build Tools for Visual Studio on Windows).*

---

## How to Use

### 1. Run the script:
Navigate to the project directory in your terminal and run:
```bash
python main.py
```

### 2. Enter Credentials:
- Input your Instagram Username.
- Input your Instagram Password (characters will not show on the screen as you type).

### 3. Choose Task:
Select a number from the menu (e.g., `1` to `6`) and follow the on-screen prompts for target usernames or messages.

---

## ⚠️ Important Safety Warnings & Disclaimers

> [!WARNING]
> **Use at Your Own Risk:**
> Instagram has strict policies against automation and bots. Using automation tools can result in action blocks, temporary restrictions, or permanent suspension of your Instagram account.

- **Use Test Accounts:** It is highly recommended to test this tool using a secondary/throwaway account rather than your primary personal or business account.
- **Observe Rate Limits:** Do not trigger too many commands in rapid succession. Instagram monitors accounts for unnaturally fast behavior.

---

## Troubleshooting

### "Login Failed / Cookie Error"
If you fail to login or change accounts, `instabot` will often throw errors because of existing cached session cookies. 
- **Solution:** Delete the `config` folder created in the `05-Instagram-Automation` directory.
  - On Windows: Run `rmdir /s /q config` or delete the folder via File Explorer.
  - On macOS/Linux: Run `rm -rf config/`.
- Then, re-run `python main.py`.
