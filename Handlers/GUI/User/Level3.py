#
#    USER - LEVEL3
#

import tkinter as tk

class UserHandler():
    def __init__(self, root, ts, scrollTop, scrollBottom):
        self.root = root
        self.ts = ts
        self.scrollTop = scrollTop
        self.scrollBottom = scrollBottom

    def scrollHandler(self, type):
        if type == 1: # bottom
            if self.page+10 >= len(self.transac):
                pass
            else:
                self.page += 1
        else:
            if self.page <= 0:
                pass
            else:
                self.page -= 1

        self.shownTransac = self.transac[self.page:self.page+10]
        for index in range(10):
            self.labels[index][0]["text"] = self.shownTransac[index]["info"]
            self.labels[index][1]["text"] = str(self.shownTransac[index]["date"])[:10]
            self.labels[index][2]["text"] = self.shownTransac[index]["value"]

        self.lPage["text"] = "Page : {}-{}/{}".format(self.page, self.page+10, len(self.transac))

        self.root.update()


    def set(self, transac):
        self.transac = transac
        self.height = self.root.winfo_screenheight()
        self.width = self.root.winfo_screenwidth()
        self.page = 0
        self.total = 0

        self.lhisto = tk.Label(self.root, text="Historique des Transactions", font=("Arial", 18), anchor='center', background="white")
        self.lhisto.place(anchor="center", x=int(self.width/2), y=150)

        if(len(self.transac) >= 10):
            self.tButton = tk.Button(self.root, image=self.scrollTop, highlightthickness = 0, bd = 0, bg="#fff", command=lambda: self.scrollHandler(2))
            self.tButton.place(anchor="center", y=int(self.height/3), x=self.width-35)

            self.bButton = tk.Button(self.root, image=self.scrollBottom, highlightthickness = 0, bd = 0, bg="#fff", command=lambda: self.scrollHandler(1))
            self.bButton.place(anchor="center", y=int(self.height*(2/3.0)), x=self.width-35)

            self.shownTransac = self.transac[self.page:self.page+10]
            self.labels = []
            for index in range(10):
                self.labels.append([])
                for indexY in range(3):
                    self.labels[index].append(tk.Label(self.root, font=("arial", 14), bg="#fff"))
                self.labels[index][0].place(anchor="nw", x=30, y=(index*40)+200) ; self.labels[index][0]["text"] = self.shownTransac[index]["info"]
                self.labels[index][1].place(anchor="nw", x=200, y=(index*40)+200); self.labels[index][1]["text"] = str(self.shownTransac[index]["date"])[:10]
                self.labels[index][2].place(anchor="nw", x=350, y=(index*40)+200); self.labels[index][2]["text"] = self.shownTransac[index]["value"]
            for index in range(len(self.transac)):
                self.total += float(self.transac[index]["value"])

            self.lPage = tk.Label(self.root, font=("arial", 15), bg="#fff")
            self.lPage.place(anchor="se", x=self.width-75, y=self.height-180) ; self.lPage["text"] = "Page : {}-{}/{}".format(self.page, self.page+10, len(self.transac))
            self.root.update()
        else:
            self.shownTransac = self.transac
            self.labels = []
            for index in range(len(self.transac)):
                self.labels.append([])
                for indexY in range(3):
                    self.labels[index].append(tk.Label(self.root, font=("arial", 14), bg="#fff"))
                self.labels[index][0].place(anchor="nw", x=30, y=(index*40)+200) ; self.labels[index][0]["text"] = self.shownTransac[index]["info"]
                self.labels[index][1].place(anchor="nw", x=200, y=(index*40)+200); self.labels[index][1]["text"] = str(self.shownTransac[index]["date"])[:10]
                self.labels[index][2].place(anchor="nw", x=350, y=(index*40)+200); self.labels[index][2]["text"] = self.shownTransac[index]["value"]
                self.total += float(self.transac[index]["value"])

        self.lhisto = tk.Label(self.root, text="Reste a payer :   "+str(self.total), font=("Arial", 18), anchor='center', background="white")
        self.lhisto.place(anchor="se", x=self.width-75, y=self.height-150)
