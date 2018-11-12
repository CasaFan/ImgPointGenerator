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

def getFormattedCoordinates(thePolygone):
    formattedCoordinates = ''
    for i in range(len(polygone)):
        if ((i)%2) == 0: #indice impaire (x)
            print(i)
            print((i+1)%2)
            formattedCoordinates += (str(thePolygone[i])+',')
        else: #paire (y)
            formattedCoordinates += (str(thePolygone[i])+' ')
    print()
    return formattedCoordinates

if __name__ == "__main__":
    #Setting GUI 
    root = Tk()

    #Main Frame
    frame = Frame(root, relief=SUNKEN)
    frame.grid_rowconfigure(0, weight=1)
    frame.grid_columnconfigure(0, weight=1)
    frame.pack(fill=BOTH,expand=1)

    #adding the image
    File = askopenfilename(parent=root, initialdir="C:/",title='')
    img = ImageTk.PhotoImage(Image.open(File))
    root.geometry(str(img.width()) + 'x' + str(img.height()+250))
    canvas = Canvas(frame, bd=0, height=img.height(), width=img.width())
    canvas.grid(row=0, column=0, sticky=N+S+E+W)
    canvas.create_image(0,0,image=img,anchor="nw")

    #Text area frame
    canvasText = Canvas(frame, bd=0, height=230)
    canvasText.grid(row=2, column=0, sticky=N+S+E+W)

    """ TODO: scroll
    xscroll = Scrollbar(frame, orient=HORIZONTAL)
    xscroll.grid(row=2, column=0, sticky=E+W)
    yscroll = Scrollbar(frame)
    yscroll.grid(row=0, column=1, sticky=N+S)
    xscroll.config(command=canvasText.xview)
    yscroll.config(command=canvasText.yview)
    """

    #function to be called when mouse is clicked
    def addLine(event):
        global x0, x1, y0, y1, x_start, y_start, randomColor, polygone, canvas, canvasText
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
                canvasText.create_text(100, 30, text=getFormattedCoordinates(polygone), fill=randomColor)
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