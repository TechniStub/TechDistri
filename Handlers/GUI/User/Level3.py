import tkinter as tk

class UserHandler():
    def __init__(self, root, ts):
        self.root = root
        self.ts = ts

    def set(self, transac):
        self.transac = transac
        self.height = self.root.winfo_screenheight()
        self.width = self.root.winfo_screenwidth()
        self.page = 0

        self.lhisto = tk.Label(self.root, text="Historique des Transactions", font=("Arial", 18), anchor='center', background="white")
        self.lhisto.place(anchor="center", x=int(self.width/2), y=150)

        if(len(self.transac) >= 10):
            self.shownTransac = self.transac[page:page+10]
            self.labels = []
            for index in range(10):
                self.labels.append([])
                for indexY in range(3):
                    self.labels[index].append(tk.Label(self.root, font=("arial", 14), bg="#fff"))
                self.labels[index][0].place(anchor="nw", x=(index*50), y=30) ; self.labels[index][0]["text"] = self.shownTransac[index]["info"]
                self.labels[index][1].place(anchor="nw", x=(index*50), y=200); self.labels[index][1]["text"] = self.shownTransac[index]["date"]
                self.labels[index][2].place(anchor="nw", x=(index*50), y=300); self.labels[index][2]["text"] = self.shownTransac[index]["value"]
        else:
            self.shownTransac = self.transac
            self.labels = []
            for index in range(len(self.transac)):
                self.labels.append([])
                for indexY in range(3):
                    self.labels[index].append(tk.Label(self.root, font=("arial", 14), bg="#fff"))
                self.labels[index][0].place(anchor="nw", x=30, y=(index*40)+200) ; self.labels[index][0]["text"] = self.shownTransac[index]["info"]
                self.labels[index][1].place(anchor="nw", x=200, y=(index*40)+200); self.labels[index][1]["text"] = self.shownTransac[index]["date"]
                self.labels[index][2].place(anchor="nw", x=350, y=(index*40)+200); self.labels[index][2]["text"] = self.shownTransac[index]["value"]
