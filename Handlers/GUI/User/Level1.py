import tkinter as tk
import time

class UserHandler():
    def __init__(self, root, image):
        self.root = root
        self.isSelected = False
        self.logoTs = image
        self.selection = {}

    def cancel(self):
        print("Cancel")
        self.poproot.destroy()

    def validate(self):
        pass

    def changeQty(self, pos):
        self.selection["qty"] = pos+1
        self.qtyButtons[pos]["background"] = "#eaeaea"

        for index in range(self.zSize):
            if(index != pos):
                self.qtyButtons[index]["background"] = "#fff"

    def touchHandler(self, text):
        self.x=0
        print("Touched {}{}".format(text[0], text[1]))
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
            self.poproot.configure(background="white")
            self.poproot.geometry("450x250")
            self.poproot.title("Confirmation")

            self.lNom = tk.Label(self.poproot, text=self.ActiveProduct["nom"], font=("Arial", 14), bg="#fff")
            self.lNom.place(anchor="nw", x=30, y=30)

            self.lCredit = tk.Label(self.poproot, text="Credit : "+str(self.session["credit"]), font=("Arial", 14), bg="#fff")
            self.lCredit.place(anchor="nw", x=30, y=60)

            self.lUnitPrice = tk.Label(self.poproot, text="Prix unité : "+str(self.ActiveProduct["price"])+" €", font=("Arial", 14), bg="#fff")
            self.lUnitPrice.place(anchor="nw", x=30, y=90)

            self.validateButton = tk.Button(self.poproot, text="Valider", background="#fff", font=("Arial", 14), highlightthickness = 0, bd = 0, bg="#fff", command=lambda: self.validate)
            self.validateButton.place(anchor="se", x=450-30, y=250-30)

            self.cancelButton = tk.Button(self.poproot, text="Annuler", background="#fff", font=("Arial", 14), highlightthickness = 0, bd = 0, bg="#fff", command=lambda: self.cancel())
            self.cancelButton.place(anchor="sw", x=30, y=250-30)

            self.zSize = int(self.distriParam["stockRackMax"]["value"])
            coef = (450-(30*2)) / float(self.zSize)
            self.qtyButtons = []
            index = -1

            for posB in range(self.zSize):
                index += 1
                xpos = (coef * posB) + 30*2
                self.qtyButtons.append(tk.Button(self.poproot, text=posB+1, font=("Arial", 14), background="#fff", highlightthickness = 0, bd = 0, bg="#fff", command=lambda pos=posB:self.changeQty(pos)))
                self.qtyButtons[index].place(anchor="center", x=xpos, y=130)

            self.changeQty(0) # set qty to 1

            self.poproot.update()

    def set(self, session, distriParam, products):
        self.products = products
        self.session = session
        self.distriParam = distriParam
        self.height = self.root.winfo_screenheight()
        self.width = self.root.winfo_screenwidth()
        self.lachat = tk.Label(self.root, text="Achat", font=("Arial", 18), anchor='center', background="white")
        self.lachat.place(anchor="center", x=int(self.width/2), y=150)

        self.sizex = int(distriParam["colqty"]["value"])
        self.sizey = int(distriParam["rowqty"]["value"])

        self.fuzed = []
        index = -1
        for group in distriParam["fusioned"]["value"].split(","):
            index += 1
            self.fuzed.append([])
            for childs in group.split(";"):
                self.fuzed[index].append(childs)

        self.buttons = []

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

                if passing == 0: # affichage ?
                    ## ---------------- AFFICHAGE D'UN BOUTTON ----------------
                    pos = (y,x)
                    self.buttons[_x].append(tk.Button(self.root, text="{}{}".format(y, x), font=("Arial", 14), highlightthickness = 0, bd = 0, bg="#fff", command=lambda p=pos: self.touchHandler(p)))
                    self.buttons[_x][_y].place(x=50+(_x*(((self.width-70)/self.sizex))), y=200+(_y*(((self.width-50)/self.sizey))))
                else:
                    ## ---------------- AFFICHAGE D'UN BOUTTON SUR x ----------------
                    size = len(self.fuzed[passing-1])
                    if(passing != _passing):
                        _passing = passing
                        print("Changing")
                        xChanging += 1
                        add = int((size/4.0) * (((self.width-70)/self.sizex)))

                        posx = 50+(_x*(((self.width-70)/self.sizex)))
                        posy = 200+(_y*(((self.width-50)/self.sizey)))

                        pos = (y,x)
                        self.buttons[_x].append(tk.Button(self.root, text="{}{}".format(y, xChanging), font=("Arial", 14), highlightthickness = 0, bd = 0, bg="#fff", command=lambda p=pos: self.touchHandler(p)))
                        self.buttons[_x][_y].place(x=posx+add, y=posy)
                    else:
                        self.buttons[_x].append(None)
