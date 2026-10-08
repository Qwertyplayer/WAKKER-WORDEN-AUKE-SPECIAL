import tkinter as tk
import os

root = tk.Tk()
root.title("Wakker Worden Auke Special")
root.geometry("760x520")

image_path = os.path.join(
    os.path.dirname(__file__),
    "achtergrond.png"
)

print("Afbeelding:", image_path)

image = tk.PhotoImage(file=image_path)

print("Breedte:", image.width())
print("Hoogte:", image.height())

label = tk.Label(
    root,
    image=image,
    bg="red"
)

label.pack()

root.mainloop()