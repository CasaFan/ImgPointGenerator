from tkinter import *
from tkinter.ttk import Combobox, Button
from tkinter.filedialog import askopenfilename
from PIL import Image, ImageTk
import random

#global vars 
x0 = y0 = x1 = y1 = x_start = y_start = -1
polygone = []
polygoneCollection = []
colorCollection = ['black', 'red', 'green', 'blue', 'cyan', 'yellow', 'magenta']
randomColor = random.choice(colorCollection)
#fontText = tkFont.Font(family='Helvetica')
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
    textCanavas = Canvas(frame, bd=0, bg='blue', height=230)
    textCanavas.grid(row=4, column=0, sticky=N+S+E+W)

    #text frame in canavas
    textFrame = Frame(textCanavas, relief=SUNKEN, bg="yellow")
    textFrame.grid_rowconfigure(0, weight=1)
    textFrame.grid_columnconfigure(0, weight=1)
    textCanavas.create_window(20, 20, anchor=NW, window=textFrame, width=(img.width()-50), height=200)
    
    #text widget
    textContent = Text(textFrame, font='Arial')
    setTextColorTags(textContent, colorCollection)
    textContent.pack(side=LEFT, fill=Y)

    #utility frame
    utilityFrame = Frame(textFrame, relief=SUNKEN)
    utilityFrame.pack(side=LEFT, fill=BOTH)

    #listbox widget
    comboBox = Combobox(utilityFrame, width=20)
    comboBox['values'] = ('Text', 'Json', 'Html')
    comboBox.current(0)
    comboBox['state'] = 'readonly'
    comboBox.pack(padx=10, pady=5, anchor=N)

    #button frame: for spacing from the combobox
    btnFrame  = Frame(utilityFrame)
    btnFrame.pack(padx=10, pady=50)

    #Copy Button widget
    copyBtn = Button(btnFrame, text='Copy')
    copyBtn.pack()

    #clipboard indicator
    cpMsgLabel = Label(utilityFrame, text='text copié!')

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
                polygoneStr = getFormattedCoordinates(polygone)
                textContent.insert('end', polygoneStr+'\n', randomColor)
                polygoneCollection.append(polygoneStr)
                polygone = []
                randomColor = getNoRepeatColor()
                print('restart!')
                print(polygoneCollection)
            else:
                x0 = x1
                y0 = y1
                polygone.append(x0)
                polygone.append(y0)
        
        print (event.x, event.y)

    def generateText(event):
        global textContent, polygoneCollection
        formattedText = ''
        selection = event.widget.get()
        
        if selection == "Json":
            formattedText = '{\n\tvalue: "", label: "", \n\tzone: [\n\t\t'
            for i in range(0, len(polygoneCollection)):
                if i != (len(polygoneCollection)-1):
                    formattedText += '{id: "", points: "' + polygoneCollection[i] + '"},\n\t\t'
                else: 
                    formattedText += '{id: "", points: "' + polygoneCollection[i] + '"}\n\t'
            formattedText += ']\n}'
        elif selection == 'Html':
            for polygone in polygoneCollection:
                formattedText += '<polygon id="" class="st0" points="' + polygone + '"/>\n'
        else:
            for polygone in polygoneCollection:
                formattedText += polygone + '\n'
        textContent.delete('1.0', END)
        textContent.insert('1.0', formattedText)

    def clearMsgLabel():
        cpMsgLabel.pack_forget()

    def copyTextToClipBoard(event):
        global textContent
        textAreaValues = textContent.get('1.0', END)
        root.clipboard_clear()
        root.clipboard_append(textAreaValues)
        cpMsgLabel.pack()
        cpMsgLabel.after(2500, clearMsgLabel)

    #bind mouseclick event
    canvas.bind("<Button 1>", addLine)
    comboBox.bind('<<ComboboxSelected>>', generateText)
    copyBtn.bind("<Button 1>", copyTextToClipBoard)

    root.mainloop()