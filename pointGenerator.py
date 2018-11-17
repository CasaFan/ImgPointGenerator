from tkinter import *
from tkinter.filedialog import askopenfilename
from PIL import Image, ImageTk
import random

#global vars 
x0 = y0 = x1 = y1 = x_start = y_start = -1
polygone = []
colorCollection = ['black', 'red', 'green', 'blue', 'cyan', 'yellow', 'magenta']
randomColor = random.choice(colorCollection)
textHeight = 30

def getNoRepeatColor():
    """
    Retourne une couleur dans la colorCollection autre que la variable 'randomColor'
    Pour éviter d'avoir 2 fois la suite la meme couleur
    """
    global randomColor, colorCollection
    colorCollectionCopie = colorCollection.copy()
    colorCollectionCopie.remove(randomColor)
    return random.choice(colorCollectionCopie)

def getFormattedCoordinates(thePolygone):
    """
    Retourne un String de coordonées de polygone sous forme: "x0, y0 x1, y1 ... "
    """
    formattedCoordinates = ''
    for i in range(len(polygone)):
        if ((i)%2) == 0: #indice paire (x)
            formattedCoordinates += (str(thePolygone[i])+',')
        else: #impaire (y)
            formattedCoordinates += (str(thePolygone[i])+' ')
    return formattedCoordinates

def setTextColorTags(textWidget, colorCollection):
    """
    Creer un textTag pour chaque couleur dans 'colorCollection'
    """
    for color in colorCollection:
        textWidget.tag_config(color, foreground=color)

if __name__ == "__main__":
    #Setting GUI 
    root = Tk()

    #Main Frame
    frame = Frame(root, relief=SUNKEN, bg="red")
    frame.grid_rowconfigure(0, weight=1)
    frame.grid_columnconfigure(0, weight=1)
    frame.pack(fill=BOTH,expand=1)

    #adding the image
    File = askopenfilename(parent=root, initialdir="C:/",title='')
    img = ImageTk.PhotoImage(Image.open(File))
    root.geometry(str(img.width()) + 'x' + str(img.height()+250))
    canvas = Canvas(frame, bg="black", bd=0, height=img.height(), width=img.width())
    canvas.grid(row=0, column=0, sticky=N+S+E+W)
    canvas.create_image(0,0,image=img,anchor="nw")

    #Text area frame
    textCanavas = Canvas(frame, bd=0, bg='blue', height=230, scrollregion=(0, 0, 0, 500)) #To Modify 
    textCanavas.grid(row=4, column=0, sticky=N+S+E+W)

    #text frame in canavas
    textFrame = Frame(textCanavas, relief=SUNKEN)
    textFrame.grid_rowconfigure(0, weight=1)
    textFrame.grid_columnconfigure(0, weight=1)
    textCanavas.create_window(20, 20, anchor=NW, window=textFrame, width=(img.width()-50), height=200, state=DISABLED)
    textContent = Text(textFrame)
    setTextColorTags(textContent, colorCollection)

    #function to be called when mouse is clicked
    def addLine(event):
        """
        MouseClick event pour tracer les polygones
        """
        global x0, x1, y0, y1, x_start, y_start, randomColor, polygone, canvas, textContent
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
                textContent.insert('end', getFormattedCoordinates(polygone)+'\n', randomColor)
                textContent.pack()
                polygone = []
                randomColor = getNoRepeatColor()
                print('restart!')
            else:
                x0 = x1
                y0 = y1
                polygone.append(x0)
                polygone.append(y0)
        
        print (event.x, event.y)
        
    #bind mouseclick event
    canvas.bind("<Button 1>", addLine)

    root.mainloop()