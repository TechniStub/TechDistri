import tkinter as tk

class AdminHandler():
    def __init__(self, root, image, home, rfid, database, queries, keyboard, image1, commonFunc, scrollLeft, scrollRight, session, userEdit, userPlus, userMoins, stockVoir, stockModify, produitsModify, produitsSee, produitsAddDel):
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
        self.session = session
        self.pageChanging = False
        self.userEdit = userEdit
        self.userPlus = userPlus
        self.userMoins = userMoins
        self.stockVoir = stockVoir
        self.stockModify = stockModify
        self.productsModify = produitsModify
        self.productsSee = produitsSee
        self.productsAddDel = produitsAddDel

    def changeEdit(self, val):
        self.edit = val

    def continuing(self, _is):
        print(_is)
        self.continueVAR = _is

    def choiceHandler(self, frameId, buttonId):
        if frameId == 1: # badges
            if buttonId == 1: # new
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
                        if user is None or user == []:
                            pass
                        else:
                            for (_Id) in user:
                                id = _Id
                                nUser += 1


                        if(nUser == 0):
                            success = False
                            if True:
                                self.db.edit(self.queries["createUser"].format(self.nom, self.pnom))
                                self.db.edit(self.queries["createUserPart2"].format(self.nom, self.pnom))
                                self.db.edit(self.queries["associateBadge"].format(str(newId), self.nom, self.pnom))
                                success = True
                            else:
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
            elif buttonId == 2: # delete
                print("Badges - Delete")
                self.commonInst.newPopup("Supprimer un badge", sizey=150)
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
                if(nUser == 1):
                    self.continueVAR = False
                    self.lResult = tk.Label(self.poproot, text="UUID : {}".format(id), font=("arial", 14), bg="#fff")
                    self.lResult.place(anchor="nw", x=30, y=60)
                    self.trashBinButton = tk.Button(self.poproot, text="Supprimer", command=lambda: self.continuing(True), height=1, width=7, font=("Arial", 14), bd=0, highlightthickness = 0, bg="#fd3303", activebackground="#000000", fg="#ffffff", activeforeground="#ffffff", pady=2)
                    self.trashBinButton.place(anchor="s", x=450/2, y=150-30)
                    self.poproot.update()
                    while not self.continueVAR:
                        self.poproot.update()
                    sureDelete = self.commonInst.areSure("Supprimer {}".format(id))
                    self.poproot.destroy()
                    success = False
                    try:
                        self.db.edit(self.queries["deleteUserPart1"].format(id))
                        self.db.edit(self.queries["deleteUserPart2"].format(id))
                        self.db.edit(self.queries["deleteUserPart3"].format(id))
                        self.db.edit(self.queries["deleteUserPart4"].format(id))
                        success = True
                    except:
                        success = False

                    if(success):
                        text="L'utilisateur {} avec le badge {} a été supprimé".format(id, newId)
                    else:
                        text="Erreur : L'utilisateur {} avec le badge {} n'a pas pu etre suprimé".format(id, newId)
                    self.commonInst.info(text, sizex=len(text)*5, line=3, sizey=150)
            elif buttonId == 3:
                print("Badges - Add / Del Grade")
                self.commonInst.newPopup("Grader un badge", sizey=150)
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
                if(nUser == 1):
                    self.edit=0
                    self.lGrade = tk.Label(self.poproot, text="Grade : "+str(self.session["gradeInText"]), bg="#fff", font=("arial", 14))
                    self.lGrade.place(anchor="nw", x=30, y=60)

                    self.bToBeUser = tk.Button(self.poproot, text="Utilisateur", bg="#fff", command=lambda: self.changeEdit(1), highlightthickness=0, bd=0, font=("arial", 14))
                    self.bToBeUser.place(anchor="nw", x=165, y=58)

                    self.bToBeAdmin = tk.Button(self.poproot, text="Administrateur", bg="#fff", command=lambda: self.changeEdit(2), highlightthickness=0, bd=0, font=("arial", 14))
                    self.bToBeAdmin.place(anchor="nw", x=290, y=58)

                    while not self.commonInst.canceled:
                        if self.edit != 0:
                            if self.edit == 2:
                                self.lGrade["text"] = "Grade : admin"
                                gradeId = 0
                            else:
                                self.lGrade["text"] = "Grade : user"
                                gradeId = 1
                            self.edit = 0
                            self.commonInst.validateButton["state"] = "normal"
                        else:
                            self.poproot.update()

                    if self.commonInst.validated:
                        sure = self.commonInst.areSure("Grader ?")
                        if sure == 1:
                            self.db.edit(self.queries["updateGrade"].format(gradeId, id))
                        else:
                            pass
        elif frameId == 3: # stock
            if buttonId == 1: # see
                print("Stock - See")
            elif buttonId == 2: # edit
                print("Stock - Edit")
        elif frameId == 4: # products
            if buttonId == 1: # see
                print("Products - See")
            elif buttonId == 2: # edit
                print("Products - Edit")
            elif buttonId == 3: # add / del
                print("Products - Add/Del")

    def changePage(self):
        self.pageChanging = True

    def set(self, session):
        self.session = session
        self.height = self.root.winfo_screenheight()
        self.width = self.root.winfo_screenwidth()

        generalDecalage = -45

        self.dashboardL = tk.Label(self.root, text="Dashboard", font=("arial", 24), fg="#ff3500", bg="#fff")
        self.dashboardL.place(anchor="center", x=self.width/2, y=self.height/4-45)

        ###      Badges menu     ###
        self.lBadges = tk.Label(self.root, text="Badges"+(50*" "), font=("arial", 16), bg="#00b3f1", fg="#fff", padx=10, pady=5)
        self.lBadges.place(anchor="nw", x=25, y=self.height/4+45+generalDecalage)

        #self.newBadgeButton = tk.Button(self.root, command=lambda: self.choiceHandler(1, 1), image=self.userEdit, height=1, width=6, bd=0, highlightthickness = 0, activebackground="#000")
        self.newBadgeButton = tk.Button(self.root, image=self.userPlus, highlightthickness = 0, bd = 0, bg="#fff", command=lambda: self.choiceHandler(1, 1))
        self.newBadgeButton.place(anchor="center", y=315+generalDecalage, x=75)
        self.newBadgeLabel = tk.Label(self.root, text="Nouveau", font=("arial", 16), bg="#fff")
        self.newBadgeLabel.place(anchor="center", y=353+generalDecalage, x=75)

        #self.delBadgeButton = tk.Button(self.root, command=lambda: self.choiceHandler(1, 2), text="Supprimer", height=1, width=8, font=("Arial", 14), bd=0, highlightthickness = 0, bg="#fd3303", activebackground="#000", fg="#fff", activeforeground="#fff", pady=2)
        self.delBadgeButton = tk.Button(self.root, image=self.userMoins, highlightthickness = 0, bd = 0, bg="#fff", command=lambda: self.choiceHandler(1, 2))
        self.delBadgeButton.place(anchor="center", y=315+generalDecalage, x=225)
        self.delBadgeLabel = tk.Label(self.root, text="Supprimer", font=("arial", 16), bg="#fff")
        self.delBadgeLabel.place(anchor="center", y=353+generalDecalage, x=225)

        #self.delBadgeButton = tk.Button(self.root, command=lambda: self.choiceHandler(1, 3), text="Grader", height=1, width=8, font=("Arial", 14), bd=0, highlightthickness = 0, bg="#fd3303", activebackground="#000", fg="#fff", activeforeground="#fff", pady=2)
        self.editBadgeButton = tk.Button(self.root, image=self.userEdit, highlightthickness = 0, bd = 0, bg="#fff", command=lambda: self.choiceHandler(1, 3))
        self.editBadgeButton.place(anchor="center", y=315+generalDecalage, x=380)
        self.editBadgeLabel = tk.Label(self.root, text="Modifier", font=("arial", 16), bg="#fff")
        self.editBadgeLabel.place(anchor="center", y=353+generalDecalage, x=380)

        ###     Stock menu     ###
        self.lStock = tk.Label(self.root, text="Stock"+(53*" "), font=("arial", 16), bg="#00b3f1", fg="#fff", padx=10, pady=5)
        self.lStock.place(anchor="nw", x=25, y=406+generalDecalage)

        self.seeStockButton = tk.Button(self.root, image=self.stockVoir, highlightthickness = 0, bd = 0, bg="#fff", command=lambda: self.choiceHandler(3, 1))
        self.seeStockButton.place(anchor="center", y=485+generalDecalage, x=75)
        self.delBadgeLabel = tk.Label(self.root, text="Voir", font=("arial", 16), bg="#fff", fg="#000")
        self.delBadgeLabel.place(anchor="center", y=520+generalDecalage, x=75)

        self.editStockButton = tk.Button(self.root, image=self.stockModify, highlightthickness = 0, bd = 0, bg="#fff", command=lambda: self.choiceHandler(3, 2))
        self.editStockButton.place(anchor="center", y=485+generalDecalage, x=225)
        self.delBadgeLabel = tk.Label(self.root, text="Modifier", font=("arial", 16), bg="#fff", fg="#000")
        self.delBadgeLabel.place(anchor="center", y=520+generalDecalage, x=225)

        ###      Product menu     ###
        self.lProduct = tk.Label(self.root, text="Products"+(48*" "), font=("arial", 16), bg="#00b3f1", fg="#fff", padx=10, pady=5)
        self.lProduct.place(anchor="nw", x=25, y=570+generalDecalage)

        self.seeProductsButton = tk.Button(self.root, image=self.productsSee, highlightthickness = 0, bd = 0, bg="#fff", command=lambda: self.choiceHandler(4, 1))
        self.seeProductsButton.place(anchor="center", y=645+generalDecalage, x=75)
        self.delBadgeLabel = tk.Label(self.root, text="Voir", font=("arial", 16), bg="#fff", fg="#000")
        self.delBadgeLabel.place(anchor="center", y=680+generalDecalage, x=75)

        self.modifyProductsButton = tk.Button(self.root, image=self.productsModify, highlightthickness = 0, bd = 0, bg="#fff", command=lambda: self.choiceHandler(4, 2))
        self.modifyProductsButton.place(anchor="center", y=645+generalDecalage, x=225)
        self.delBadgeLabel = tk.Label(self.root, text="Modifier", font=("arial", 16), bg="#fff", fg="#000")
        self.delBadgeLabel.place(anchor="center", y=680+generalDecalage, x=225)

        self.adddelProductsButton = tk.Button(self.root, image=self.productsAddDel, highlightthickness = 0, bd = 0, bg="#fff", command=lambda: self.choiceHandler(4, 3))
        self.adddelProductsButton.place(anchor="center", y=645+generalDecalage, x=380)
        self.delBadgeLabel = tk.Label(self.root, text="Ajout / Suppr", font=("arial", 16), bg="#fff", fg="#000")
        self.delBadgeLabel.place(anchor="center", y=680+generalDecalage, x=380)

        # Change Admin Page
        if(self.session["sAdmin"]):
            self.changePageButton = tk.Button(self.root, image=self.scrollRight, highlightthickness = 0, bd = 0, bg="#fff", command=lambda: self.changePage())
            self.changePageButton.place(anchor="center", y=700, x=350)
            self.pageLabel = tk.Label(self.root, text="1/2", font=("arial", 16), bg="#fff")
            self.pageLabel.place(anchor="center", y=700, x=240)
