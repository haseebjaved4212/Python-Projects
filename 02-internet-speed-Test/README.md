# Netflow Speedtest GUI App

A modern, sleek desktop application built in Python using the `customtkinter` framework and `speedtest-cli` API. It provides a visual dashboard to measure your internet download speed, upload speed, and network latency (ping) in real-time.

---

## Features

- **Premium Modern UI:** Built with `customtkinter` using a Slate-color palette (`slate-900`/`slate-50`), rounded dashboard cards, and clean typography.
- **Multi-Threaded Runner:** The test runs on a background worker thread (`threading.Thread`), keeping the graphical user interface completely responsive and preventing window freezing/lag.
- **Dynamic Theme Switcher:** Fully interactive Light Mode and Dark Mode toggle.
- **Stateful Progress Bar:** The progress bar shifts colors indicating current test phases (Download ➔ Upload ➔ Ping) and changes to Green when the network test successfully finishes.
- **Telemetry Indicators:** Displays clean cards for:
  - ⬇ **Download Speed** (in Mbps)
  - ⬆ **Upload Speed** (in Mbps)
  - ⚡ **Ping / Latency** (in ms)

---

## How It Works

1. **UI Initialization:** The app starts up using standard Tkinter event loops managed by CustomTkinter. It sets the default theme to Dark Mode.
2. **Worker Threading:** When you click **START SPEED TEST**, the main thread spawns a daemon background thread (`run_speed_test`). 
3. **Speedtest API Queries:** The background thread:
   - Fetches the closest and fastest Speedtest server via `get_best_server()`.
   - Starts a download binary stream test and measures bandwidth in Mbps.
   - Starts an upload binary stream test and measures bandwidth.
   - Measures packet latency (ping) in milliseconds.
4. **Main Loop Polling:** The main UI thread monitors state variables using `self.after(100, self.check_status)`, updating the status text and dashboard numbers as data becomes available in real-time.
5. **Completion state:** Once finished, the progress bar stops animating, turns solid green, and the test button becomes active again.

---

## Installation & Setup

### 1. Prerequisites
- Python 3.x

### 2. Install Required Packages
Install the required packages using pip:
```bash
pip install customtkinter speedtest-cli
```

*Note: Even though the library is installed via pip as `speedtest-cli`, it is imported inside Python as `import speedtest`.*

---

## How to Run

1. Open your terminal or command prompt.
2. Navigate to the project directory:
   ```bash
   cd "C:\Users\DELL\OneDrive\Desktop\Python Projects\02-internet-speed-Test"
   ```
3. Run the application:
   ```bash
   python main.py
   ```

---

## Troubleshooting

- **Speedtest Errors / Timeouts:**
  If you receive a connection error, it might be due to speedtest-cli server restrictions.
  The code initiates the speedtest client using `secure=True`:
  ```python
  st = speedtest.Speedtest(secure=True)
  ```
  This forces SSL/HTTPS requests, which prevents standard HTTP certificate blocks and handshake errors on modern networks. Ensure you have an active internet connection when running the test.
