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
    speed = speedtest.Speedtest()
    speed.get_best_server()
    speed.download()
    speed.upload()
    speed.results.ping
    label.config(text=f"Download Speed: {speed.download()} {speed.results.download}")
    label.config(text=f"Upload Speed: {speed.upload()} {speed.results.upload}")
    label.config(text=f"Ping: {speed.results.ping}")

window.mainloop()

