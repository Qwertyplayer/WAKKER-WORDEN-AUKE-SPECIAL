import tkinter as tk
import os
from time import strftime

root = tk.Tk()
root.title("Wakker Worden Auke Special")
root.geometry("760x520")

# Achtergrond laden
image_path = os.path.join(
    os.path.dirname(__file__),
    "achtergrond.png"
)

image = tk.PhotoImage(file=image_path)

label = tk.Label(root, image=image)
label.place(x=0, y=0, relwidth=1, relheight=1)

#hoe de klok eruit ziet
clock = tk.Label(
    root,
    font=("Arial", 24, "bold"),
    fg="white",
    bg="black",
    padx=20,
    pady=10
)

clock.place(relx=0.6, rely=0.08, anchor="ne")

#update elke seconde de klok
def update_clock():
    current_time = strftime("%H:%M:%S")
    clock.config(text=current_time)
    root.after(1000, update_clock)

# zorgt ervoor dat de klok grote bij het venster past
def resize_clock(event):
    if event.widget == root:
        size = max(24, int(event.width / 64))
        clock.config(font=("Arial", size, "bold"))

root.bind("<Configure>", resize_clock)

update_clock()

root.mainloop()