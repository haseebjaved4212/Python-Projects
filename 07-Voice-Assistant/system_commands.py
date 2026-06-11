import os
import re
import subprocess
import ctypes
import datetime
import webbrowser
import pyautogui
import wikipedia

# Set Wikipedia language
wikipedia.set_lang("en")

# Virtual key codes for volume and media controls
VK_VOLUME_MUTE = 0xAD
VK_VOLUME_DOWN = 0xAE
VK_VOLUME_UP = 0xAF
VK_MEDIA_NEXT_TRACK = 0xB0
VK_MEDIA_PREV_TRACK = 0xB1
VK_MEDIA_PLAY_PAUSE = 0xB3

def press_key(vk_code):
    """Simulates a key press and release for a virtual key code."""
    ctypes.windll.user32.keybd_event(vk_code, 0, 0, 0)      # Key down
    ctypes.windll.user32.keybd_event(vk_code, 0, 2, 0)      # Key up

def get_cpu_usage():
    """Gets current CPU usage percentage using wmic."""
    try:
        output = subprocess.check_output("wmic cpu get LoadPercentage", shell=True).decode()
        numbers = re.findall(r'\d+', output)
        if numbers:
            return int(numbers[0])
    except Exception as e:
        print(f"Error fetching CPU usage: {e}")
    return 0

def get_ram_usage():
    """Gets current RAM usage percentage using wmic."""
    try:
        output = subprocess.check_output("wmic OS get FreePhysicalMemory,TotalVisibleMemorySize /Value", shell=True).decode()
        lines = output.strip().split('\n')
        free_kb = 0
        total_kb = 0
        for line in lines:
            if 'FreePhysicalMemory' in line:
                match = re.search(r'\d+', line)
                if match:
                    free_kb = int(match.group())
            elif 'TotalVisibleMemorySize' in line:
                match = re.search(r'\d+', line)
                if match:
                    total_kb = int(match.group())
        if total_kb > 0:
            used_kb = total_kb - free_kb
            return round((used_kb / total_kb) * 100, 1)
    except Exception as e:
        print(f"Error fetching RAM usage: {e}")
    return 0

def get_battery_info():
    """Gets battery percentage and charging status using wmic."""
    try:
        # Get battery percentage
        pct_output = subprocess.check_output("wmic path Win32_Battery get EstimatedChargeRemaining", shell=True).decode()
        pct_match = re.findall(r'\d+', pct_output)
        percent = int(pct_match[0]) if pct_match else None

        # Get battery status (charging vs discharging)
        status_output = subprocess.check_output("wmic path Win32_Battery get BatteryStatus", shell=True).decode()
        status_match = re.findall(r'\d+', status_output)
        status_code = int(status_match[0]) if status_match else None
        
        charging = False
        if status_code in [2, 6, 7, 8]: # Charging, partially charged, etc.
            charging = True
            
        return {"percent": percent, "charging": charging}
    except Exception as e:
        print(f"Error fetching Battery status: {e}")
    return {"percent": None, "charging": False}

def take_screenshot(static_dir):
    """Takes a screenshot and saves it to the static directory, returning the URL path."""
    try:
        screenshots_dir = os.path.join(static_dir, "screenshots")
        os.makedirs(screenshots_dir, exist_ok=True)
        
        filename = f"screenshot_{int(datetime.datetime.now().timestamp())}.png"
        filepath = os.path.join(screenshots_dir, filename)
        
        # Take the screenshot and save
        pyautogui.screenshot(filepath)
        
        return {
            "success": True, 
            "url": f"/static/screenshots/{filename}",
            "message": "Screenshot captured successfully!"
        }
    except Exception as e:
        return {"success": False, "message": f"Failed to capture screenshot: {str(e)}"}

def open_app(app_name):
    """Launches common Windows applications."""
    app_map = {
        "notepad": "notepad.exe",
        "calculator": "calc.exe",
        "calc": "calc.exe",
        "paint": "mspaint.exe",
        "mspaint": "mspaint.exe",
        "cmd": "cmd.exe",
        "command prompt": "cmd.exe",
        "explorer": "explorer.exe",
        "file explorer": "explorer.exe",
        "task manager": "taskmgr.exe",
        "taskmgr": "taskmgr.exe",
        "word": "start winword",
        "excel": "start excel",
        "powerpoint": "start powerpnt",
        "vscode": "code",
        "vs code": "code",
        "browser": "start msedge",
        "edge": "start msedge",
        "settings": "start ms-settings:"
    }
    
    app_name_lower = app_name.lower().strip()
    
    # Check if we have a direct mapping
    if app_name_lower in app_map:
        try:
            cmd_to_run = app_map[app_name_lower]
            if cmd_to_run.startswith("start "):
                os.system(cmd_to_run)
            else:
                subprocess.Popen(cmd_to_run)
            return f"Opening {app_name}."
        except Exception as e:
            return f"Failed to open {app_name}. Error: {str(e)}"
            
    # Fallback to standard web applications or system utilities
    if "chrome" in app_name_lower:
        try:
            os.system("start chrome")
            return "Opening Google Chrome."
        except:
            webbrowser.get('windows-default').open('https://www.google.com')
            return "Opening Google Chrome fallback."
            
    elif "youtube" in app_name_lower:
        webbrowser.open("https://www.youtube.com")
        return "Opening YouTube."
        
    elif "spotify" in app_name_lower:
        try:
            os.system("start spotify")
            return "Opening Spotify."
        except:
            webbrowser.open("https://open.spotify.com")
            return "Opening Spotify web."
            
    # Attempt to open via Windows "start" command as a fallback
    try:
        subprocess.Popen(f"start {app_name_lower}", shell=True)
        return f"Attempting to open {app_name}."
    except:
        pass
        
    return f"Sorry, I don't know how to open '{app_name}' yet. You can add it to my configurations!"

def search_wikipedia(query):
    """Searches Wikipedia for a query and returns a summary."""
    try:
        # Clean search term
        cleaned_query = re.sub(r'\b(who is|what is|search wikipedia for|search wikipedia|wikipedia)\b', '', query, flags=re.IGNORECASE).strip()
        summary = wikipedia.summary(cleaned_query, sentences=2)
        return {"success": True, "text": summary, "source": "Wikipedia"}
    except wikipedia.exceptions.DisambiguationError as e:
        # Return first option
        try:
            summary = wikipedia.summary(e.options[0], sentences=2)
            return {"success": True, "text": f"Multiple options found. Here is info on {e.options[0]}: {summary}", "source": "Wikipedia"}
        except:
            return {"success": False, "message": "The search term was ambiguous. Please be more specific."}
    except wikipedia.exceptions.PageError:
        return {"success": False, "message": "I couldn't find any Wikipedia page matching that description."}
    except Exception as e:
        return {"success": False, "message": f"An error occurred while searching Wikipedia: {str(e)}"}

def process_command(command, static_dir):
    """Parses natural language input and runs corresponding system commands."""
    cmd = command.lower().strip()
    
    # 1. System Statistics
    if any(k in cmd for k in ["system status", "system stats", "hardware stats", "how is my computer"]):
        cpu = get_cpu_usage()
        ram = get_ram_usage()
        bat = get_battery_info()
        bat_str = f"Battery is at {bat['percent']}%" + (" (Charging)" if bat["charging"] else "") if bat["percent"] is not None else "Battery info unavailable"
        msg = f"Your system stats are: CPU usage is at {cpu}%, RAM usage is at {ram}%, and {bat_str}."
        return {"type": "info", "message": msg, "data": {"cpu": cpu, "ram": ram, "battery": bat}}
        
    elif "cpu usage" in cmd or "cpu status" in cmd:
        cpu = get_cpu_usage()
        return {"type": "info", "message": f"Your CPU usage is currently {cpu}%.", "data": {"cpu": cpu}}
        
    elif "ram usage" in cmd or "memory usage" in cmd or "ram status" in cmd:
        ram = get_ram_usage()
        return {"type": "info", "message": f"Your RAM usage is currently {ram}%.", "data": {"ram": ram}}
        
    elif "battery" in cmd:
        bat = get_battery_info()
        if bat["percent"] is not None:
            state = "charging" if bat["charging"] else "discharging"
            return {"type": "info", "message": f"Your battery is at {bat['percent']}% and is currently {state}.", "data": {"battery": bat}}
        return {"type": "error", "message": "I couldn't read the battery status."}

    # 2. System Commands (Volume & Media)
    elif "volume up" in cmd or "increase volume" in cmd:
        # Increase volume a few steps
        for _ in range(5):
            press_key(VK_VOLUME_UP)
        return {"type": "action", "message": "Volume increased."}
        
    elif "volume down" in cmd or "decrease volume" in cmd:
        for _ in range(5):
            press_key(VK_VOLUME_DOWN)
        return {"type": "action", "message": "Volume decreased."}
        
    elif "mute" in cmd or "unmute" in cmd:
        press_key(VK_VOLUME_MUTE)
        return {"type": "action", "message": "Volume mute status toggled."}
        
    elif "play" in cmd and "music" in cmd and "pause" in cmd:
        press_key(VK_MEDIA_PLAY_PAUSE)
        return {"type": "action", "message": "Media playback toggled."}
    elif "pause" in cmd or "stop music" in cmd:
        press_key(VK_MEDIA_PLAY_PAUSE)
        return {"type": "action", "message": "Media playback paused."}
    elif "next track" in cmd or "next song" in cmd:
        press_key(VK_MEDIA_NEXT_TRACK)
        return {"type": "action", "message": "Skipping to next track."}
    elif "previous track" in cmd or "previous song" in cmd:
        press_key(VK_MEDIA_PREV_TRACK)
        return {"type": "action", "message": "Going back to previous track."}

    # 3. Screenshot
    elif "screenshot" in cmd or "capture screen" in cmd or "take a picture of the screen" in cmd:
        result = take_screenshot(static_dir)
        if result["success"]:
            return {
                "type": "screenshot",
                "message": "I've taken a screenshot of your screen.",
                "url": result["url"]
            }
        return {"type": "error", "message": result["message"]}

    # 4. Open Apps
    elif "open " in cmd:
        match = re.search(r'open\s+(.+)', cmd)
        if match:
            app_name = match.group(1).strip()
            msg = open_app(app_name)
            return {"type": "action", "message": msg}

    # 5. Launch Websites directly
    elif "google" in cmd and ("search" in cmd or cmd.startswith("google ")):
        match = re.search(r'(?:search\s+(?:on\s+)?google\s+(?:for\s+)?|google\s+)(.+)', cmd)
        search_query = match.group(1).strip() if match else cmd.replace("search on google", "").replace("search google", "").replace("google", "").strip()
        url = f"https://www.google.com/search?q={search_query.replace(' ', '+')}"
        webbrowser.open(url)
        return {"type": "action", "message": f"Searching Google for '{search_query}' in your browser."}
        
    elif "youtube" in cmd and ("search" in cmd or cmd.startswith("youtube ")):
        match = re.search(r'(?:search\s+(?:on\s+)?youtube\s+(?:for\s+)?|youtube\s+)(.+)', cmd)
        search_query = match.group(1).strip() if match else cmd.replace("search on youtube", "").replace("search youtube", "").replace("youtube", "").strip()
        url = f"https://www.youtube.com/results?search_query={search_query.replace(' ', '+')}"
        webbrowser.open(url)
        return {"type": "action", "message": f"Searching YouTube for '{search_query}'."}

    # 6. Wikipedia Lookup
    elif "wikipedia" in cmd or cmd.startswith("who is ") or cmd.startswith("what is "):
        wiki_res = search_wikipedia(command)
        if wiki_res["success"]:
            return {"type": "info", "message": wiki_res["text"]}
        else:
            # Fallback to simple Google Search if Wikipedia fails and it's a general question
            if cmd.startswith("who is ") or cmd.startswith("what is "):
                search_query = command.strip()
                url = f"https://www.google.com/search?q={search_query.replace(' ', '+')}"
                webbrowser.open(url)
                return {"type": "info", "message": f"I couldn't find a direct article, but I've opened a Google search for '{search_query}'."}
            return {"type": "error", "message": wiki_res["message"]}

    # 7. Basic Conversations & Time
    elif "time" in cmd:
        now = datetime.datetime.now().strftime("%I:%M %p")
        return {"type": "info", "message": f"The current time is {now}."}
        
    elif "date" in cmd or "today" in cmd:
        today = datetime.datetime.now().strftime("%A, %B %d, %Y")
        return {"type": "info", "message": f"Today is {today}."}

    # If it falls through, return none so we can route it to LLM in the main server
    return None
