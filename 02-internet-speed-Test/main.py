from tkinter import *

import speedtest



window = Tk()
window.title("Internet Speed Test")
window.geometry("500x500")
window.resizable(False, False)
window.configure(bg="white")

label = Label(window, text="Internet Speed Test", font=("Arial", 24, "bold"))
label.pack(pady=20)

button = Button(window, text="Test Speed", font=("Arial", 18, "bold"), command=lambda: test_speed())
button.pack(pady=20)

def test_speed():
    label.config(text="Testing download speed...")
    window.update()
    
    speed = speedtest.Speedtest()
    speed.get_best_server()
    
    download_speed = speed.download() / 1_000_000  # Convert bits/s to Mbps
    
    label.config(text="Testing upload speed...")
    window.update()
    
    upload_speed = speed.upload() / 1_000_000  # Convert bits/s to Mbps
    ping = speed.results.ping
    
    label.config(
        text=f"Download: {download_speed:.2f} Mbps\n"
             f"Upload: {upload_speed:.2f} Mbps\n"
             f"Ping: {ping} ms"
    )

window.mainloop()

