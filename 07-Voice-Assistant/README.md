# 🎙️ Antigravity AI Voice Assistant

An elegant, desktop-integrated Voice Assistant built with a **Flask backend** and a premium, glassmorphism **HTML/CSS/JS frontend**. It features real-time Windows OS integration, hardware stat monitoring, screen capture controls, and conversational intelligence powered by Google's Gemini API.

---

## 🌟 Visual & Interactive Features

- **Siri-Style Canvas Wave Visualizer:** A mathematically animated wave on an HTML5 canvas that dynamically adapts its color, frequency, and height depending on the assistant's state (`IDLE`, `LISTENING`, `THINKING`, or `SPEAKING`).
- **Interactive Chat Console:** A scrollable interface displaying a transcription log of the user's commands and the assistant's replies.
- **Hardware Metrics Widget:** Instantly retrieves CPU usage, RAM utilization, and battery status, rendering them as customized progress meters in the console.
- **Screen Capture Lightbox:** Snaps screenshots on demand and displays a thumbnail in the chat log, which opens in an overlay modal when clicked.
- **Persistent Settings Drawer:** Allows you to input your Gemini API Key (stored securely in browser `localStorage`), select from a list of available system text-to-speech voices, and refer to shortcut command guides.

---

## 📂 Project Architecture

Here is an overview of the role each file plays in the application:

```
07-Voice-Assistant/
├── static/
│   ├── screenshots/  # Stores generated desktop screen captures
│   ├── script.js     # Handles audio visualizer loop, Web Speech APIs, & API routes
│   └── style.css     # CSS rules for dark cyberpunk theme & animations
├── templates/
│   └── index.html    # Core dashboard structure and settings panel
├── app.py            # Flask web server routing APIs & API keys
├── main.py           # Program entry point that fires up Flask and opens the browser
└── system_commands.py# OS level tools (app launching, volume keys, system statistics)
```

### File Breakdown

* **main.py**: The entry point. Spawns a background thread to wait for the Flask server to initialize, then launches your default web browser directly to the dashboard, ensuring a zero-configuration start.
* **app.py**: The Flask router. Directs user commands to local OS tasks. If a command cannot be executed locally, it routes the text to the Google Gemini API (if an API key is provided) to fetch an AI-generated chat response.
* **system_commands.py**: Houses OS-specific integration routines. Simulates hardware media and volume keystrokes using standard Windows APIs (`ctypes`), runs shell commands to read hardware performance metrics (`wmic`), maps shortcuts to launch system programs, and captures images using `pyautogui`.
* **templates/index.html**: The dashboard markup, referencing styling and script sheets. Integrates Google Fonts ("Outfit" and "Inter") and FontAwesome vectors.
* **static/style.css**: Tailors the space-black interface. Utilizes glassmorphism properties (blur overlays, borders, inner shadows) alongside pulsing animation triggers for states.
* **static/script.js**: Orchestrates the frontend. Runs the `webkitSpeechRecognition` loop to capture real-time user voice, schedules audio output utilizing the local browser's `speechSynthesis` engine, and updates the canvas visualizer waves.

---

## 🛠️ How It Works Under the Hood

The Voice Assistant utilizes a hybrid architecture:
1. **Speech-to-Text (STT):** Handles speech transcription on the client side using the browser's native **Web Speech API** (`SpeechRecognition`). This provides high accuracy, supports multiple languages, and avoids heavy PyAudio dependencies in Python.
2. **Command Processing:** Transcribed text is sent to the local Flask server (`/api/command`). The server parses the input against predefined OS controls or routes it to the **Gemini 1.5 Flash** API for general conversations.
3. **Text-to-Speech (TTS):** The text response is read aloud by the browser's native **SpeechSynthesis** engine. This lets the user choose between multiple natural-sounding system voices from a dropdown menu.

---

## 🚀 Setup Instructions

Follow these steps to set up and run the Voice Assistant on your local device:

### Prerequisites
- **Python 3.8 or higher** installed on your machine.
- A modern web browser that supports the Web Speech API (e.g., **Google Chrome**, **Microsoft Edge**, or **Opera**).

### Step 1: Install Dependencies
Open a command prompt or terminal in the `07-Voice-Assistant` directory and install the required Python packages:

```bash
pip install Flask pyautogui wikipedia requests pillow
```

*Note: These libraries handle the web server, system automation shortcuts, Wikipedia summaries, API requests, and image output.*

### Step 2: Launch the Assistant
Run the main script using Python:

```bash
python main.py
```

The script will:
- Initialize the Flask backend.
- Automatically launch a browser window opening to the URL: `http://127.0.0.1:5000`.

---

## 🗣️ Voice Commands to Try

Once the dashboard is open in your browser, click the **Microphone Button** (or press the **Spacebar** while your text cursor is inactive) and speak:

| Command | Action |
| :--- | :--- |
| **"Open notepad"** / **"Open calculator"** | Launches the respective Windows desktop application. |
| **"Volume up"** / **"Volume down"** / **"Mute"** | Dynamically changes the master volume of your system. |
| **"Take a screenshot"** | Captures the screen, saves it, and shows a clickable lightbox thumbnail. |
| **"System status"** / **"CPU usage"** / **"Battery"** | Displays a card with CPU load, RAM allocation, and charge levels. |
| **"Wikipedia Albert Einstein"** | Fetches and reads a 2-sentence summary of the page. |
| **"Search Google for [topic]"** | Automatically opens Google search for the queried topic in a new tab. |
| **"Search YouTube for [topic]"** | Opens YouTube search for the query in a new tab. |
| **"Time"** / **"Date"** | Informs you of the local time and current date. |

### Adding Gemini AI Capabilities
To ask general questions (e.g., *"Write a Python print function"* or *"What is the distance to the moon?"*):
1. Click the **Sliders icon** (top right) to open the Settings Panel.
2. Enter your **Gemini API Key** (obtainable from Google AI Studio).
3. Click **Save Key**. The assistant will now automatically use Gemini Flash to respond to any complex conversational query.
