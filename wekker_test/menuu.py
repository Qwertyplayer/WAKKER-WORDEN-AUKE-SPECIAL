import tkinter as tk
from tkinter import messagebox

class WAKKER_WORDEN_AUKE_SPECIAL:
    def __init__(self, root):
        self.root = root
        root.title("wakker worden auke special")
        root.geometry("760x520")

        menu = tk.Menu(root)
        root.config(menu=menu)

        bestand = tk.Menu(menu, tearoff=0)
        menu.add_cascade(label="Bestand", menu=bestand)
        bestand.add_command(label="Nieuw", command=self.nieuw)
        bestand.add_separator()
        bestand.add_command(label="Afsluiten", command=root.destroy)

        instellingen = tk.Menu(menu, tearoff=0)
        menu.add_cascade(label="Instellingen", menu=instellingen)
        instellingen.add_command(label="Achtergrond", command=self.achtergrond)

        help_menu = tk.Menu(menu, tearoff=0)
        menu.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="Over het programma", command=self.help)

    def nieuw(self):
        messagebox.showinfo("Nieuw", "Welkom bij de wekker!")

    def achtergrond(self):
        messagebox.showinfo("Instellingen", "Achtergrond komt later.")

    def help(self):
        messagebox.showinfo("Help", "Wekker en timer programma.")

root = tk.Tk()
app = WAKKER_WORDEN_AUKE_SPECIAL(root)
root.mainloop()
