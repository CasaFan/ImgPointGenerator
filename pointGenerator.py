from tkinter import *
from tkinter.filedialog import askopenfilename
from PIL import Image, ImageTk
import random

#global vars 
x0 = y0 = x1 = y1 = x_start = y_start = -1
polygone = []
colorCollection = ['black', 'red', 'green', 'blue', 'cyan', 'yellow', 'magenta']
randomColor = random.choice(colorCollection)

def getNoRepeatColor():
    global randomColor, colorCollection
    colorCollectionCopie = colorCollection.copy()
    colorCollectionCopie.remove(randomColor)
    return random.choice(colorCollectionCopie)

if __name__ == "__main__":
    #Setting GUI 
    root = Tk()

    frame = Frame(root, relief=SUNKEN)
    frame.grid_rowconfigure(0, weight=1)
    frame.grid_columnconfigure(0, weight=1)
    xscroll = Scrollbar(frame, orient=HORIZONTAL)
    xscroll.grid(row=1, column=0, sticky=E+W)
    yscroll = Scrollbar(frame)
    yscroll.grid(row=0, column=1, sticky=N+S)
    canvas = Canvas(frame, bd=0, xscrollcommand=xscroll.set, yscrollcommand=yscroll.set)
    canvas.grid(row=0, column=0, sticky=N+S+E+W)
    xscroll.config(command=canvas.xview)
    yscroll.config(command=canvas.yview)
    frame.pack(fill=BOTH,expand=1)

    #adding the image
    File = askopenfilename(parent=root, initialdir="C:/",title='')
    img = ImageTk.PhotoImage(Image.open(File))
    root.geometry(str(img.width()) + 'x' + str(img.height()))
    canvas.create_image(0,0,image=img,anchor="nw")
    canvas.config(scrollregion=canvas.bbox(ALL))
    
    #function to be called when mouse is clicked
    def addLine(event):
        global x0, x1, y0, y1, x_start, y_start, randomColor, polygone, canvas
        if(x0 == -1 and y0 == -1): # start drawing
            x0 = event.x
            y0 = event.y
            x_start = x0
            y_start = y0
            polygone.append(x_start)
            polygone.append(y_start)
        else: # in drawing
            x1 = event.x
            y1 = event.y
            canvas.create_line(x0, y0, x1, y1, fill=randomColor)
            if ((x_start-5) <= x1 <= (x_start+5)) and ((y_start-5) <= y1 <= (y_start+5)): 
                # endPoint ~ start point (in a range of 5 pixels ): restart draw
                x0 = -1
                y0 = -1
                canvas.create_polygon(' '.join(str(points) for points in polygone), fill=randomColor)
                print (' '.join(str(points) for points in polygone))
                polygone = []
                randomColor = getNoRepeatColor()
                print('restart!')
            else:
                x0 = x1
                y0 = y1
                polygone.append(x0)
                polygone.append(y0)
        
        print (event.x, event.y)
        
    #mouseclick event
    canvas.bind("<Button 1>", addLine)

    root.mainloop()