import tkinter as tk
import os
import time


class WAKKER_WORDEN_AUKE_SPECIAL:

    def __init__(self, root):
        self.root = root
        self.root.title("Wakker Worden Auke Special")
        self.root.geometry("760x520")

        # Achtergrond laden
        image_path = os.path.join(
            os.path.dirname(__file__),
            "achtergrond.png"
        )

        self.image = tk.PhotoImage(file=image_path)

        self.label = tk.Label(
            self.root,
            image=self.image
        )
        self.label.place(
            x=0, y=0,
            relwidth=1,
            relheight=1
        )

        # Klok
        self.clock = tk.Label(
            self.root,
            font=("Arial", 24, "bold"),
            fg="white",
            bg="black",
            padx=20,
            pady=10
        )

        self.clock.place(
            relx=0.6,
            rely=0.08,
            anchor="ne"
        )

        # Menu aanmaken
        menu = tk.Menu(self.root)
        self.root.config(menu=menu)

        # Bestand menu
        bestand_menu = tk.Menu(menu, tearoff=0)
        menu.add_cascade(
            label="Bestand",
            menu=bestand_menu
        )

        bestand_menu.add_command(
            label="Afsluiten",
            command=self.root.destroy
        )

        # Alarm menu
        alarm_menu = tk.Menu(menu, tearoff=0)
        menu.add_cascade(
            label="Alarm",
            menu=alarm_menu
        )

        alarm_menu.add_command(
            label="Open Alarm",
            command=self.open_alarm
        )

        # Timer menu
        timer_menu = tk.Menu(menu, tearoff=0)
        menu.add_cascade(
            label="Timer",
            menu=timer_menu
        )

        timer_menu.add_command(
            label="Open Timer",
            command=self.open_timer
        )

        # Klok starten
        self.update_clock()

        # Klok aanpassen aan venstergrootte
        self.root.bind(
            "<Configure>",
            self.resize_clock
        )

    # Klok elke seconde updaten
    def update_clock(self):
        current_time = time.strftime("%H:%M:%S")
        self.clock.config(text=current_time)

        self.root.after(1000, self.update_clock)

    # Klok aanpassen aan venstergrootte
    def resize_clock(self, event):
        if event.widget == self.root:
            size = max(24, int(event.width / 64))
            self.clock.config(
                font=("Arial", size, "bold")
            )

    # Alarm openen
    def open_alarm(self):
        print("Alarm openen")

    # Timer openen
    def open_timer(self):
        print("Timer openen")


root = tk.Tk()
app = WAKKER_WORDEN_AUKE_SPECIAL(root)
root.mainloop()