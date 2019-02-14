from tkinter import *
from tkinter.ttk import Button, Scale
from tkinter.filedialog import askopenfilename
from PIL import Image, ImageTk
from util.HTMLParser import MyHTMLParser
from util.FileHandler import FileHandler
from util.EmojiParser import with_surrogates
import random
import json

WINDOW_WIDTH = 1900
WINDOW_HEIGHT = 1080


class GUI:

    x0 = y0 = x1 = y1 = x_start = y_start = rect_x0 = rect_y0 = rect_x2 = rect_y2 = -1
    polygone = []
    # polygonesPointsCollection = []
    polygone_id_collection = {}
    polygoneCollection = {}
    colorCollection = ['black', 'red', 'green', 'blue', 'cyan', 'yellow', 'magenta']
    randomColor = random.choice(colorCollection)
    # fontText = tkFont.Font(family='Helvetica')
    textHeight = 30
    line_tmp = None
    # format de text in the text-area
    text_format = "txt"
    check_mark = u"\u2713"
    rect = None
    canvasLigneCollection = []
    the_last_draw = None

    def __init__(self, master):
        self.master = master
        self.master.title("Points indicator")

        # Mode de draw
        self.draw_mode = "point"

        # Image
        self.origin_image = None
        self.scale = 1.0
        self.img = None
        self.img_id = None

        # Menu
        self.menu_bar = Menu(self.master)
        self.create_menus()

        # main frame
        self.frame = Frame(self.master, relief=SUNKEN, bg="red", width=WINDOW_WIDTH)
        self.frame.grid_rowconfigure(0, weight=1)
        self.frame.grid_columnconfigure(0, weight=1)
        self.frame.pack(fill=None, expand=False)

        # scroll bars
        self.xscrollbar = Scrollbar(self.frame, orient=HORIZONTAL)
        self.xscrollbar.grid(row=2, column=0, columnspan=2, sticky=EW)

        self.yscrollbar = Scrollbar(self.frame)
        self.yscrollbar.grid(row=1, column=1, sticky=NS)

        # canvas to put image
        self.canvas = Canvas(self.frame, bg="black", bd=0,
                             height=(WINDOW_HEIGHT-400),
                             width=(WINDOW_WIDTH-100),
                             xscrollcommand=self.xscrollbar.set,
                             yscrollcommand=self.yscrollbar.set)
        self.canvas.grid(row=1, column=0, sticky=NSEW)
        self.xscrollbar.config(command=self.canvas.xview)
        self.yscrollbar.config(command=self.canvas.yview)

        # zoom utility buttons
        zoom_in_button = Button(self.frame, text="+", command=lambda: self.zoom(self.scale*2), width=3)
        zoom_out_button = Button(self.frame, text="-", command=lambda: self.zoom(self.scale*0.5), width=3)
        self.zoom_scale = Scale(self.frame, from_=1, to=3, length=80, command=self.on_scale, orient=VERTICAL)

        zoom_in_button.place(relx=0.92, rely=0.03)
        self.zoom_scale.place(relx=0.92, rely=0.07)
        zoom_out_button.place(relx=0.92, rely=0.18)

        # Frame to put text
        self.textFrame = Frame(self.frame, relief=SUNKEN, bg=self.master.cget('bg'),
                               width=WINDOW_WIDTH-100,
                               height=(WINDOW_HEIGHT-int(self.canvas['height'])-135))
        self.textFrame.grid_rowconfigure(0, weight=1)
        self.textFrame.grid_columnconfigure(0, weight=1)
        self.textFrame.grid(row=3, column=0, columnspan=2, sticky=NSEW)
        self.textFrame.grid_propagate(False)

        # text area widget
        self.textContent = Text(self.textFrame, font='Arial')
        self.textContent.grid(row=4, column=0, padx=25, pady=25, sticky=NSEW)
        self.set_text_color_tags()

        # popup entry value
        self.roomLabel = StringVar()

        # bind mouse-click event
        self.go_to_point_mode()  # point mode by default
        self.canvas.bind("<MouseWheel>", self.on_mouse_wheel)

    def create_menus(self):
        """
        create pull-down menus, and add it to the menu bar
        """
        # menu File
        file_menu = Menu(self.menu_bar, tearoff=0)
        file_menu.add_command(label="New Image", command=self.open_file)
        file_menu.add_command(label="Save Data", command=self.save_to)
        file_menu.add_command(label="Load From File", command=self.load_work_from_file)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.master.quit)
        self.menu_bar.add_cascade(label="File", menu=file_menu)
        self.master.config(menu=self.menu_bar)

        # menu Format
        convert_menu = Menu(self.menu_bar, tearoff=0)
        convert_menu.add_command(label="Json", command=lambda: self.generate_text("json"))
        convert_menu.add_command(label="Html", command=lambda: self.generate_text("html"))
        convert_menu.add_command(label="Text", command=lambda: self.generate_text("txt"))
        self.menu_bar.add_cascade(label="Format", menu=convert_menu)
        self.master.config(menu=self.menu_bar)

        # menu Tools
        tools_menu = Menu(self.menu_bar, tearoff=0)
        tools_menu.add_command(label="Copy text to clipboard", command=self.copy_text_to_clipboard)
        self.menu_bar.add_cascade(label="Tools", menu=tools_menu)
        self.master.config(menu=self.menu_bar)

        """
        menu Mode (draw mode): 
        [Point mode]: dessiner des polygones par des points
        [Drag mode]: dessiner des polygones par le tire d'une aire de polygone sur l'interface
        """
        draw_mode_menu = Menu(self.menu_bar, tearoff=0)
        draw_mode_menu.add_command(label=self.check_mark+" Point",
                                   command=lambda: self.change_draw_mode(draw_mode_menu, 'point'))
        draw_mode_menu.add_command(label=" Drag",
                                   command=lambda: self.change_draw_mode(draw_mode_menu, 'drag'))
        self.menu_bar.add_cascade(label="Mode", menu=draw_mode_menu)
        self.master.config(menu=self.menu_bar)

        # menu Undo
        menu_undo = Menu(self.menu_bar, tearoff=0)
        menu_undo.add_command(label="Remove the last polygone", command=self.undo_last_polygone)
        self.menu_bar.add_cascade(label="Undo", menu=menu_undo)
        self.master.config(menu=self.menu_bar)

    def end_draw_cycle(self, popup):
        if self.roomLabel.get() in self.polygoneCollection:
            self.popup("Id already exist and they are unique.", "#ff3838")
            self.roomLabel.set('')
        elif self.roomLabel.get() == '':
            self.popup("The id can't be empty.", "#ff3838")
        else:
            popup.destroy()
            polygone_str = self.get_formatted_coordinates(self.polygone)
            # self.textContent.insert('end', self.roomLabel.get() + ': ' + polygone_str+'\n', self.randomColor)
            self.polygoneCollection[self.roomLabel.get()] = polygone_str
            self.roomLabel.set('')
            self.polygone = []
            self.remove_polygone_lignes()
            self.randomColor = self.get_no_repeat_color()
            self.generate_text(self.text_format)
            print('restart!')
            print(self.polygoneCollection)

    def popup_entry(self):
        popup = Toplevel()
        popup.wm_title("Entry an id")
        popup.wm_geometry("%dx%d%+d%+d" % (220, 80, 450, 300))

        popup_label = Label(popup, text="Id : ")
        popup_label.grid(row=0, padx=10, pady=10)

        entry = Entry(popup, textvariable=self.roomLabel)
        entry.grid(row=0, column=1, padx=10, pady=10)
        entry.focus_set()
        entry.bind("<Return>", (lambda event: self.end_draw_cycle(popup)))

        button = Button(popup, text="Ok", command=lambda: self.end_draw_cycle(popup))
        button.grid(row=1, columnspan=2, padx=10, pady=10)
        popup.protocol("WM_DELETE_WINDOW", lambda: self.close_entry_popup_window(popup))

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
            # print(str(self.canvas.canvasx(self.x0)) + ', ' + str(self.canvas.canvasy(self.y0)))
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
                self.the_last_draw = self.canvas.create_polygon(
                    ' '.join(str(points * self.scale) for points in self.polygone),
                    fill=self.randomColor)
                self.polygone_id_collection[self.the_last_draw] = self.randomColor
                # self.polygonesPointsCollection.append(self.polygone)
                self.popup_entry()
            else:
                self.x0 = self.x1
                self.y0 = self.y1
                # print(str(self.canvas.canvasx(self.x1)) + ', ' + str(self.canvas.canvasy(self.y1)))
                """
                print(str(self.x1) + ', ' + str(self.y1))
                self.x0 = self.mutate_point(self.x1)
                self.y0 = self.mutate_point(self.y1)
                print("after: " + str(self.x0) + ", " + str(self.y0))
                """
                self.polygone.append(self.canvas.canvasx(self.x0, 0.5) / self.scale)
                self.polygone.append(self.canvas.canvasy(self.y0, 0.5) / self.scale)

    """ [TODO]: draw with a polygone near by
    def mutate_point(self, point):
        if self.polygonesPointsCollection:
            for polygonPoints in self.polygonesPointsCollection:
                for pt in polygonPoints:
                    if (pt-10) <= point <= (pt+10):
                        return pt
        return point
    """

    def cancel_draw(self, e):
        self.x0 = self.y0 = self.x_start = self.y_start = -1
        self.polygone = []
        self.popup("Draw cancelled.")
        self.remove_polygone_lignes()

    def popup(self, msg, text_color=None):
        popup = Toplevel(self.master)
        # popup window par rapport a l'écran TODO: center to root window
        popup.wm_title("Info")
        popup.wm_geometry("%dx%d%+d%+d" % (220, 80, 450, 300))

        if text_color:
            popup_label = Label(popup, text=msg, fg=text_color)
        else:
            popup_label = Label(popup, text=msg)
        popup_label.grid(row=0, padx=10, pady=10)

        button = Button(popup, text="Ok", command=popup.destroy)
        button.grid(row=1, padx=65, pady=10)

    def on_mouse_wheel(self, event):
        self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    def generate_text(self, text_format):
        formatted_text = ''

        if text_format == "json":
            formatted_text = '{\n\t"value": "", "label": "", \n\t"zones": [\n\t'
            for key, value in self.polygoneCollection.items():
                formatted_text += '\t{"id": "' + key + '", "points": "' + value + '"},\n\t'
            formatted_text = self.r_replace(formatted_text, ',', '', 1)
            formatted_text += ']\n}'
            self.text_format = "json"
        elif text_format == 'html':
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
        self.popup("Text copied to clipboard, [Ctrl]+[V] to paste.")

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

    def zoom(self, zoom_scale):
        if 1 <= zoom_scale <= 4:
            self.scale = zoom_scale
            self.zoom_scale.set(self.scale)
            self.load_image()
            self.redraw_all_polygone()

    def load_image(self):
        self.canvas.delete("all")
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
        file = askopenfilename(parent=self.master, initialdir="C:/", title='Choose a file to open')
        if file:
            self.origin_image = Image.open(file)
            self.load_image()

    def on_button_press(self, event):
        """
        Set x0, y0 du rectangle
        :param event: on click event
        """
        self.rect = None
        self.rect_x0 = self.canvas.canvasx(event.x) / self.scale
        self.rect_y0 = self.canvas.canvasy(event.y) / self.scale

    def on_move_press(self, event):
        if self.rect:
            self.canvas.delete(self.rect)
        self.rect_x2 = self.canvas.canvasx(event.x)
        self.rect_y2 = self.canvas.canvasy(event.y)
        # expand rectangle as you drag the mouse
        self.rect = self.canvas.create_rectangle(
            self.rect_x0 * self.scale, self.rect_y0 * self.scale, self.rect_x2, self.rect_y2, fill=self.randomColor)

    def on_button_release(self, event):
        self.polygone.extend(
            [self.rect_x0, self.rect_y0,
             self.rect_x2 / self.scale, self.rect_y0,
             self.rect_x2 / self.scale, self.rect_y2 / self.scale,
             self.rect_x0, self.rect_y2 / self.scale]
        )
        self.the_last_draw = self.rect
        self.polygone_id_collection[self.the_last_draw] = self.randomColor
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
            self.text_format = my_file_handler.file_extension.replace('.', '')
        self.reload_text_content(content)

    def reinit_variables_from_content(self, content_text, extension):
        # clean global variables
        self.clean_global_variables()
        self.polygone_id_collection = {}
        self.polygoneCollection = {}

        # Initialisation des datas quand reload
        if extension == '.json':
            json_obj = json.loads(content_text)
            for zone in json_obj['zones']:
                points = zone['points'].replace(',', ' ')
                polygone = self.canvas.create_polygon(points, fill=self.randomColor)
                self.polygone_id_collection[polygone] = ''
                self.polygoneCollection[zone['id']] = zone['points']
        elif extension == '.html':
            my_html_parser = MyHTMLParser()
            my_html_parser.feed(content_text)
            for polygone in my_html_parser.polygone_collection:
                points = polygone[2][1].replace(',', ' ')
                polygone = self.canvas.create_polygon(points, fill=self.randomColor)
                self.polygone_id_collection[polygone] = ''
                self.polygoneCollection[polygone[0][1]] = polygone[2][1]
        elif extension == '.txt':
            structured_data = content_text.rstrip('\n')
            structured_data = [s.split(': ') for s in structured_data.splitlines()]
            for polygon in structured_data:
                points = polygon[1].replace(',', ' ')
                polygone = self.canvas.create_polygon(points, fill=self.randomColor)
                self.polygone_id_collection[polygone] = ''
                self.polygoneCollection[polygon[0]] = polygon[1]
        self.randomColor = self.get_no_repeat_color()

    def on_scale(self, event):
        value = self.zoom_scale.get()
        if int(value) != value:
            self.zoom_scale.set(round(value))
            self.scale = round(value)
            self.zoom(round(value))

    def undo_last_polygone(self):
        """
        clean the last drawn
        """
        if self.polygone_id_collection:
            self.canvas.delete(list(self.polygone_id_collection.items())[-1][0])
            self.polygone_id_collection.popitem()
            # self.canvas.delete(self.the_last_draw)
            self.clean_global_variables()
            self.polygoneCollection.popitem()
            self.generate_text(self.text_format)

    def change_draw_mode(self, menu, mode_to_change):
        """
        Fonction qui change le mode de draw entre "point mode" et "drag mode"
        """
        if mode_to_change != self.draw_mode:
            # TODO: [clean] separer le switch de menu dans 2 fonction differents
            if mode_to_change == 'point':
                self.go_to_point_mode()
                menu.entryconfig(0, label=self.check_mark + ' Point')
                menu.entryconfig(2, label=' Drag')
            elif mode_to_change == 'drag':
                self.go_to_drag_mode()
                menu.entryconfig(0, label=' Point')
                menu.entryconfig(2, label=self.check_mark + ' Drag')
            self.draw_mode = mode_to_change

    def go_to_point_mode(self):
        self.clean_global_variables()
        self.canvas.unbind("<ButtonRelease 1>")
        self.canvas.unbind("<B1-Motion>")
        self.canvas.bind("<Button 1>", self.add_line)
        self.canvas.bind("<Motion>", self.preview_line)
        self.canvas.bind("<Button 3>", self.cancel_draw)

    def go_to_drag_mode(self):
        """
        [Drag Mode]
        """
        self.clean_global_variables()
        self.canvas.unbind("<Button 3>")
        self.canvas.bind("<Button 1>", self.on_button_press)
        self.canvas.bind("<B1-Motion>", self.on_move_press)
        self.canvas.bind("<ButtonRelease 1>", self.on_button_release)

    def clean_global_variables(self):
        """
        Réinitialiser les variables globales sauf la collection de polygone :polygoneCollection
        """
        self.x0 = self.y0 = self.x1 = self.y1 = self.x_start = self.y_start = self.rect_x0 = self.rect_y0 = self.rect_x2 = self.rect_y2 = -1
        self.polygone = []
        self.randomColor = self.get_no_repeat_color()
        self.line_tmp = None
        self.rect = None

    def close_entry_popup_window(self, popup, event=None):
        popup.destroy()
        self.canvas.delete(self.the_last_draw)
        self.remove_polygone_lignes()
        self.clean_global_variables()

    def remove_polygone_lignes(self):
        for canvasLigne in self.canvasLigneCollection:
            self.canvas.delete(canvasLigne)
        self.canvasLigneCollection = []

    def redraw_all_polygone(self):
        for polygone_coordinates in self.polygoneCollection.values():
            points = polygone_coordinates.replace(',', ' ').rstrip().split(' ')
            points = [float(point) * self.scale for point in points]
            canvas_coord = ' '.join(str(s) for s in points)
            polygone = self.canvas.create_polygon(canvas_coord, fill=self.randomColor)
            self.polygone_id_collection[polygone] = ''
