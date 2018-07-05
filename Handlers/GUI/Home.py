import tkinter as tk

class HomeHandler():
    def __init__(self, root, ts, rfidInstance):
        self.root = root
        self.ts = ts
        self.rfidInst = rfidInstance


    def bypass(self, event=None):
        self.rfidInst.readed = True
        self.rfidInst.lastId = 550785624180  # ADMIN BADGE
        print("[INFO] Bypassed")

    def set(self):
        self.height = self.root.winfo_screenheight()
        self.width = self.root.winfo_screenwidth()
        self.l = tk.Label(self.root, text="Badgez pour continuer", font=("arial", 22), fg="#fd3303", anchor='center', background="white")
        self.l.place(anchor="center")
        self.l.pack(pady=(self.height/2.9))

        self.i = tk.Label(self.root, image=self.ts, background="white")
        self.i.place(anchor="nw", x=0, y=0)
        #self.i.pack(side="left")
        self.root.bind("<space>", self.bypass)

    def clr(self):
        self.l.destroy()
        self.i.destroy()
