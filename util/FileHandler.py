from tkinter.filedialog import asksaveasfilename, askopenfilename
import os


class FileHandler:

    FILE_TYPES = [("text files", "*.txt"), ("json files", "*.json"), ("html files", "*.html")]
    file_path = None
    file_extension = None

    def __init__(self, root):
        self.root = root

    def export_file(self, content_str, extension):
        self.file_path = asksaveasfilename(parent=self.root, initialdir="C:/", title="Select", defaultextension=extension)
        file = open(self.file_path, "w+")
        file.write(content_str)
        file.close()

    def load_file(self):
        file = askopenfilename(parent=self.root, initialdir="C:/", title='Choose a file to load', filetypes=self.FILE_TYPES)
        self.file_path, self.file_extension = os.path.splitext(file)
        file = open(file)  # open for RO by default
        print(self.file_extension)
        return file.read()
