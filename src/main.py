from tkinter import Tk
from src.GUI import GUI


root = Tk()
root.state('zoomed')

screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

root.maxsize(width=screen_width, height=screen_height)

# set window size to screen size by default [DEV]: 1536*864
root.geometry('%sx%s' % (screen_width, screen_height))
root.update()

myGUI = GUI(root)
# myGUI.open_file()

root.mainloop()
