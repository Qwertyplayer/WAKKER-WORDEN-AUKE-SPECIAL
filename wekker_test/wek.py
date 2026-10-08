import tkinter as tk
import os


class FactoryGame:
    def __init__(self, root):
        self.root = root
        self.root.title("wakker worden auke special")
        self.root.geometry("760x520")

        # Zoek de afbeelding in dezelfde map als dit Python-bestand
        image_path = os.path.join(
            os.path.dirname(__file__),
            "achtergrond.png"
        )

        # Afbeelding laden
        self.background = tk.PhotoImage(file=image_path)

        # Achtergrond plaatsen
        self.background_label = tk.Label(
            root,
            image=self.background
        )

        self.background_label.place(
            x=0,
            y=0,
            relwidth=1,
            relheight=1
        )


root = tk.Tk()
FactoryGame(root)
root.mainloop()