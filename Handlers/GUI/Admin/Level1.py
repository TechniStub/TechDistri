import tkinter as tk

class AdminHandler():
    def __init__(self, root, image, home):
        self.root = root
        self.isSelected = False
        self.logoTs = image
        self.logoHome = home
        self.selected = 0
        self.goToHome = False

    def adminCallback(self):
        self.isSelected = True
        self.selected = 1 # admin

    def userCallback(self):
        self.isSelected = True
        self.selected = 3 # user

    def permCallback(self):
        self.isSelected = True
        self.selected = 2 # perm

    def home(self):
        self.goToHome = True

    def set(self, session):
        self.height = self.root.winfo_screenheight()
        self.width = self.root.winfo_screenwidth()

        self.buttonAdmin = tk.Button(self.root, text="Admin", height=1, width=20, command=self.adminCallback, font=("Arial", 18), bd=0, highlightthickness = 0, bg="#fd3303", activebackground="#000000", fg="#ffffff", activeforeground="#ffffff", pady=10)
        self.buttonAdmin.place(anchor="center", x=int(self.width/2), y=int(self.height/3))

        self.buttonPerm = tk.Button(self.root, text="Permanent", height=1, width=20, command=self.permCallback, font=("Arial", 18), bd=0, highlightthickness = 0, bg="#fd3303", activebackground="#000000", fg="#ffffff", activeforeground="#ffffff", pady=10)
        self.buttonPerm.place(anchor="center", x=int(self.width/2), y=int(self.height/3)+75)

        self.buttonUser = tk.Button(self.root, text="Utilisateur", height=1, width=20, command=self.userCallback, font=("Arial", 18), bd=0, highlightthickness = 0, bg="#fd3303", activebackground="#000000", fg="#ffffff", activeforeground="#ffffff", pady=10)
        self.buttonUser.place(anchor="center", x=int(self.width/2), y=int(self.height/3)+150)
