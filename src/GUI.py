from tkinter import *
from tkinter.ttk import Button
from tkinter.filedialog import askopenfilename
from PIL import Image, ImageTk
from util.FileHandler import FileHandler
import random


class GUI:

    x0 = y0 = x1 = y1 = x_start = y_start = -1
    polygone = []
    polygonesPointsCollection = []
    polygoneCollection = {}
    colorCollection = ['black', 'red', 'green', 'blue', 'cyan', 'yellow', 'magenta']
    randomColor = random.choice(colorCollection)
    # fontText = tkFont.Font(family='Helvetica')
    textHeight = 30
    line_tmp = None
    # format de text in the text-area
    text_format = "txt"

    def __init__(self, master, image):
        self.master = master
        master.title("Points indicator")

        # Image
        self.origin_image = image
        self.scale = 1.0
        self.img = None
        self.img_id = None

        # Menu
        self.menu_bar = Menu(self.master)
        self.create_menus()

        # main frame
        self.frame = Frame(self.master, relief=SUNKEN, bg="red", width=800)
        self.frame.grid_rowconfigure(0, weight=1)
        self.frame.grid_columnconfigure(0, weight=1)
        self.frame.pack(fill=None, expand=False)

        # scroll bars
        self.xscrollbar = Scrollbar(self.frame, orient=HORIZONTAL)
        self.xscrollbar.grid(row=2, column=0, sticky=EW)

        self.yscrollbar = Scrollbar(self.frame)
        self.yscrollbar.grid(row=1, column=1, sticky=NS)

        # canvas for image
        self.canvas = Canvas(self.frame, bg="black", bd=0, height=self.origin_image.height, width=self.origin_image.width, xscrollcommand=self.xscrollbar.set, yscrollcommand=self.yscrollbar.set)
        self.canvas.grid(row=1, column=0, sticky=NSEW)
        self.xscrollbar.config(command=self.canvas.xview)
        self.yscrollbar.config(command=self.canvas.yview)

        # draw the initial image at 1x scale
        self.load_image()

        # zoom utility frame
        zoom_frame = Frame(self.frame, relief=SUNKEN, bg="black", width=5)
        zoom_frame.grid(row=1, column=2, sticky=N, pady=20)
        # zoom utility buttons
        zoom_in_button = Button(zoom_frame, text="+", command=lambda: self.zoom("in"), width=3)
        zoom_out_button = Button(zoom_frame, text="-", command=lambda: self.zoom("out"), width=3)
        zoom_in_button.grid(row=0, column=0, padx=2, pady=5)
        zoom_out_button.grid(row=1, column=0, padx=2, pady=5)

        # Text area canvas
        self.textCanvas = Canvas(self.frame, bd=0, bg='#f5f5f0', height=230)
        self.textCanvas.grid(row=4, column=0, sticky=NSEW)

        # text frame in canvas
        self.textFrame = Frame(self.textCanvas, relief=SUNKEN, bg="#f5f5f0")
        self.textFrame.grid_rowconfigure(0, weight=1)
        self.textFrame.grid_columnconfigure(0, weight=1)
        self.textCanvas.create_window(20, 20, anchor=NW, window=self.textFrame, width=(image.width - 50), height=200)

        # text area widget
        self.textContent = Text(self.textFrame, font='Arial')
        self.set_text_color_tags()
        self.textContent.grid(row=0, column=0, padx=10, sticky=NSEW)

        # popup entry value
        self.roomLabel = StringVar()

        # Les traces de ligne
        self.canvasLigneCollection = []

        # bind mouse-click event
        self.canvas.bind("<Button 1>", self.add_line)
        self.canvas.bind("<Motion>", self.preview_line)
        self.canvas.bind("<Button 3>", self.cancel_draw)
        self.canvas.bind("<MouseWheel>", self.on_mouse_wheel)

        # Tracer du rectangle en 1 click
        self.x = self.y = 0 
        self.rect = None
        self.canvas.bind("<ButtonPress-1>", self.on_button_press)
        self.canvas.bind("<B1-Motion>", self.on_move_press)
        self.canvas.bind("<ButtonRelease-1>", self.on_button_release)

    def create_menus(self):
        """
        create pull-down menus, and add it to the menu bar
        """
        file_menu = Menu(self.menu_bar, tearoff=0)
        file_menu.add_command(label="New Image", command=self.open_file)
        file_menu.add_command(label="Save Data", command=self.save_to)
        file_menu.add_command(label="Load From File", command=self.load_work_from_file)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.master.quit)
        self.menu_bar.add_cascade(label="File", menu=file_menu)
        self.master.config(menu=self.menu_bar)

        convert_menu = Menu(self.menu_bar, tearoff=0)
        convert_menu.add_command(label="json", command=lambda: self.generate_text("Json"))
        convert_menu.add_command(label="html", command=lambda: self.generate_text("Html"))
        convert_menu.add_command(label="text", command=lambda: self.generate_text("Text"))
        self.menu_bar.add_cascade(label="Format", menu=convert_menu)
        self.master.config(menu=self.menu_bar)

        tools_menu = Menu(self.menu_bar, tearoff=0)
        tools_menu.add_command(label="Copy text to clipboard", command=self.copy_text_to_clipboard)
        self.menu_bar.add_cascade(label="Tools", menu=tools_menu)
        self.master.config(menu=self.menu_bar)

    def end_draw_cycle(self, popup):

        popup.destroy()
        polygone_str = self.get_formatted_coordinates(self.polygone)
        print(self.polygone)
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
        entry.bind("<Return>", (lambda event: self.end_draw_cycle(popup)))

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
        if self.x0 == -1 and self.y0 == -1:  # start drawing (start point: x0, y0)
            self.x0 = event.x
            self.y0 = event.y
            print(str(self.canvas.canvasx(self.x0)) + ', ' + str(self.canvas.canvasy(self.y0)))
            self.x_start = self.x0
            self.y_start = self.y0
            """
            self.x_start = self.mutate_point(self.x0)
            if self.x_start != self.x0:
                self.y_start = self.mutate_point(self.y0)
            else:
                self.y_start = self.y0
            print("after: " + str(self.x_start) + ", " + str(self.y_start))
            """
            self.polygone.append(self.canvas.canvasx(self.x_start) / self.scale)
            self.polygone.append(self.canvas.canvasy(self.y_start) / self.scale)
        else:  # in drawing
            self.x1 = event.x
            self.y1 = event.y
            print("x0, y0: " + str(self.x0) + ", " + str(self.y0))
            print("canvas x0, y0: " + str(self.canvas.canvasx(self.x0)) + ", " + str(self.canvas.canvasy(self.y0)))
            print("canvas scale x0, y0: " + str(self.canvas.canvasx(self.x0) / self.scale) + ", " + str(self.canvas.canvasy(self.y0) / self.scale))
            canvas_ligne = self.canvas.create_line(
                self.canvas.canvasx(self.x0),
                self.canvas.canvasy(self.y0),
                self.canvas.canvasx(self.x1),
                self.canvas.canvasy(self.y1),
                fill=self.randomColor)
            self.canvasLigneCollection.append(canvas_ligne)
            if ((self.x_start-5) <= self.x1 <= (self.x_start+5)) and ((self.y_start-5) <= self.y1 <= (self.y_start+5)):
                # endPoint ~ start point (in a range of 5 pixels ): end 1 cycle draw
                self.x0 = -1
                self.y0 = -1
                self.canvas.create_polygon(' '.join(str(points * self.scale) for points in self.polygone), fill=self.randomColor)
                # self.polygonesPointsCollection.append(self.polygone)
                self.popup_entry()
            else:
                self.x0 = self.x1
                self.y0 = self.y1
                print(str(self.canvas.canvasx(self.x1)) + ', ' + str(self.canvas.canvasy(self.y1)))
                """
                print(str(self.x1) + ', ' + str(self.y1))
                self.x0 = self.mutate_point(self.x1)
                self.y0 = self.mutate_point(self.y1)
                print("after: " + str(self.x0) + ", " + str(self.y0))
                """
                self.polygone.append(self.canvas.canvasx(self.x0, 0.5) / self.scale)
                self.polygone.append(self.canvas.canvasy(self.y0, 0.5) / self.scale)

    def mutate_point(self, point):
        if self.polygonesPointsCollection:
            for polygonPoints in self.polygonesPointsCollection:
                for pt in polygonPoints:
                    if (pt-10) <= point <= (pt+10):
                        return pt
        return point

    def cancel_draw(self, e):
        self.x0 = self.y0 = self.x_start = self.y_start = -1
        self.polygone = []
        self.popup("Traçage annulé.")
        for canvasLigne in self.canvasLigneCollection:
            self.canvas.delete(canvasLigne)
        self.canvasLigneCollection = []

    def popup(self, msg):
        popup = Toplevel(self.master)
        # popup window par rapport a l'écran TODO: center to root window
        popup.wm_title("Info")
        popup.wm_geometry("%dx%d%+d%+d" % (220, 80, 450, 300))

        popup_label = Label(popup, text=msg)
        popup_label.grid(row=0, padx=10, pady=10)

        button = Button(popup, text="Ok", command=popup.destroy)
        button.grid(row=1, padx=65, pady=10)

    def on_mouse_wheel(self, event):
        self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    def generate_text(self, text_format):
        formatted_text = ''

        if text_format == "Json":
            formatted_text = '{\n\t"levels": [\n\t\t{\n\t\t\t"value": "",\n\t\t\t"label": "",\n\t\t\t"zones": [\n\t\t'
            for key, value in self.polygoneCollection.items():
                formatted_text += '\t\t{\n\t\t\t\t\t"id": "' + key + '",\n\t\t\t\t\t"points": "' + value + '"\n\t\t\t\t},\n\t\t'
            formatted_text = self.r_replace(formatted_text, ',', '', 1)
            formatted_text += '\t]\n\t\t}\n\t]\n}'
            self.text_format = "json"        
        elif text_format == 'Html':
            for key, value in self.polygoneCollection.items():
                formatted_text += '<polygon id="' + key + '" class="st0" points="' + value + '"/>\n'
            self.text_format = "html"
        else:
            for key, value in self.polygoneCollection.items():
                formatted_text += (key + ': ' + value + '\n')
            self.text_format = "txt"
        self.reload_text_content(formatted_text)

    def reload_text_content(self, text):
        self.textContent.delete('1.0', END)
        self.textContent.insert('1.0', text)

    def copy_text_to_clipboard(self):
        text_area_values = self.textContent.get('1.0', END)
        self.master.clipboard_clear()
        self.master.clipboard_append(text_area_values)
        self.popup("Text a été copié, [Ctrl]+[V] pour coller.")

    def set_text_color_tags(self):
        """
        Créer un textTag pour chaque couleur dans 'colorCollection'
        """
        for color in self.colorCollection:
            self.textContent.tag_config(color, foreground=color)

    def r_replace(self, s, old, new, occurrence):
        """
        Inversement remplacer le 'old' character 'occurrence' fois par 'new' caracter dans le string 's'
        """
        li = s.rsplit(old, occurrence)
        return new.join(li)

    def preview_line(self, event):
        if self.line_tmp:
            self.canvas.delete(self.line_tmp)
            self.line_tmp = None
        if self.x0 != -1 and self.y0 != -1:
            x_start = self.x0
            y_start = self.y0
            self.line_tmp = self.canvas.create_line(
                self.canvas.canvasx(x_start),
                self.canvas.canvasy(y_start),
                self.canvas.canvasx(event.x),
                self.canvas.canvasy(event.y),
                fill=self.randomColor)

    def zoom(self, zoom_type):
        if zoom_type == "in":
            self.scale *= 2
        elif zoom_type == "out":
            self.scale *= 0.5
        self.load_image()

    def load_image(self):
        if self.img_id:
            self.canvas.delete(self.img_id)
        image_width, image_height = self.origin_image.size
        size = int(image_width * self.scale), int(image_height * self.scale)
        self.img = ImageTk.PhotoImage(self.origin_image.resize(size))
        self.img_id = self.canvas.create_image(0, 0, image=self.img, anchor=NW)

        # tell the canvas to scale up/down the vector objects as well
        self.canvas.scale(ALL, 0, 0, self.scale, self.scale)
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def open_file(self):
        """
        [menu][File][Open] changer l'image sur la quelle qu'on travail
        """
        self.load_image()
        file = askopenfilename(parent=self.master, initialdir="C:/", title='Choose a file to open')
        self.origin_image = Image.open(file)
        self.load_image()

    def on_button_press(self, event):
        self.x = event.x
        self.y = event.y
        if not self.rect:
            self.rect = self.canvas.create_rectangle(self.x, self.y, self.x, self.y, outline='black')

    def on_move_press(self, event):
            
        curX = self.canvas.canvasx(event.x)
        curY = self.canvas.canvasy(event.y)
        # expand rectangle as you drag the mouse
        self.canvas.coords(self.rect, self.x, self.y, curX, curY)    

    def on_button_release(self, event):
        #coin haut gauche
        x0,y0 = (self.x, self.y)
        #coin bas droite
        x2,y2 = (event.x, event.y)
        #coin haut droite
        x1,y1 = (x2, y0)
        #coin bas gauche
        x3,y3 = (x0, y2)

        tab_x = [x0,x1,x2,x3]
        tab_y = [y0,y1,y2,y3]
        i = 0
        while i < 4:
            self.polygone.append(tab_x[i])
            self.polygone.append(tab_y[i])
            i+=1
        self.canvas.create_polygon(' '.join(str(points) for points in self.polygone), fill=self.randomColor)
        self.popup_entry()    

    def save_to(self):
        """
        [menu][File][Save] export de fichier
        """
        my_file_handler = FileHandler(self.master)
        my_file_handler.export_file(self.textContent.get(1.0, END), self.text_format)

    def load_work_from_file(self):
        """
        [menu][File][Load_from_file] export de fichier
        """
        my_file_handler = FileHandler(self.master)
        content = my_file_handler.load_file()
        if my_file_handler.file_extension:
            self.reinit_variables_from_content(content, my_file_handler.file_extension)
        self.reload_text_content(content)

    def reinit_variables_from_content(self, contentText, extension):
        # TODO: initialisation des datas quand reload
        if extension == 'json':
            print("json")
        elif extension == 'html':
            print("html")
        elif extension == 'txt':
            print("txt")