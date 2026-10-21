
import tkinter as tk
import os
import winsound
from time import strftime
from math import floor

root = tk.Tk()
root.title("Wakker Worden Auke Special")
root.geometry("760x520")

# Achtergrond laden
image_path = os.path.join(
    os.path.dirname(__file__),
    "achtergrond.png"
)

original_image = tk.PhotoImage(file=image_path)

canvas = tk.Canvas(root, highlightthickness=0)
canvas.pack(fill="both", expand=True)

image = original_image

background = canvas.create_image(
    0, 0,
    image=image,
    anchor="nw"
)

clock = canvas.create_text(
    0, 0,
    text="",
    font=("Arial", 24, "bold"),
    fill="white",
    anchor="ne"
)


def resize_window(event):
    global image

    if event.widget != canvas:
        return

    width = event.width
    height = event.height

    # Vergroot de afbeelding zodat het hele venster gevuld wordt
    scale = max(
        width / original_image.width(),
        height / original_image.height()
    )

    if scale >= 1:
        factor = max(1, int(scale))
        image = original_image.zoom(factor, factor)
    else:
        factor = max(1, int(1 / scale))
        image = original_image.subsample(factor, factor)

    canvas.itemconfig(background, image=image)

    # Afbeelding in het midden plaatsen
    canvas.coords(
        background,
        (width - image.width()) / 2,
        (height - image.height()) / 2
    )

    # Klok op zijn plek houden
    canvas.coords(clock, width * 0.6, height * 0.08)

    size = max(24, int(width / 64))
    canvas.itemconfig(clock, font=("Arial", size, "bold"))

def update_clock():
    canvas.itemconfig(clock, text=strftime("%H:%M:%S"))
    root.after(1000, update_clock)

canvas.bind("<Configure>", resize_window)
sound_path = os.path.join(
    os.path.dirname(__file__),
    "alarm.geluid.wav"
)

def play_alarm():
    winsound.PlaySound(
        sound_path,
        winsound.SND_FILENAME | winsound.SND_ASYNC
    )

def stop_alarm():
    winsound.PlaySound(None, winsound.SND_PURGE)
update_clock()
root.mainloop()
    