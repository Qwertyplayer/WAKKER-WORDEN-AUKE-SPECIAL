import tkinter as tk

class FactoryGame:
    def __init__(self, root):
        self.root = root
        self.root.title("wakker worden auke special")
        self.root.geometry("760x520")

        self.background = tk.PhotoImage(file="achtergrond.png")

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