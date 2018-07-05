import tkinter as tk
import time

class UserHandler():
    def __init__(self, root, image):
        self.root = root
        self.isSelected = False
        self.logoTs = image
        self.selected = 0
        self.poproot = None

    def clearTk(self, toClr): # definition de la fonction d' éfacage du gui
        for widget in toClr.winfo_children():
            widget.destroy()

    def cancel(self):
        print("Cancel")
        self.clearTk(self.poproot)
        self.poproot.destroy()
        print(self.poproot)

    def validate(self):
        pass

    def touchHandler(self, text):
        print("Touched {}{}".format(text[0], text[1]))
        self.ActiveProduct = {}
        # break time !
        for product in self.products:
            if(product["row"] == text[0] and product["col"] == text[1]):
                self.ActiveProduct = product
            else:
                self.ActiveProduct["id"] = -1

        if(self.ActiveProduct["id"] != -1):
            self.poproot = tk.Tk()
            self.poproot.configure(background="white")
            self.poproot.geometry("450x200")
            self.poproot.title("Confirmation")

            self.lNom = tk.Label(self.poproot, text=self.ActiveProduct["nom"], font=("Arial", 14), bg="#fff")
            self.lNom.place(anchor="nw", x=30, y=30)

            """self.validate = tk.Button(self.poproot, text="Valider", background="#fff", font=("Arial", 14), highlightthickness = 0, bd = 0, bg="#fff", command=lambda: self.validate)
            self.validate.place(anchor="se", x=450-30, y=200-30)"""

            self.cancel = tk.Button(self.poproot, text="Annuler", background="#fff", font=("Arial", 14), highlightthickness = 0, bd = 0, bg="#fff", command=self.cancel)
            self.cancel.place(anchor="sw", x=30, y=200-30)

    def set(self, session, distriParam, products):
        self.products = products
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
