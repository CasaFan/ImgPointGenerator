from tkinter import *
from tkinter.ttk import Combobox, Button
from tkinter.filedialog import askopenfilename
from PIL import Image, ImageTk
import random


class GUI:

    x0 = y0 = x1 = y1 = x_start = y_start = -1
    polygone = []
    polygoneCollection = {}
    colorCollection = ['black', 'red', 'green', 'blue', 'cyan', 'yellow', 'magenta']
    randomColor = random.choice(colorCollection)
    # fontText = tkFont.Font(family='Helvetica')
    textHeight = 30

    def __init__(self, master, image):
        self.master = master
        master.title("Points indicator")

        self.frame = Frame(self.master, relief=SUNKEN, bg="red")
        self.frame.grid_rowconfigure(0, weight=1)
        self.frame.grid_columnconfigure(0, weight=1)
        self.frame.pack(fill=BOTH, expand=1)
        # Menu
        self.menu_bar = Menu(self.master)

        # create a pull-down menu, and add it to the menu bar
        file_menu = Menu(self.menu_bar, tearoff=0)
        file_menu.add_command(label="Open", command=self.open_file)
        file_menu.add_command(label="Save", command=self.save_to)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.master.quit)
        self.menu_bar.add_cascade(label="File", menu=file_menu)
        self.master.config(menu=self.menu_bar)

        self.master.geometry(str(image.width()) + 'x' + str(image.height() + 250))
        self.canvas = Canvas(self.frame, bg="black", bd=0, height=image.height(), width=image.width())
        self.canvas.grid(row=1, column=0, sticky=N + S + E + W)
        self.canvas.create_image(0, 0, image=image, anchor="nw")

        # Text area frame
        self.textCanvas = Canvas(self.frame, bd=0, bg='blue', height=230)
        self.textCanvas.grid(row=4, column=0, sticky=N + S + E + W)

        # text frame in canvas
        self.textFrame = Frame(self.textCanvas, relief=SUNKEN, bg="yellow")
        self.textFrame.grid_rowconfigure(0, weight=1)
        self.textFrame.grid_columnconfigure(0, weight=1)
        self.textCanvas.create_window(20, 20, anchor=NW, window=self.textFrame, width=(image.width() - 50), height=200)

        # text widget
        self.textContent = Text(self.textFrame, font='Arial')
        self.set_text_color_tags()
        self.textContent.pack(side=LEFT, fill=Y)

        # utility frame
        self.utilityFrame = Frame(self.textFrame, relief=SUNKEN)
        self.utilityFrame.pack(side=LEFT, fill=BOTH)

        # listbox widget
        self.comboBox = Combobox(self.utilityFrame, width=20)
        self.comboBox['values'] = ('Text', 'Json', 'Html')
        self.comboBox.current(0)
        self.comboBox['state'] = 'readonly'
        self.comboBox.pack(padx=10, pady=5, anchor=N)

        # button frame: for spacing from the combobox
        self.btnFrame = Frame(self.utilityFrame)
        self.btnFrame.pack(padx=10, pady=50)

        # Copy Button widget
        self.copyBtn = Button(self.btnFrame, text='Copy text')
        self.copyBtn.pack()

        # clipboard indicator
        self.cpMsgLabel = Label(self.utilityFrame, text='text copié!')

        # popup entry value
        self.roomLabel = StringVar()

        # Les traces de ligne
        self.canvasLigneCollection = []

        # bind mouse-click event
        self.canvas.bind("<Button 1>", self.add_line)
        self.canvas.bind("<Button 3>", self.cancel_draw)
        self.comboBox.bind('<<ComboboxSelected>>', self.generate_text)
        self.copyBtn.bind("<Button 1>", self.copy_text_to_clipboard)

    def end_draw_cycle(self, popup):

        popup.destroy()
        polygone_str = self.get_formatted_coordinates(self.polygone)
        self.textContent.insert('end', self.roomLabel.get() + ': ' + polygone_str+'\n', self.randomColor)
        self.polygoneCollection[self.roomLabel.get()] = polygone_str
        self.roomLabel.set('')
        self.polygone = []
        self.canvasLigneCollection = []
        self.randomColor = self.get_no_repeat_color()
        print('restart!')
        print(self.polygoneCollection)

    def popup_entry(self):

        popup = Toplevel()
        popup.wm_title("Saisir un label")
        popup.wm_geometry("%dx%d%+d%+d" % (220, 80, 450, 300))

        popup_label = Label(popup, text="Label : ")
        popup_label.grid(row=0, padx=10, pady=10)

        entry = Entry(popup, textvariable=self.roomLabel)
        entry.grid(row=0, column=1, padx=10, pady=10)
        entry.focus_set()

        button = Button(popup, text="Ok", command=lambda: self.end_draw_cycle(popup))
        button.grid(row=1, columnspan=2, padx=10, pady=10)

    def get_formatted_coordinates(self, the_polygone):
        """
        Retourne un String de coordonées de polygone sous forme: "x0, y0 x1, y1 ... "
        """
        formatted_coordinates = ''
        for i in range(len(self.polygone)):
            if i % 2 == 0:  # indice paire (x)
                formatted_coordinates += (str(the_polygone[i]) + ',')
            else:  # impaire (y)
                formatted_coordinates += (str(the_polygone[i]) + ' ')
        return formatted_coordinates

    def get_no_repeat_color(self):
        """
        Retourne une couleur dans la colorCollection autre que la variable 'randomColor'
        Pour éviter d'avoir 2 fois la suite la meme couleur
        """
        color_collection_copie = self.colorCollection.copy()
        color_collection_copie.remove(self.randomColor)
        return random.choice(color_collection_copie)

    def add_line(self, event):
        """
        MouseClick event pour tracer les polygones
        """
        if self.x0 == -1 and self.y0 == -1:  # start drawing
            self.x0 = event.x
            self.y0 = event.y
            self.x_start = self.x0
            self.y_start = self.y0
            self.polygone.append(self.x_start)
            self.polygone.append(self.y_start)
        else:  # in drawing
            self.x1 = event.x
            self.y1 = event.y
            canvas_ligne = self.canvas.create_line(self.x0, self.y0, self.x1, self.y1, fill=self.randomColor)
            self.canvasLigneCollection.append(canvas_ligne)
            if ((self.x_start-5) <= self.x1 <= (self.x_start+5)) and ((self.y_start-5) <= self.y1 <= (self.y_start+5)):
                # endPoint ~ start point (in a range of 5 pixels ): end 1 cycle draw
                self.x0 = -1
                self.y0 = -1
                self.canvas.create_polygon(' '.join(str(points) for points in self.polygone), fill=self.randomColor)
                self.popup_entry()
            else:
                self.x0 = self.x1
                self.y0 = self.y1
                self.polygone.append(self.x0)
                self.polygone.append(self.y0)

    def cancel_draw(self, e):
        self.x0 = self.y0 = self.x_start = self.y_start = -1
        self.polygone = []
        self.popup("Tracage annulé.")
        for canvasLigne in self.canvasLigneCollection:
            self.canvas.delete(canvasLigne)
        self.canvasLigneCollection = []

    def popup(self, msg):
        popup = Toplevel(self.master)
        popup.wm_title("Info")
        popup.wm_geometry("%dx%d%+d%+d" % (220, 80, 450, 300))

        popup_label = Label(popup, text=msg)
        popup_label.grid(row=0, padx=65, pady=10)

        button = Button(popup, text="Ok", command=popup.destroy)
        button.grid(row=1, padx=65, pady=10)

    def generate_text(self, event):
        formatted_text = ''
        selection = event.widget.get()

        if selection == "Json":
            formatted_text = '{\n\tvalue: "", label: "", \n\tzones: [\n\t'
            for key, value in self.polygoneCollection.items():
                formatted_text += '\t{id: "' + key + '", points: "' + value + '"},\n\t'
            formatted_text = self.r_replace(formatted_text, ',', '', 1)
            formatted_text += ']\n}'
        elif selection == 'Html':
            for key, value in self.polygoneCollection.items():
                formatted_text += '<polygon id="' + key + '" class="st0" points="' + value + '"/>\n'
        else:
            for key, value in self.polygoneCollection.items():
                formatted_text += (key + ': ' + value + '\n')
        self.textContent.delete('1.0', END)
        self.textContent.insert('1.0', formatted_text)

    def copy_text_to_clipboard(self, e):
        text_area_values = self.textContent.get('1.0', END)
        self.master.clipboard_clear()
        self.master.clipboard_append(text_area_values)
        self.cpMsgLabel.pack(anchor=N)
        self.cpMsgLabel.after(2500, self.clear_msg_label)

    def clear_msg_label(self):
        self.cpMsgLabel.pack_forget()

    def set_text_color_tags(self):
        """
        Créer un textTag pour chaque couleur dans 'colorCollection'
        """
        for color in self.colorCollection:
            self.textContent.tag_config(color, foreground=color)

    def r_replace(self, s, old, new, occurrence):
        """
        Inversement remplacer le 'old' caracter 'occurrence' fois par 'new' caracter dans le string 's'
        """
        li = s.rsplit(old, occurrence)
        return new.join(li)

    def open_file(self):
        """
        TODO: change imageFile
        :return:
        """

    def save_to(self):
        """
        TODO: export du fichier json

        """
