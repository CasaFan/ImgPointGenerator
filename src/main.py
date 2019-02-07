from tkinter import Tk
from PIL import Image
from src.GUI import GUI

root = Tk()

# adding the image
# File = askopenfilename(parent=root, initialdir="C:/", title='')
# NOTE: Chemin seulement pour faciliter le développement: à changer en prod
image = Image.open("C:/Users/gs63vr/Documents/Grener/app/src/assets/img/confort/N4.png")

root.geometry(str(image.width) + 'x' + str(image.height + 250))

myGUI = GUI(root, image)
root.mainloop()
