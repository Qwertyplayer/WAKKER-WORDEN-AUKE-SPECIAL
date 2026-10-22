import tkinter as tk
import os
import time
import winsound

# VENSTER INSTELLEN
root = tk.Tk()
root.title("Wakker Worden - Wekker")
root.geometry("760x520")
root.minsize(600, 450)
root.configure(bg="#101827")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
IMAGE_PATH = os.path.join(BASE_DIR, "achtergrond.png")
SOUND_PATH = os.path.join(BASE_DIR, "alarm.geluid.wav")

# Kleuren
BG = "#101827"
PANEL = "#1e293b"
WHITE = "#ffffff"
MUTED = "#aebbd0"
BLUE = "#3b82f6"
GREEN = "#22c55e"
RED = "#ef4444"

# ACHTERGROND
canvas = tk.Canvas(
    root,
    highlightthickness=0,
    bg=BG
)
canvas.pack(fill="both", expand=True)

original_image = None
background = None
image = None

if os.path.exists(IMAGE_PATH):
    original_image = tk.PhotoImage(file=IMAGE_PATH)
    image = original_image
    background = canvas.create_image(
        0, 0, image=image, anchor="nw"
    )

# DIGITALE KLOK
clock = canvas.create_text(
    0, 0,
    text="00:00:00",
    fill=WHITE,
    font=("Arial", 30, "bold"),
    anchor="center"
)

title = canvas.create_text(
    0, 0,
    text="WAKKER WORDEN",
    fill=WHITE,
    font=("Arial", 22, "bold"),
    anchor="center"
)

subtitle = canvas.create_text(
    0, 0,
    text="Wekker",
    fill="#93c5fd",
    font=("Arial", 12, "bold"),
    anchor="center"
)

# TIMER
remaining_seconds = 300
timer_running = False
timer_job = None
deadline = None
alarm_active = False


def format_time(seconds):
    minutes = seconds // 60
    seconds = seconds % 60
    return f"{minutes:02d}:{seconds:02d}"


timer_panel = tk.Frame(
    root,
    bg=PANEL,
    padx=24,
    pady=20,
    highlightthickness=1,
    highlightbackground="#334155"
)

tk.Label(
    timer_panel,
    text="STEL JE WEKKER IN",
    font=("Arial", 15, "bold"),
    fg=WHITE,
    bg=PANEL
).grid(row=0, column=0, columnspan=3, pady=(0, 14))

tk.Label(
    timer_panel,
    text="Minuten",
    font=("Arial", 10),
    fg=MUTED,
    bg=PANEL
).grid(row=1, column=0, padx=8)

tk.Label(
    timer_panel,
    text="Seconden",
    font=("Arial", 10),
    fg=MUTED,
    bg=PANEL
).grid(row=1, column=2, padx=8)

minutes_input = tk.Entry(
    timer_panel,
    width=5,
    font=("Arial", 17, "bold"),
    justify="center",
    bg="#0f172a",
    fg=WHITE,
    insertbackground=WHITE,
    relief="flat"
)
minutes_input.insert(0, "5")
minutes_input.grid(row=2, column=0, padx=8, pady=5, ipady=5)

tk.Label(
    timer_panel,
    text=":",
    font=("Arial", 20, "bold"),
    fg=WHITE,
    bg=PANEL
).grid(row=2, column=1)

seconds_input = tk.Entry(
    timer_panel,
    width=5,
    font=("Arial", 17, "bold"),
    justify="center",
    bg="#0f172a",
    fg=WHITE,
    insertbackground=WHITE,
    relief="flat"
)
seconds_input.insert(0, "0")
seconds_input.grid(row=2, column=2, padx=8, pady=5, ipady=5)

timer_display = tk.Label(
    timer_panel,
    text="05:00",
    font=("Arial", 34, "bold"),
    fg=GREEN,
    bg=PANEL
)
timer_display.grid(
    row=3, column=0, columnspan=3, pady=(14, 4)
)

status_label = tk.Label(
    timer_panel,
    text="Klaar om te starten",
    font=("Arial", 10),
    fg=MUTED,
    bg=PANEL
)
status_label.grid(
    row=4, column=0, columnspan=3, pady=(0, 12)
)


def stop_alarm():
    global alarm_active
    try:
        winsound.PlaySound(None, winsound.SND_PURGE)
    except RuntimeError:
        pass
    alarm_active = False


def play_alarm():
    global alarm_active

    if not os.path.exists(SOUND_PATH):
        status_label.config(
            text="Timer klaar! alarm.geluid.wav ontbreekt.",
            fg=RED
        )
        return

    try:
        winsound.PlaySound(
            SOUND_PATH,
            winsound.SND_FILENAME | winsound.SND_ASYNC | winsound.SND_LOOP
        )
        alarm_active = True
        status_label.config(
            text="Alarm is aan",
            fg=RED
        )
    except (RuntimeError, OSError):
        status_label.config(
            text="Timer klaar, maar alarm kon niet afspelen.",
            fg=RED
        )


def cancel_timer_job():
    global timer_job

    if timer_job is not None:
        root.after_cancel(timer_job)
        timer_job = None


def update_display():
    timer_display.config(text=format_time(remaining_seconds))


def timer_tick():
    global remaining_seconds, timer_running
    global timer_job, deadline

    timer_job = None

    if not timer_running:
        return

    # Gebruik de klok zodat de timer niet steeds
    # langzamer wordt door kleine vertragingen.
    remaining_seconds = max(
        0, int(deadline - time.monotonic() + 0.999)
    )

    update_display()

    if remaining_seconds <= 0:
        timer_running = False
        deadline = None
        status_label.config(text="De tijd is om!", fg=RED)
        play_alarm()
        return

    timer_job = root.after(200, timer_tick)


def start_timer():
    global remaining_seconds, timer_running, deadline

    try:
        minutes = int(minutes_input.get())
        seconds = int(seconds_input.get())

        if minutes < 0 or seconds < 0 or seconds > 59:
            status_label.config(
                text="Gebruik minuten >= 0 en seconden 0-59.",
                fg=RED
            )
            return

        total = minutes * 60 + seconds

        if total <= 0:
            status_label.config(
                text="Stel een tijd groter dan nul in.",
                fg=RED
            )
            return

    except ValueError:
        status_label.config(
            text="Vul alleen hele getallen in.",
            fg=RED
        )
        return

    cancel_timer_job()
    stop_alarm()

    remaining_seconds = total
    timer_running = True
    deadline = time.monotonic() + remaining_seconds

    status_label.config(text="Timer loopt...", fg=GREEN)
    update_display()
    timer_tick()


def pause_timer():
    global remaining_seconds, timer_running, deadline

    if not timer_running:
        return

    remaining_seconds = max(
        0, int(deadline - time.monotonic() + 0.999)
    )

    timer_running = False
    deadline = None
    cancel_timer_job()
    update_display()

    status_label.config(text="Timer gepauzeerd", fg=MUTED)


def resume_timer():
    global timer_running, deadline

    if timer_running or remaining_seconds <= 0:
        return

    stop_alarm()
    deadline = time.monotonic() + remaining_seconds
    timer_running = True

    status_label.config(text="Timer loopt...", fg=GREEN)
    timer_tick()


def reset_timer():
    global remaining_seconds, timer_running, deadline

    timer_running = False
    deadline = None
    cancel_timer_job()
    stop_alarm()

    try:
        minutes = int(minutes_input.get())
        seconds = int(seconds_input.get())

        if minutes < 0 or seconds < 0 or seconds > 59:
            raise ValueError

        remaining_seconds = minutes * 60 + seconds

        if remaining_seconds <= 0:
            raise ValueError

    except ValueError:
        remaining_seconds = 0
        status_label.config(
            text="Vul een geldige tijd in.",
            fg=RED
        )
        update_display()
        return

    status_label.config(text="Timer gereset", fg=MUTED)
    update_display()


def make_button(parent, text, color, command):
    return tk.Button(
        parent,
        text=text,
        command=command,
        font=("Arial", 10, "bold"),
        bg=color,
        fg=WHITE,
        activebackground=color,
        activeforeground=WHITE,
        relief="flat",
        cursor="hand2",
        padx=12,
        pady=9
    )


start_button = make_button(
    timer_panel, "Start", BLUE, start_timer
)
pause_button = make_button(
    timer_panel, "Pauze", "#475569", pause_timer
)
resume_button = make_button(
    timer_panel, "Verder", GREEN, resume_timer
)
reset_button = make_button(
    timer_panel, "Reset", RED, reset_timer
)

start_button.grid(row=5, column=0, padx=3, pady=5, sticky="ew")
pause_button.grid(row=5, column=1, padx=3, pady=5, sticky="ew")
resume_button.grid(row=5, column=2, padx=3, pady=5, sticky="ew")
reset_button.grid(row=6, column=0, columnspan=3, pady=(5, 0), sticky="ew")

# =========================
# KLOK BIJWERKEN
# =========================
def update_clock():
    canvas.itemconfig(
        clock,
        text=time.strftime("%H:%M:%S")
    )
    root.after(250, update_clock)

# VENSTER AANPASSEN
def resize_window(event):
    global image

    if event.widget != canvas:
        return

    width = event.width
    height = event.height

    if original_image is not None:
        # Schaal de achtergrond proportioneel en centreer hem.
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
        canvas.coords(
            background,
            (width - image.width()) / 2,
            (height - image.height()) / 2
        )

    canvas.coords(clock, width * 0.5, height * 0.07)
    canvas.coords(title, width * 0.5, height * 0.15)
    canvas.coords(subtitle, width * 0.5, height * 0.205)

    timer_panel.place(
        relx=0.5,
        rely=0.60,
        anchor="center"
    )


canvas.bind("<Configure>", resize_window)

update_clock()
root.mainloop()
