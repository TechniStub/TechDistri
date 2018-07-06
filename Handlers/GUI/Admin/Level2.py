import tkinter as tk

class AdminHandler():
    def __init__(self, root, image, home):
        self.root = root

    def set(self, session):
        self.height = self.root.winfo_screenheight()
        self.width = self.root.winfo_screenwidth()
        
