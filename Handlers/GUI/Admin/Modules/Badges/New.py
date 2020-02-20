print("Badges - New")
self.nom = ""
self.pnom= ""
self.commonInst.validated = False
self.commonInst.canceled = False
self.commonInst.newPopup("Nouveau badge", sizey=150)
self.poproot = self.commonInst.poproot
self.lWaiting=tk.Label(self.poproot, text="En attente d'un badge ...", font=("arial", 16), bg="#fff")
self.lWaiting.place(anchor="center", x=450/2, y=30)
while True:
    if self.rfid.readed and self.rfid.lastId != None:
        break
    else:
        self.poproot.update()

newId = self.rfid.lastId
self.rfid.readed=False

## TO DO : TEST IF USER EXIST
uuid = self.db.getQuery(self.queries["badgeToUuid"].format(newId))
nUser = 0
for (_Id, _Data) in uuid:
    id = _Id
    nUser += 1

self.lWaiting["text"] = "Badge : "+str(newId)
self.lResult = tk.Label(self.poproot, font=("arial", 14), bg="#fff")
self.lResult.place(anchor="nw", x=30, y=60)
self.poproot = self.commonInst.poproot
if nUser == 0:
    self.lResult["text"] = "Badge non utilisé"
    self.poproot.geometry("450x250+{}+{}".format(int((self.commonInst.ws/2) - (450/2)), int((self.commonInst.hs/2) - (250/2) - 150)))
    self.commonInst.validateButton.place(anchor="se", x=450-30, y=250-30)
    self.commonInst.cancelButton.place(anchor="sw", x=30, y=250-30)

    self.edit = 0 #0:nothing, 1:nom, 2:pnom
    #nom
    self.lNomDisp = tk.Label(self.poproot, text="Nom : ", font=("arial", 14), bg="#fff")
    self.lNomDisp.place(anchor="nw", x=30, y=90)
    self.lNomReal = tk.Label(self.poproot, text="", font=("arial", 14), bg="#fff")
    self.lNomReal.place(anchor="nw", x=85, y=90)
    self.bNomEdit = tk.Button(self.poproot, text="Editer", command=lambda x=1: self.changeEdit(x), height=1, width=6, font=("Arial", 14), bd=0, highlightthickness = 0, bg="#fd3303", activebackground="#000", fg="#fff", activeforeground="#fff", pady=2)
    self.bNomEdit.place(anchor="ne", x=450-30, y=90)

    #p nom
    self.lPnomDisp = tk.Label(self.poproot, text="Prénom : ", font=("arial", 14), bg="#fff")
    self.lPnomDisp.place(anchor="nw", x=30, y=120)
    self.lPnomReal = tk.Label(self.poproot, text="", font=("arial", 14), bg="#fff")
    self.lPnomReal.place(anchor="nw", x=115, y=120)
    self.bPnomEdit = tk.Button(self.poproot, text="Editer", command=lambda x=2: self.changeEdit(x), height=1, width=6, font=("Arial", 14), bd=0, highlightthickness = 0, bg="#fd3303", activebackground="#000", fg="#fff", activeforeground="#fff", pady=2)
    self.bPnomEdit.place(anchor="ne", x=450-30, y=120)

    while not(self.commonInst.canceled):
        if(self.edit == 1):
            self.keyboard.set()
            self.keyboard.qButton['state'] = "disabled"
            while not(self.keyboard.quit):
                self.lNomReal["text"] = self.keyboard.complete
                self.nom = self.keyboard.complete
                self.keyboard.frame.update()
            print("ENDED WHILE")
            self.edit=0
        elif(self.edit == 2):
            self.keyboard.set()
            self.keyboard.qButton['state'] = "disabled"
            while True:
                self.lPnomReal["text"] = self.keyboard.complete
                self.pnom = self.keyboard.complete
                self.keyboard.frame.update()
                if self.keyboard.quit:
                    break
            self.edit=0
        elif(self.keyboard.quit):
            print("QUITED")
            self.keyboard.frame.destroy()
            self.keyboard.quit = False
            self.keyboard.valid = False
            self.edit = 0
            self.keyboard.complete = ""
            self.keyboard.lastIndex = 0
            if self.lNomReal["text"] != "" and self.lPnomReal["text"] != "":
                self.commonInst.validateButton["state"]="normal"
        else:
            try:
                self.poproot.update()
            except:
                pass

    if(self.commonInst.validated):
        user = self.db.getQuery(self.queries["getUserFromName"].format(self.nom, self.pnom))
        nUser = 0
        for (_Id, _Data) in user:
            id = _Id
            nUser += 1

        if(nUser == 0):
            success = False
            try:
                self.db.edit(self.queries["createUser"].format(self.nom, self.pnom))
                self.db.edit(self.queries["createUserPart2"].format(self.nom, self.pnom))
                self.db.edit(self.queries["associateBadge"].format(str(newId), self.nom, self.pnom))
                success = True
            except:
                success = False

            if(success):
                text="L'utilisateur {} {} avec le badge {} a été crée".format(self.pnom, self.nom, newId)
            else:
                text="Erreur : L'utilisateur {} {} avec le badge {} n'a pas pu etre crée".format(self.pnom, self.nom, newId)
            self.commonInst.info(text, sizex=len(text)*5, line=3, sizey=150)
        else:
            self.commonInst.info("L'utilisateur {} {} éxiste déja.".format(self.pnom, self.nom), sizex=250, line=2, sizey=120)
else:
    self.lResult["text"] = "Badge déja utilisé"
try:
    self.poproot.update()
except:
    pass
