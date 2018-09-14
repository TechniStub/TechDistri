import tkinter as tk

class VirtualKeyboard():
    def __init__(self, name="Keyboard"):
        self.touched = False
        self.touch=""
        self.name = name
        self.valid = False
        self.quit = False
        self.complete = ""
        self.lastIndex = 0
        self.maj = False

    def callback(self, touch):
        self.touch = touch
        self.touched = True
        if(touch == "<-"):
            try:
                self.complete = self.complete[:self.lastIndex-1]
                self.lastIndex-=1
            except:
                pass
        elif(touch == "Maj"):
            self.maj = not self.maj
            if(self.maj):
                self.buttons["maj"]["bg"] = "#eaeaea"
                for y in range(3):
                    for x in range(self.size[y]):
                        key = self.keys[y][x]
                        self.buttons[key]["text"] = self.buttons[key]["text"].upper()
            else:
                self.buttons["maj"]["bg"] = "#fff"
                for y in range(3):
                    for x in range(self.size[y]):
                        key = self.keys[y][x]
                        self.buttons[key]["text"] = self.buttons[key]["text"].lower()
            self.frame.update()

        else:
            self.lastIndex += 1
            if(self.maj):
                self.complete += touch.upper()
            else:
                self.complete += touch
    def set(self):
        self.frame = tk.Tk()
        self.frame.configure(background="white")
        self.frame.geometry("450x150")
        self.frame.config(cursor="crosshair")
        self.frame.title(self.name)
        self.height = self.frame.winfo_screenheight()
        self.width = self.frame.winfo_screenwidth()
        self.size = [10, 10, 6]
        # -a--z--e--r--t--y--u--i--o--p-    10
        #  -q--s--d--f--g--h--j--k--l--m-   10
        #   -w--x--c--v--b--n-      <--     06

        self.keys = [["a", "z", "e", "r", "t", "y", "u", "i", "o", "p"], ["q", "s", "d", "f", "g", "h", "j", "k", "l", "m"], ["w", "x", "c", "v", "b", "n"]]
        self.buttons = {}

        for y in range(3):
            for x in range(self.size[y]):
                key = self.keys[y][x]
                self.buttons[key] = tk.Button(self.frame, command=lambda k=key: self.callback(k), text=key, highlightthickness = 0, bd = 0, bg="#fff")
                self.buttons[key].place(anchor="center", x=(x*40+(13*y))+30, y=(y*30+30))

        self.buttons["<-"] = tk.Button(self.frame, command=lambda k="<-": self.callback(k), text="<---", highlightthickness = 0, bd = 0, bg="#fff")
        self.buttons["<-"].place(anchor="center", x=(7*40+(13*2))+30, y=(2*30+30))

        self.buttons["maj"] = tk.Button(self.frame, command=lambda k="Maj": self.callback(k), text="Maj", highlightthickness = 0, bd = 0, bg="#fff")
        self.buttons["maj"].place(anchor="center", x=(9*40+(13*2))+30, y=(2*30+30))

        self.buttons[" "] = tk.Button(self.frame, command=lambda k=" ": self.callback(k), text="     Espace     ", highlightthickness = 0, bd = 0, bg="#fff")
        self.buttons[" "].place(anchor="center", x=450/2, y=(3*30+30))

        self.qButton = tk.Button(self.frame, command=self.clr, text="Annuler", highlightthickness = 0, bd = 0, bg="#cecece")
        self.qButton.place(anchor="sw", x=10, y=150-10)

        self.vButton = tk.Button(self.frame, command=self.validate, text="Valider", highlightthickness = 0, bd = 0, bg="#cecece")
        self.vButton.place(anchor="se", x=450-10, y=150-10)

        self.frame.update()

    def clr(self):
        self.quit = True
        try:
            self.frame.desroy()
        except:
            pass

    def validate(self):
        self.valid = True
        self.clr()

if __name__ == "__main__":
    ist = VirtualKeyboard()
    ist.set()
    while True:
        if(ist.touched):
            print(ist.touch)
            ist.touched = False
        else:
            ist.frame.update()
        if(ist.quit):
            break

    if(ist.valid):
        print(ist.complete)
