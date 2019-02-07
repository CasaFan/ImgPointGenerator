"""
[LEGACY]
Attention: Code abandonné (Refactored)
Voir main.py
"""

from tkinter import *
from tkinter.ttk import Combobox, Button
from tkinter.filedialog import askopenfilename
from PIL import Image, ImageTk
import random

# global vars
x0 = y0 = x1 = y1 = x_start = y_start = -1
polygone = []
polygoneCollection = {} 
colorCollection = ['black', 'red', 'green', 'blue', 'cyan', 'yellow', 'magenta']
randomColor = random.choice(colorCollection)
# fontText = tkFont.Font(family='Helvetica')
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
        if i % 2 == 0:  # indice paire (x)
            formattedCoordinates += (str(thePolygone[i])+',')
        else:  # impaire (y)
            formattedCoordinates += (str(thePolygone[i])+' ')
    return formattedCoordinates


def setTextColorTags(textWidget, colorCollection):
    """
    Créer un textTag pour chaque couleur dans 'colorCollection'
    """
    for color in colorCollection:
        textWidget.tag_config(color, foreground=color)


def rreplace(s, old, new, occurrence):
    """
    Inversement remplacer le 'old' caracter 'occurrence' fois par 'new' caracter dans le string 's'  
    """
    li = s.rsplit(old, occurrence)
    return new.join(li)


def openFile():
    """
    file = askopenfilename(parent=self.master, initialdir="C:/", title='')
    image = ImageTk.PhotoImage(Image.open(file))
    self.__init__(self.master, image)
    """

def saveTo():
    """
    return True
    """

if __name__ == "__main__":

    # Setting GUI
    root = Tk()

    # Main Frame
    frame = Frame(root, relief=SUNKEN, bg="red")
    frame.grid_rowconfigure(0, weight=1)
    frame.grid_columnconfigure(0, weight=1)
    frame.pack(fill=BOTH, expand=1)
    # Menu
    menubar = Menu(root)
    # create a pulldown menu, and add it to the menu bar
    filemenu = Menu(menubar, tearoff=0)
    filemenu.add_command(label="Open", command=openFile)
    filemenu.add_command(label="Save", command=saveTo)
    filemenu.add_separator()
    filemenu.add_command(label="Exit", command=root.quit)
    menubar.add_cascade(label="File", menu=filemenu)
    root.config(menu=menubar)

    # adding the image
    # File = askopenfilename(parent=root, initialdir="C:/",title='')
    # NOTE: Chemin seulement pour faciliter le developpement: à changer en prod
    img = ImageTk.PhotoImage(Image.open("C:/Users/gs63vr/Documents/Grener/app/src/assets/img/confort/N4.png"))
    
    root.geometry(str(img.width()) + 'x' + str(img.height()+250))
    canvas = Canvas(frame, bg="black", bd=0, height=img.height(), width=img.width())
    canvas.grid(row=1, column=0, sticky=N+S+E+W)
    canvas.create_image(0, 0, image=img, anchor="nw")

    # Text area frame
    textCanavas = Canvas(frame, bd=0, bg='blue', height=230)
    textCanavas.grid(row=4, column=0, sticky=N+S+E+W)

    # text frame in canavas
    textFrame = Frame(textCanavas, relief=SUNKEN, bg="yellow")
    textFrame.grid_rowconfigure(0, weight=1)
    textFrame.grid_columnconfigure(0, weight=1)
    textCanavas.create_window(20, 20, anchor=NW, window=textFrame, width=(img.width()-50), height=200)
    
    # text widget
    textContent = Text(textFrame, font='Arial')
    setTextColorTags(textContent, colorCollection)
    textContent.pack(side=LEFT, fill=Y)

    # utility frame
    utilityFrame = Frame(textFrame, relief=SUNKEN)
    utilityFrame.pack(side=LEFT, fill=BOTH)

    # listbox widget
    comboBox = Combobox(utilityFrame, width=20)
    comboBox['values'] = ('Text', 'Json', 'Html')
    comboBox.current(0)
    comboBox['state'] = 'readonly'
    comboBox.pack(padx=10, pady=5, anchor=N)

    # button frame: for spacing from the combobox
    btnFrame  = Frame(utilityFrame)
    btnFrame.pack(padx=10, pady=50)

    # Copy Button widget
    copyBtn = Button(btnFrame, text='Copy text')
    copyBtn.pack()

    # clipboard indicator
    cpMsgLabel = Label(utilityFrame, text='text copié!')

    # popup entry value
    roomLabel = StringVar()

    # Les traces de ligne
    canvasLigneCollection = []

    def end_draw_cycle(popup):
        global randomColor, polygone, textContent, canvasLigneCollection
        popup.destroy()
        polygoneStr = getFormattedCoordinates(polygone)
        textContent.insert('end', roomLabel.get() + ': ' + polygoneStr+'\n', randomColor)
        polygoneCollection[roomLabel.get()] = polygoneStr
        roomLabel.set('')
        polygone = []
        canvasLigneCollection = []
        randomColor = getNoRepeatColor()
        print('restart!')
        print(polygoneCollection)

    def popup_entry():
        popup = Toplevel()
        popup.wm_title("Saisir un label")
        popup.wm_geometry("%dx%d%+d%+d" % (220, 80, 450, 300))

        popup_label = Label(popup, text="Label : ")
        popup_label.grid(row=0, padx=10, pady=10)

        entry = Entry(popup, textvariable=roomLabel)
        entry.grid(row=0, column=1, padx=10, pady=10)
        entry.focus_set()

        button = Button(popup, text="Ok", command=lambda: end_draw_cycle(popup))
        button.grid(row=1, columnspan=2, padx=10, pady=10)

    def popup(msg):
        popup = Toplevel()
        popup.wm_title("Info")
        popup.wm_geometry("%dx%d%+d%+d" % (220, 80, 450, 300))

        popup_label = Label(popup, text=msg)
        popup_label.grid(row=0, padx=65, pady=10)

        button = Button(popup, text="Ok", command=popup.destroy)
        button.grid(row=1, padx=65, pady=10)

    def addLine(event):
        """
        MouseClick event pour tracer les polygones
        """
        global x0, x1, y0, y1, x_start, y_start, randomColor, polygone, canvas, textContent
        if x0 == -1 and y0 == -1:  # start drawing
            x0 = event.x
            y0 = event.y
            x_start = x0
            y_start = y0
            polygone.append(x_start)
            polygone.append(y_start)
        else:  # in drawing
            x1 = event.x
            y1 = event.y
            canvasLigne = canvas.create_line(x0, y0, x1, y1, fill=randomColor)
            canvasLigneCollection.append(canvasLigne)
            if ((x_start-5) <= x1 <= (x_start+5)) and ((y_start-5) <= y1 <= (y_start+5)): 
                # endPoint ~ start point (in a range of 5 pixels ): end 1 cycle draw
                x0 = -1
                y0 = -1
                canvas.create_polygon(' '.join(str(points) for points in polygone), fill=randomColor)
                popup_entry()
            else:
                x0 = x1
                y0 = y1
                polygone.append(x0)
                polygone.append(y0)

    def cancelDraw(event):
        global x0, y0, x_start, y_start, polygone, canvasLigneCollection
        x0 = y0 = x_start = y_start = -1
        polygone = []
        popup("Tracage annulé")
        for canvasLigne in canvasLigneCollection:
            canvas.delete(canvasLigne)
        canvasLigneCollection = []

    def generateText(event):
        global textContent, polygoneCollection
        formattedText = ''
        selection = event.widget.get()
        
        if selection == "Json":
            formattedText = '{\n\tvalue: "", label: "", \n\tzones: [\n\t'
            for key, value in polygoneCollection.items():
                formattedText += '\t{id: "' + key + '", points: "' + value + '"},\n\t'
            formattedText = rreplace(formattedText, ',', '', 1)
            formattedText += ']\n}'
        elif selection == 'Html':
            for key, value in polygoneCollection.items():
                formattedText += '<polygon id="' + key + '" class="st0" points="' + value + '"/>\n'
        else:
            for key, value in polygoneCollection.items():
                formattedText += (key + ': ' + value + '\n')
        textContent.delete('1.0', END)
        textContent.insert('1.0', formattedText)

    def clearMsgLabel():
        cpMsgLabel.pack_forget()

    def copyTextToClipBoard(event):
        global textContent
        textAreaValues = textContent.get('1.0', END)
        root.clipboard_clear()
        root.clipboard_append(textAreaValues)
        cpMsgLabel.pack(anchor=N)
        cpMsgLabel.after(2500, clearMsgLabel)

    # bind mouseclick event
    canvas.bind("<Button 1>", addLine)
    canvas.bind("<Button 3>", cancelDraw)
    comboBox.bind('<<ComboboxSelected>>', generateText)
    copyBtn.bind("<Button 1>", copyTextToClipBoard)

    root.mainloop()
