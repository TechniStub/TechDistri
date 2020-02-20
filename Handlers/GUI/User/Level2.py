#
#    USER - LEVEL2
#

import tkinter as tk
import time

class UserHandler():
    def __init__(self, root, image):
        self.root = root
        self.isSelected = False
        self.logoTs = image
        self.selection = {}
        self.selection["qty"] = 1
        self.selection["total"] = 0
        self.selection["final"] = 0
        self.validated = False
        self.canceled = False
        self.isAnAppRunning=False

    def cancel(self):
        self.canceled = True
        self.isAnAppRunning=False
        self.poproot.destroy()

    def validate(self):
        self.validated = True
        self.cancel()

    def changeQty(self, pos):
        if(pos < self.ActiveProduct["stock"]):
            self.selection["qty"] = pos+1
            self.selection["total"] = self.selection["qty"] * self.ActiveProduct["price"]
            self.selection["final"] = self.session["credit"] - self.selection["total"]
            self.qtyButtons[pos]["background"] = "#eaeaea"

            for index in range(self.zSize):
                if(index != pos):
                    self.qtyButtons[index]["background"] = "#fff"

            self.lQtyChoice["text"]="Qty. Choisie : "+str(self.selection["qty"])
            #self.lQtyChoice.place(anchor="ne", x=450-30, y=30)

            self.lTotal["text"]="Total : "+str(self.selection["total"])+"€"
            #self.lTotal.place(anchor="ne", x=450-30, y=60)

            self.lCfinal["text"]="Credit final : "+str(self.selection["final"])+"€"
            #self.lCfinal.place(anchor="ne", x=450-30, y=90)

            self.poproot.update()

    def touchHandler(self, text):
        if self.isAnAppRunning:
            self.cancel()
        self.x=0
        # print("Touched {}{}".format(text[0], text[1]))
        self.ActiveProduct = {}
        # break time !
        for product in self.products:
            if(product["row"] == text[0] and product["col"] == text[1]):
                self.ActiveProduct = product
            else:
                self.ActiveProduct["id"] = -1

        if(self.ActiveProduct["id"] != -1):
            self.selection["product"] = self.ActiveProduct
            self.poproot = tk.Tk()
            self.isAnAppRunning = True
            ws = self.poproot.winfo_screenwidth() # width of the screen
            hs = self.poproot.winfo_screenheight() # height of the scre
            self.poproot.configure(background="white")
            self.poproot.geometry("450x250+{}+{}".format(int((ws/2) - (450/2)), int((hs/2) - (250/2))))
            self.poproot.title("Confirmation")

            self.lNom = tk.Label(self.poproot, text=self.ActiveProduct["nom"], font=("Arial bold italic", 14), bg="#fff")
            self.lNom.place(anchor="nw", x=30, y=30)

            self.lCredit = tk.Label(self.poproot, text="Credit : "+str(self.session["credit"])+"€", font=("Arial", 14), bg="#fff")
            self.lCredit.place(anchor="nw", x=30, y=60)

            self.lUnitPrice = tk.Label(self.poproot, text="Prix unité : "+str(self.ActiveProduct["price"])+" €", font=("Arial", 14), bg="#fff")
            self.lUnitPrice.place(anchor="nw", x=30, y=90)

            self.lQtyChoice = tk.Label(self.poproot, text="Qty. Choisie : "+str(self.selection["qty"]), font=("Arial", 14), bg="#fff")
            self.lQtyChoice.place(anchor="ne", x=450-30, y=30)

            self.lTotal = tk.Label(self.poproot, text="Total : "+str(self.selection["total"])+"€", font=("Arial", 14), bg="#fff")
            self.lTotal.place(anchor="ne", x=450-30, y=60)

            self.lCfinal = tk.Label(self.poproot, text="Credit final : "+str(self.selection["final"])+"€", font=("Arial", 14), bg="#fff")
            self.lCfinal.place(anchor="ne", x=450-30, y=90)

            self.validateButton = tk.Button(self.poproot, text="Valider", background="#fff", font=("Arial", 14), highlightthickness = 0, bd = 0, bg="#fff", command=lambda: self.validate())
            self.validateButton.place(anchor="se", x=450-30, y=250-30)

            self.cancelButton = tk.Button(self.poproot, text="Annuler", background="#fff", font=("Arial", 14), highlightthickness = 0, bd = 0, bg="#fff", command=lambda: self.cancel())
            self.cancelButton.place(anchor="sw", x=30, y=250-30)

            self.zSize = int(self.distriParam["stockRackMax"]["value"])
            coef = (450-(30*2)) / float(self.zSize)
            self.qtyButtons = []
            index = -1
            color = "#fff"
            state = "normal"

            for posB in range(self.zSize):
                index += 1
                xpos = (coef * posB) + 30*2
                if(posB >= (self.ActiveProduct["stock"])):
                    color = "#eaeaea"
                    state = "disabled"
                self.qtyButtons.append(tk.Button(self.poproot, state=state, text=posB+1, font=("Arial", 14), background="#fff", highlightthickness = 0, bd = 0, bg="#fff", command=lambda pos=posB:self.changeQty(pos)))
                self.qtyButtons[index].place(anchor="center", x=xpos, y=150)

            self.changeQty(-1) # set qty to 0
            self.poproot.update()

    def set(self, session, distriParam, products):
        self.products = products
        self.session = session
        self.distriParam = distriParam
        self.selection={}
        self.height = self.root.winfo_screenheight()
        self.width = self.root.winfo_screenwidth()
        self.lachat = tk.Label(self.root, text="Achat", font=("arial", 24), fg="#ff3500", bg="#fff", anchor='center')
        self.lachat.place(anchor="center", x=int(self.width/2), y=150)

        self.selection = {}
        self.selection["qty"] = 1
        self.selection["total"] = 0
        self.selection["final"] = 0
        self.validated = False

        self.sizex = int(distriParam["colqty"]["value"])
        self.sizey = int(distriParam["rowqty"]["value"])

        self.fuzed = []
        index = -1
        for group in distriParam["fusioned"]["value"].split(";"):
            index += 1
            self.fuzed.append([])
            for childs in group.split(","):
                self.fuzed[index].append(childs)

        self.buttons = []
        # print(self.fuzed)

        _passing = 0 # vieux passing
        xChanging = 0 # nbr de changement
        pos = (0,0)

        for _x in range(self.sizex): # boucle des colonnes
            self.buttons.append([])  # array des bouttons
            x=_x+1 # lisible :)
            for _y in range(self.sizey): # boucle des lignes
                y=_y+1 # lisible :)
                passing = 0 # est affiché
                idx = 0 # index
                for group in self.fuzed: # boucle renvoyant des arrays
                    idx += 1 # inc. de l'index
                    if str(str(y)+str(x)) in group: # la position est dans la matrice
                        passing = idx # c'est l'index
                    # print(str(str(y)+str(x)))

                if passing == 0: # affichage ?
                    ## ---------------- AFFICHAGE D'UN BOUTTON ----------------
                    pos = (y,x)
                    self.buttons[_x].append(tk.Button(self.root, text="{}{}".format(y, x), font=("Arial", 18), bd=0, highlightbackground="#fd3303", highlightcolor="#fd3303", highlightthickness=1, bg="#fff", activebackground="#000", fg="#000", activeforeground="#ffffff", pady=8, padx=12, command=lambda p=pos: self.touchHandler(p)))
                    self.buttons[_x][_y].place(x=42.5+(_x*(((self.width-70)/self.sizex))), y=240+(_y*(((self.width-175)/self.sizey))))
                else:
                    ## ---------------- AFFICHAGE D'UN BOUTTON SUR x ----------------
                    size = len(self.fuzed[passing-1])
                    if(passing != _passing):
                        _passing = passing
                        xChanging += 1
                        add = int((size/4.0) * (((self.width-460)/self.sizex)))

                        posx = 42.5+(_x*(((self.width-70)/self.sizex)))
                        posy = 240+(_y*(((self.width-175)/self.sizey)))

                        pos = (y,x)
                        self.buttons[_x].append(tk.Button(self.root, text="{}{}".format(y, xChanging), font=("Arial", 18), bd=0, highlightbackground="#fd3303", highlightcolor="#fd3303", highlightthickness=1, bg="#fff", activebackground="#000", fg="#000", activeforeground="#ffffff", pady=8, padx=45, command=lambda p=pos: self.touchHandler(p)))
                        self.buttons[_x][_y].place(x=posx+add, y=posy)
                    else:
                        self.buttons[_x].append(None)
