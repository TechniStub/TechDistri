import tkinter as tk

class UserHandler():
    def __init__(self, root, image):
        self.root = root
        self.selection = 0
        self.logoTs = image

    def achatCallback(self):
        self.selection = 1

    def histoCallback(self):
        self.selection = 2

    def home(self):
        self.goToHome = True

    def set(self, session):
        self.height = self.root.winfo_screenheight()
        self.width = self.root.winfo_screenwidth()

        self.selection = 0

        # Miaou v (button a chat)
        self.buttonAchat = tk.Button(self.root, text="Achat", height=1, width=20, command=self.achatCallback, font=("Arial", 18), bd=0, highlightthickness = 0, bg="#fd3303", activebackground="#000000", fg="#ffffff", activeforeground="#ffffff", pady=10)
        self.buttonAchat.place(anchor="center", x=int(self.width/2), y=int(self.height/3))

        self.buttonHisto = tk.Button(self.root, text="Historique", height=1, width=20, command=self.histoCallback, font=("Arial", 18), bd=0, highlightthickness = 0, bg="#fd3303", activebackground="#000000", fg="#ffffff", activeforeground="#ffffff", pady=10)
        self.buttonHisto.place(anchor="center", x=int(self.width/2), y=int(self.height/3)+75)

        self.root.update()
