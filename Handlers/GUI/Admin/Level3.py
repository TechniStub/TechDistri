import tkinter as tk

class AdminHandler():
    def __init__(self, root, image, home, rfid, database, queries, keyboard, image1, commonFunc, scrollLeft, scrollRight, session):
        self.root = root
        self.rfid = rfid
        self.finished = False
        self.db = database
        self.queries = queries
        self.keyboard = keyboard
        self.trashImage = image1
        self.continueVAR=False
        self.commonInst = commonFunc
        self.scrollLeft = scrollLeft
        self.scrollRight = scrollRight
        self.pageChanging = False

    def changeEdit(self, val):
        self.edit = val

    def continuing(self, _is):
        print(_is)
        self.continueVAR = _is

    def choiceHandler(self, frameId, buttonId):
        if frameId == 2: # database
            if buttonId == 1: # see
                print("Database - See")
            elif buttonId == 2: # edit
                print("Database - Edit")

    def changePage(self):
        self.pageChanging = True

    def set(self, session):
        self.height = self.root.winfo_screenheight()
        self.width = self.root.winfo_screenwidth()
        self.session = session

        # Bdd menu
        self.lDataBase = tk.Label(self.root, text="Base de donnée", font=("arial", 16), bg="#fff")
        self.lDataBase.place(anchor="nw", x=50, y=self.height/4)

        self.seeDBButton = tk.Button(self.root, command=lambda: self.choiceHandler(2, 1), text="Voir", height=1, width=6, font=("Arial", 14), bd=0, highlightthickness = 0, bg="#fd3303", activebackground="#000", fg="#fff", activeforeground="#fff", pady=2)
        self.seeDBButton.place(anchor="center", y=self.height/4+45, x=125)

        self.editDBButton = tk.Button(self.root, command=lambda: self.choiceHandler(2, 2), text="Modifier", height=1, width=8, font=("Arial", 14), bd=0, highlightthickness = 0, bg="#fd3303", activebackground="#000", fg="#fff", activeforeground="#fff", pady=2)
        self.editDBButton.place(anchor="center", y=self.height/4+45, x=255)

        # Change Admin Page
        if(self.session["sAdmin"]):
            self.changePageButton = tk.Button(self.root, image=self.scrollLeft, highlightthickness = 0, bd = 0, bg="#fff", command=lambda: self.changePage())
            self.changePageButton.place(anchor="center", y=700, x=130)
            self.pageLabel = tk.Label(self.root, text="2/2", font=("arial", 16), bg="#fff")
            self.pageLabel.place(anchor="center", y=700, x=240)
