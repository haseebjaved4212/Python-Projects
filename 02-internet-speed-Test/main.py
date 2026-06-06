import tkinter as tk
import customtkinter as ctk
import speedtest
import threading

# Set window appearance and theme
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class SpeedTestApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        # Configure window
        self.title("Internet Speed Test")
        self.geometry("620x520")
        self.resizable(False, False)
        
        # Color definitions for aesthetics
        self.bg_color_dark = "#0F172A"      # Slate 900
        self.bg_color_light = "#F8FAFC"     # Slate 50
        
        self.card_bg_dark = "#1E293B"       # Slate 800
        self.card_bg_light = "#FFFFFF"      # White
        
        self.text_muted_dark = "#94A3B8"    # Slate 400
        self.text_muted_light = "#64748B"   # Slate 500
        
        self.accent_download = "#0EA5E9"    # Cyan 500
        self.accent_upload = "#8B5CF6"      # Violet 500
        self.accent_ping = "#F59E0B"        # Amber 500
        
        self.configure(fg_color=(self.bg_color_light, self.bg_color_dark))
        
        # Speedtest state variables
        self.download_val = 0.0
        self.upload_val = 0.0
        self.ping_val = 0.0
        self.status_msg = "Ready to test"
        self.testing = False
        
        # Setup UI
        self.create_widgets()
        
    def create_widgets(self):
        # --- HEADER ---
        self.header_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.header_frame.pack(fill="x", padx=30, pady=(30, 20))
        
        self.title_label = ctk.CTkLabel(
            self.header_frame, 
            text="NETFLOW SPEEDTEST", 
            font=("Segoe UI", 24, "bold"),
            text_color=("#1E293B", "#F1F5F9")
        )
        self.title_label.pack(side="left")
        
        # Theme Switch
        self.theme_switch = ctk.CTkSwitch(
            self.header_frame,
            text="Dark Mode",
            command=self.toggle_theme,
            font=("Segoe UI", 12),
            text_color=(self.text_muted_light, self.text_muted_dark)
        )
        self.theme_switch.pack(side="right")
        self.theme_switch.select() # Start in Dark Mode
        
        # --- DASHBOARD (CARDS) ---
        self.dashboard_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.dashboard_frame.pack(fill="x", padx=30, pady=10)
        
        # Configure columns equally
        self.dashboard_frame.columnconfigure((0, 1, 2), weight=1, uniform="equal")
        
        # DOWNLOAD CARD
        self.dl_card = ctk.CTkFrame(
            self.dashboard_frame, 
            fg_color=(self.card_bg_light, self.card_bg_dark),
            border_width=2,
            border_color=self.accent_download,
            corner_radius=12
        )
        self.dl_card.grid(row=0, column=0, padx=8, pady=5, sticky="nsew")
        
        self.dl_title = ctk.CTkLabel(
            self.dl_card,
            text="⬇ DOWNLOAD",
            font=("Segoe UI", 13, "bold"),
            text_color=self.accent_download
        )
        self.dl_title.pack(pady=(15, 5))
        
        self.dl_value_label = ctk.CTkLabel(
            self.dl_card,
            text="--",
            font=("Segoe UI", 36, "bold"),
            text_color=("#0F172A", "#FFFFFF")
        )
        self.dl_value_label.pack(pady=5)
        
        self.dl_unit = ctk.CTkLabel(
            self.dl_card,
            text="Mbps",
            font=("Segoe UI", 12),
            text_color=(self.text_muted_light, self.text_muted_dark)
        )
        self.dl_unit.pack(pady=(0, 15))
        
        # UPLOAD CARD
        self.ul_card = ctk.CTkFrame(
            self.dashboard_frame,
            fg_color=(self.card_bg_light, self.card_bg_dark),
            border_width=2,
            border_color=self.accent_upload,
            corner_radius=12
        )
        self.ul_card.grid(row=0, column=1, padx=8, pady=5, sticky="nsew")
        
        self.ul_title = ctk.CTkLabel(
            self.ul_card,
            text="⬆ UPLOAD",
            font=("Segoe UI", 13, "bold"),
            text_color=self.accent_upload
        )
        self.ul_title.pack(pady=(15, 5))
        
        self.ul_value_label = ctk.CTkLabel(
            self.ul_card,
            text="--",
            font=("Segoe UI", 36, "bold"),
            text_color=("#0F172A", "#FFFFFF")
        )
        self.ul_value_label.pack(pady=5)
        
        self.ul_unit = ctk.CTkLabel(
            self.ul_card,
            text="Mbps",
            font=("Segoe UI", 12),
            text_color=(self.text_muted_light, self.text_muted_dark)
        )
        self.ul_unit.pack(pady=(0, 15))
        
        # PING CARD
        self.ping_card = ctk.CTkFrame(
            self.dashboard_frame,
            fg_color=(self.card_bg_light, self.card_bg_dark),
            border_width=2,
            border_color=self.accent_ping,
            corner_radius=12
        )
        self.ping_card.grid(row=0, column=2, padx=8, pady=5, sticky="nsew")
        
        self.ping_title = ctk.CTkLabel(
            self.ping_card,
            text="⚡ PING",
            font=("Segoe UI", 13, "bold"),
            text_color=self.accent_ping
        )
        self.ping_title.pack(pady=(15, 5))
        
        self.ping_value_label = ctk.CTkLabel(
            self.ping_card,
            text="--",
            font=("Segoe UI", 36, "bold"),
            text_color=("#0F172A", "#FFFFFF")
        )
        self.ping_value_label.pack(pady=5)
        
        self.ping_unit = ctk.CTkLabel(
            self.ping_card,
            text="ms",
            font=("Segoe UI", 12),
            text_color=(self.text_muted_light, self.text_muted_dark)
        )
        self.ping_unit.pack(pady=(0, 15))
        
        # --- ACTION PANEL ---
        self.action_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.action_frame.pack(fill="x", padx=38, pady=(30, 20))
        
        # Progress Bar
        self.progress_bar = ctk.CTkProgressBar(
            self.action_frame, 
            height=10, 
            corner_radius=5,
            progress_color=self.accent_download
        )
        self.progress_bar.pack(fill="x", pady=10)
        self.progress_bar.set(0.0)
        
        # Status message
        self.status_label = ctk.CTkLabel(
            self.action_frame,
            text="Ready to measure network speeds.",
            font=("Segoe UI", 13, "italic"),
            text_color=(self.text_muted_light, self.text_muted_dark)
        )
        self.status_label.pack(pady=10)
        
        # Start Button
        self.start_button = ctk.CTkButton(
            self.action_frame,
            text="START SPEED TEST",
            font=("Segoe UI", 15, "bold"),
            height=50,
            corner_radius=25,
            fg_color="#4F46E5", # Indigo 600
            hover_color="#4338CA", # Indigo 700
            command=self.start_test_thread
        )
        self.start_button.pack(fill="x", pady=(10, 0))
        
    def toggle_theme(self):
        if self.theme_switch.get() == 1:
            ctk.set_appearance_mode("dark")
        else:
            ctk.set_appearance_mode("light")
            
    def start_test_thread(self):
        # Reset UI
        self.download_val = 0.0
        self.upload_val = 0.0
        self.ping_val = 0.0
        
        self.dl_value_label.configure(text="--")
        self.ul_value_label.configure(text="--")
        self.ping_value_label.configure(text="--")
        
        self.testing = True
        self.status_msg = "Initializing speed test..."
        self.status_label.configure(text=self.status_msg)
        
        # Set button state
        self.start_button.configure(state="disabled", text="TEST RUNNING...")
        
        # Start progress bar animation
        self.progress_bar.set(0.0)
        self.progress_bar.start()
        
        # Spawn test in a thread
        self.test_thread = threading.Thread(target=self.run_speed_test, daemon=True)
        self.test_thread.start()
        
        # Check thread status regularly
        self.check_status()
        
    def run_speed_test(self):
        try:
            self.status_msg = "Finding the best server..."
            st = speedtest.Speedtest(secure=True)
            st.get_best_server()
            
            # Ping
            self.ping_val = st.results.ping
            
            # Download
            self.status_msg = "Testing download speed..."
            self.download_val = st.download() / 1_000_000
            
            # Upload
            self.status_msg = "Testing upload speed..."
            self.upload_val = st.upload() / 1_000_000
            
            self.status_msg = "Network test completed successfully!"
        except Exception as e:
            self.status_msg = "Error: Unable to run test. Check connection."
            print(f"Speedtest Error: {e}")
        finally:
            self.testing = False
            
    def check_status(self):
        # Update display from state variables
        self.status_label.configure(text=self.status_msg)
        
        if self.download_val > 0:
            self.dl_value_label.configure(text=f"{self.download_val:.2f}")
        if self.ul_value_label._text == "--" and self.download_val > 0:
            # If download has finished, show progress color of progressbar as upload color
            self.progress_bar.configure(progress_color=self.accent_upload)
            
        if self.upload_val > 0:
            self.ul_value_label.configure(text=f"{self.upload_val:.2f}")
            self.progress_bar.configure(progress_color=self.accent_ping)
            
        if self.ping_val > 0:
            self.ping_value_label.configure(text=f"{self.ping_val:.0f}")
            
        if self.testing:
            # Recheck after 100ms
            self.after(100, self.check_status)
        else:
            # Test finished or errored
            self.progress_bar.stop()
            self.progress_bar.set(1.0)
            self.progress_bar.configure(progress_color="#10B981") # Green on completion
            self.start_button.configure(state="normal", text="START SPEED TEST")

if __name__ == "__main__":
    app = SpeedTestApp()
    app.mainloop()
