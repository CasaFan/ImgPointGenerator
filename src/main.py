from tkinter import Tk
from src.GUI import GUI


WINDOW_WIDTH = "1920"
WINDOW_HEIGHT = "1080"

root = Tk()

"""

# [DEV] Chemin seulement pour faciliter le développement: à changer en prod
image = Image.open("C:/Users/gs63vr/Documents/Grener/app/src/assets/img/confort/N4.png")
"""
root.geometry(WINDOW_WIDTH + "x" + WINDOW_HEIGHT)

myGUI = GUI(root)
myGUI.open_file()

root.mainloop()
