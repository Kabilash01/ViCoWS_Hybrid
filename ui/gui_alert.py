# Placeholder for gui_alert.py
# ui/gui_alert.py

import tkinter as tk

def alert_window():
    """
    Opens a pop-up window to alert the driver of a collision threat.
    """
    root = tk.Tk()
    root.title("⚠️ Collision Warning Alert!")
    root.geometry("500x300")
    root.configure(bg="red")

    label = tk.Label(root, text="⚠️ WARNING: Collision Risk Detected!", font=("Arial", 24, "bold"), fg="white", bg="red")
    label.pack(expand=True, pady=30)

    message = tk.Label(root, text="Please take immediate action!\nSlow down and drive cautiously.", font=("Arial", 16), fg="white", bg="red")
    message.pack(expand=True)

    root.mainloop()
