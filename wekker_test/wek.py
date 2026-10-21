import tkinter as tk
import os
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
# Invoervakken voor de timer
minutes_input = tk.Entry(root, width=3, font=("Arial", 14))
minutes_input.insert(0, "5")

seconds_input = tk.Entry(root, width=3, font=("Arial", 14))
seconds_input.insert(0, "0")

timer_job = None

def set_timer():
    global remaining_seconds, timer_running, timer_job

    try:
        minutes = int(minutes_input.get())
        seconds = int(seconds_input.get())

        if minutes < 0 or seconds < 0 or seconds > 59:
            return

        # Stop een bestaande aftelling
        timer_running = False

        if timer_job is not None:
            root.after_cancel(timer_job)
            timer_job = None

        remaining_seconds = minutes * 60 + seconds

        canvas.itemconfig(
            timer_text,
            text=f"{minutes:02d}:{seconds:02d}"
        )

        # Start precies één aftelling
        timer_running = True
        update_timer()

    except ValueError:
        print("Vul geldige getallen in.")

set_button = tk.Button(
    root,
    text="Stel timer in",
    command=set_timer
)

minutes_input.place(relx=0.42, rely=0.40, anchor="center")
seconds_input.place(relx=0.50, rely=0.40, anchor="center")
set_button.place(relx=0.59, rely=0.40, anchor="center")

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
    anchor="center"
)

# Timer instellen op 5 minuten
remaining_seconds = 0
timer_running = False

timer_title = canvas.create_text(
    0, 0,
    text="TIMER",
    font=("Arial", 18, "bold"),
    fill="white",
    anchor="ne"
)

timer_text = canvas.create_text(
    0, 0,
    text="00:00",
    font=("Arial", 24, "bold"),
    fill="white",
    anchor="center"
)



def update_timer():
    global remaining_seconds, timer_running, timer_job

    if not timer_running:
        return

    minutes = remaining_seconds // 60
    seconds = remaining_seconds % 60

    canvas.itemconfig(
        timer_text,
        text=f"{minutes:02d}:{seconds:02d}"
    )

    if remaining_seconds > 0:
        remaining_seconds -= 1
        timer_job = root.after(1000, update_timer)
    else:
        timer_running = False
        canvas.itemconfig(timer_text, text="TIJD OM!")

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
    canvas.coords(clock, width * 0.509, height * 0.12)

    size = max(24, int(width / 64))
    canvas.itemconfig(clock, font=("Arial", size, "bold"))

    
    # Titel boven de timer
    canvas.coords(
        timer_title,
        width * 0.6,
        height * 0.20
    )

    canvas.itemconfig(
        timer_title,
        fill="black",
        font=("Arial", max(32, int(width / 180)), "bold")
    )

    # Timer onder de titel
    canvas.coords(
        timer_text,
        width * 0.515,
        height * 0.33
    )

    canvas.itemconfig(
        timer_text,
        font=("Arial", size, "bold")
    )

def update_clock():
    canvas.itemconfig(clock, text=strftime("%H:%M:%S"))
    root.after(1000, update_clock)

canvas.bind("<Configure>", resize_window)

update_clock()

timer_running = True
update_timer()

root.mainloop()
