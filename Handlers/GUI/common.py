import tkinter as tk

class commonGUIs():
    def __init__(self, root):
        self.root = root
        self.validated = False
        self.canceled = False

    def info(self, text, sizex=250, sizey=90, line=1):
        self.inforoot = tk.Toplevel(self.root)
        self.inforoot.transient(self.root)
        self.inforoot.grab_set()
        self.inforoot.configure(background="white")
        self.inforoot.geometry("{}x{}".format(sizex, sizey))
        self.inforoot.config(cursor="crosshair")
        self.inforoot.title("Info")
        self.okButton = tk.Button(self.inforoot, text="Ok", state="normal", background="#fff", font=("Arial", 14), highlightthickness = 0, bd = 0, bg="#fff", command=lambda: self.inforoot.destroy())
        self.okButton.place(anchor="center", x=sizex/2, y=sizey-30)
        size = int(len(text) / line)
        #lastAdd = len(text) - (size*line)
        self.textLabel=[]

        for index in range(line):
            if(index == line-1):
                self.textLabel.append(tk.Label(self.inforoot, text=text[index*size:], bg="#fff", highlightthickness=0, font=("arial", 16)))
                self.textLabel[index].place(anchor="center", x=sizex/2, y=30*(index+1))
            else:
                self.textLabel.append(tk.Label(self.inforoot, text=text[index*size:(index+1)*size], bg="#fff", highlightthickness=0, font=("arial", 16)))
                self.textLabel[index].place(anchor="center", x=sizex/2, y=30*(index+1))
        self.inforoot.update()

    def changeSure(self, val):
        self.sure=val

    def areSure(self, text):
        self.sureroot = tk.Toplevel(self.root)
        self.sureroot.transient(self.root)
        self.sureroot.grab_set()
        self.sure = 0
        self.sureroot.configure(background="white")
        self.sureroot.geometry("{}x{}".format(200, 90))
        self.sureroot.config(cursor="crosshair")
        self.sureroot.title("Etes vous sur ?")
        label = tk.Label(self.sureroot, text=text, bg='#fff', font=("arial", 14))
        label.place(anchor="center", x=200/2, y=30)
        self.oui = tk.Button(self.sureroot, text="Oui", background="#fff", command=lambda: self.changeSure(1), font=("Arial", 14), highlightthickness = 0, bd = 0, bg="#fff")
        self.oui.place(anchor="sw", x=10, y=80)
        self.non = tk.Button(self.sureroot, text="Non", background="#fff", command=lambda: self.changeSure(2), font=("Arial", 14), highlightthickness = 0, bd = 0, bg="#fff")
        self.non.place(anchor="se", x=200-10, y=80)
        self.sureroot.update()
        while self.sure == 0:
            self.sureroot.update()

        self.sureroot.destroy()
        return self.sure


    def newPopup(self, name, sizex=450, sizey=250):
        self.poproot = tk.Toplevel(self.root)
        self.poproot.transient(self.root)
        self.poproot.grab_set()
        self.ws = self.poproot.winfo_screenwidth() # width of the screen
        self.hs = self.poproot.winfo_screenheight() # height of the scre
        self.poproot.configure(background="white")
        self.poproot.config(cursor="crosshair")
        self.poproot.geometry("{}x{}+{}+{}".format(sizex, sizey, int((self.ws/2) - (450/2)), int((self.hs/2) - (250/2) - 150)))
        self.poproot.title(name)
        self.validateButton = tk.Button(self.poproot, text="Valider", state="disabled", background="#fff", font=("Arial", 14), highlightthickness = 0, bd = 0, bg="#fff", command=lambda: self.popUpValidate())
        self.validateButton.place(anchor="se", x=sizex-30, y=sizey-30)
        self.cancelButton = tk.Button(self.poproot, text="Annuler", background="#fff", font=("Arial", 14), highlightthickness = 0, bd = 0, bg="#fff", command=lambda: self.popUpCancel())
        self.cancelButton.place(anchor="sw", x=30, y=sizey-30)
        self.poproot.update()
        self.canceled = False

    def popUpCancel(self):
        self.poproot.destroy()
        self.canceled = True

    def popUpValidate(self):
        self.validated = True
        self.popUpCancel()
