from tkinter import Tk
from PIL import Image
# from tkinter.filedialog import askopenfilename
from src.GUI import GUI

root = Tk()

""" [PROD] 
# adding the image
File = askopenfilename(parent=root, initialdir="C:/", title='')
image = Image.open(File)
"""

# [DEV] Chemin seulement pour faciliter le développement: à changer en prod
image = Image.open("C:/Users/gs63vr/Documents/Grener/app/src/assets/img/confort/N4.png")

root.geometry('952x843')

myGUI = GUI(root, image)
root.mainloop()
