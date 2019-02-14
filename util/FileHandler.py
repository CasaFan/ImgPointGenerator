from tkinter.filedialog import asksaveasfilename, askopenfilename
import os


class FileHandler:

    EXPORT_FILE_TYPES = [("text files", "*.txt"), ("json files", "*.json"), ("html files", "*.html")]
    IMAGE_FILE_TYPES = [("PNG", "*.png"), ("JPEG", "*.jpeg *.jpg"), ("Bitmap", "*.bmp")]
    file_path = None
    file_extension = None

    def __init__(self, root):
        self.root = root

    def export_file(self, content_str, extension):
        self.file_path = asksaveasfilename(
            parent=self.root,
            initialdir="C:/",
            title="Select",
            defaultextension=extension)
        try:
            file = open(self.file_path, "w+")
            file.write(content_str)
        except IOError:
            print('Can not open/write', self.file_path)
        else:
            file.close()

    def load_file(self):
        file = askopenfilename(
            parent=self.root,
            initialdir="C:/",
            title='Choose a file to load',
            filetypes=self.EXPORT_FILE_TYPES)

        self.file_path, self.file_extension = os.path.splitext(file)
        try:
            file = open(file)  # open for RO by default
        except IOError:
            print('Can not open/write', self.file_path)
        else:
            return file.read()
