from tkinter import*
from tkinter.filedialog import askdirectory

class ExportFile:
        def export(self, root, stringFile, fileName):
                file = askdirectory(parent=root, initialdir="C:/",title='')
                f= open(file + '/' + fileName,"w+")
                f.write(stringFile)
                f.close()

