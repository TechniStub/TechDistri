#
#    USER - LEVEL4 - Ajouter Crédit
#

import tkinter as tk
from PIL import ImageTk, Image
import json
from time import sleep

class UserHandler():
    def __init__(self, root, rfid, db, queries, commonGUI, supervisor, handlers):
        self.root = root
        self.rfid = rfid
        self.db = db
        self.queries = queries
        self.commonInst = commonGUI
        self.user = {}
        self.KeyboardReturn = [0, 0, 0, 0]
        self.KeyboardQty = 0
        self.finished = False
        self.supervisor = supervisor
        self.handlers = handlers

    def rfidGet(self):
        self.supervisor.data["iswWaiting"] = True
        self.commonInst.newPopup("En attente d'un Admin ...", sizey=150)
        self.poproot = self.commonInst.poproot
        self.lWaiting=tk.Label(self.poproot, text="En attente d'un badge ...", font=("arial", 16), bg="#fff")
        self.lWaiting.place(anchor="center", x=450/2, y=30)

        while (not self.supervisor.bypass) and (not self.commonInst.canceled):
            if self.rfid.readed and self.rfid.lastId != None:
                break
            else:
                self.root.update()
                self.poproot.update()

        newId = self.rfid.lastId
        self.rfid.readed=False

        self.poproot.destroy()

        self.supervisor.data["iswWaiting"] = True

        ## TO DO : TEST IF USER EXIST
        uuid = self.db.getQuery(self.queries["badgeToUuid"].format(newId))
        nUser = 0
        for (_Id, _Data) in uuid:
            id = _Id
            nUser += 1

        if nUser == 1:
            _userRaw = self.db.getQuery(self.queries["getUserInfo"].format(newId))
            for (Data, Id, Nom, PNom, Grade, Value, GradeCustom) in _userRaw:
                self.user["id"] = Id
                self.user["uuid"] = Data
                self.user["Nom"] = Nom
                self.user["PNom"] = PNom
                self.user["Grade"] = Grade
                self.user["GradeCustom"] = GradeCustom

            if self.user["Grade"] == 0 or self.user["Grade"] == -1:
                pass
            else:
                self.user = {} # Non admin : remise à zero
        else:
            print("[ERROR] No user found with uuid {}".format(newId))

    def connect(self, _user=None): # _user : FORCE USER - DEBUG ONLY
        if _user is None:
            self.rfidGet()
        else:
            print("User is not None")
            self.user = {"id": 1, "uuid": "550785624180", "Nom": "SAHLER", "PNom": "Vincent", "Grade": (0-1), "GradeCustom": "The Admin"}

        if self.user != {}:
            print(self.user)
            self.AdminInfo["text"] = "{} {}".format(self.user["Nom"], self.user["PNom"])
            self.connectAdmin["text"] = "Connecté"

    def numericalKeyboardEventHadler(self, val):
        if val == "<-":
            self.KeyboardQty -= 1
            self.KeyboardReturn[3] = self.KeyboardReturn[2]
            self.KeyboardReturn[2] = self.KeyboardReturn[1]
            self.KeyboardReturn[1] = self.KeyboardReturn[0]
            self.KeyboardReturn[0] = 0
        else:
            self.KeyboardReturn[0] = self.KeyboardReturn[1]
            self.KeyboardReturn[1] = self.KeyboardReturn[2]
            self.KeyboardReturn[2] = self.KeyboardReturn[3]
            self.KeyboardReturn[3] = str(val)
            if self.KeyboardQty == 4:
                self.KeyboardQty = 4
            else:
                self.KeyboardQty += 1

        print(self.KeyboardReturn)
        self.soldeAjout["text"] = "  {} {} {} . {}  ".format(self.KeyboardReturn[0], self.KeyboardReturn[1], self.KeyboardReturn[2], self.KeyboardReturn[3])

    def numericalKeyboard(self):
        self.button = [[None, None, None], [None, None, None], [None, None, None]]
        for x in range(3):
            for y in range(3):
                self.button[x][y] = tk.Button(self.root, font=("arial", 14), text=str(y*3+x+1), command=lambda k=(y*3+x+1): self.numericalKeyboardEventHadler(k), highlightthickness = 0, bd = 0, bg="#fff")
                self.button[x][y].place(anchor="center", x=(x*50+75), y=(y*50+self.height/2))

        self.button.append(tk.Button(self.root, font=("arial", 14), text="    0    ", command=lambda k=0: self.numericalKeyboardEventHadler(k), highlightthickness = 0, bd = 0, bg="#fff"))
        self.button[3].place(anchor="center", x=(0.5*50+75), y=(3*50+self.height/2))

        self.button.append(tk.Button(self.root, font=("arial", 14), text="<-", command=lambda k="<-": self.numericalKeyboardEventHadler(k), highlightthickness = 0, bd = 0, bg="#fff"))
        self.button[4].place(anchor="center", x=(2*50+75), y=(3*50+self.height/2))

    def validate(self, paypal=1):
        #self._user = self.user
        #self.rfidGet()

        print(type(self.handlers))

        value = int(self.KeyboardReturn[0])*100+int(self.KeyboardReturn[1])*10+int(self.KeyboardReturn[2])*1+int(self.KeyboardReturn[3])*0.1
        proceed = self.commonInst.areSure("Proceder à la transaction de {}€".format(value), x_size=350)

        if proceed:
            if paypal:
                for widget in self.widgets:
                    widget.destroy()
                for button in self.button:
                    if type(button) == list:
                        for _button in button:
                            _button.destroy()
                    else:
                        button.destroy()

                res, payment = self.handlers["paypal"].createPayment(value)

                print(res, " ", str(float(value)))
                print(payment.error)

                self.handlers["supervisor"].Print("[PayPal] Started Payment procedure for {}EUR".format(value))

                self.handlers["paypal"].getURL()  # "create" paypal payment url

                qrCode = self.handlers["paypal"].getQR()
                qrCode = ImageTk.PhotoImage(qrCode.resize((400, 400), Image.ANTIALIAS))
                qrCodeLabel = tk.Label(self.root, image=qrCode)
                qrCodeLabel.place(anchor="center", x=int(self.width / 2), y=int(self.height / 2)+75)

                waitLabel = tk.Label(self.root, text="En Attente d'une connection ...", font=("arial", 18), bg="#fff")
                waitLabel.place(anchor="center", x=int(self.width / 2), y=150)

                data = {}

                while True and not self.handlers["supervisor"].bypass:
                    self.root.update()
                    try:
                        with open('/home/pi/TechDistri/Handlers/PayPal/db.json') as json_file:
                            data = json.load(json_file)
                            if self.handlers["paypal"].id in data:
                                self.handlers["supervisor"].Print("[PayPal] Transaction of {}EUR validated".format(value))
                                self.handlers["supervisor"].blocked = True
                                break
                            else:
                                print("Waiting ", end="")
                                sleep(0.4)
                                for x in range(3):
                                    print(".", end="")
                                    sleep(0.4)
                                print()
                    except:
                        print("Something went wrong")

                qrCodeLabel.destroy()
                waitLabel["text"] = "Validation en cours ... "

                self.root.update()

                if self.handlers["paypal"].acceptPayment(data[self.handlers["paypal"].id]["PayerID"]):  # return True or False
                    self.handlers["supervisor"].Print("[PayPal] Payment[%s] execute successfully" % payment.id)
                    waitLabel["text"] = "En attente de PayPal ..."

                    self.root.update()

                    while True and not self.handlers["supervisor"].bypass:
                        self.root.update()
                        tr = self.handlers["paypal"].getTransactionState()

                        if tr[0] == "approved":
                            self.handlers["supervisor"].Print(str(tr[1].payer))
                            self.handlers["supervisor"].Print("[PayPal] Payment approved by " + str(tr[1].payer.payer_info.email) +", aka "+ str(tr[1].payer.payer_info.first_name) + " " + str(tr[1].payer.payer_info.last_name))
                            break

                    if not self.handlers["supervisor"].bypass:
                        waitLabel["text"] = "Validé, Merci :) "
                        print("************* VALIDATED *************")
                        self.db.edit(self.queries["addCredits"].format(value, self.session["uuid"]))
                        self.db.edit(self.queries["transacFromServer"].format(self.session["uuid"], value, "Input"))

                    self.root.update()
                else:
                    self.handlers["supervisor"].Print("[PayPal]" + str(payment.error))
                    waitLabel["text"] = "Une erreur est survenue ...\nContactez un admin"
                    self.root.update()
                self.handlers["supervisor"].blocked = False
            else:
                print(self.user)
                if len(self.user) == 0:
                    self.connect()
                else:
                    if self.user["Grade"] <= 0: # is admin
                        self.db.edit(self.queries["addCredits"].format(value, self.session["uuid"]))
                        self.db.edit(self.queries["transacFromServer"].format(self.session["uuid"], value, "Input"))
                self.cancel(validated=True)
        else:
            pass

    def cancel(self, validated=False):
        if validated:
            self.finished = True
        else:
            proceed = self.commonInst.areSure("Annuler la transaction")
            if proceed:
                self.finished = True
            else:
                pass

    def clearVar(self):
        self.user = {}
        self.KeyboardReturn = [0, 0, 0, 0]
        self.KeyboardQty = 0
        self.finished = False
        self.handlers["paypal"].id = None
        self.handlers["paypal"].url = None
        self.handlers["paypal"].payment = None

    def set(self, session):
        self.clearVar()
        self.height = self.root.winfo_screenheight()
        self.width = self.root.winfo_screenwidth()
        self.paypalButton = tk.Button(self.root, text="PayPal", height=1, width=20, command=lambda s=session, ppl=1: self.setCommon(s, paypal=ppl),
                                     font=("Arial", 18), bd=0, highlightthickness=0, bg="#fd3303",
                                     activebackground="#000000", fg="#ffffff", activeforeground="#ffffff", pady=10)
        self.paypalButton.place(anchor="center", x=int(self.width / 2), y=int(self.height / 3) + 0)

        self.monnaieButton = tk.Button(self.root, text="Monnaie", height=1, width=20, command=lambda s=session, ppl=0: self.setCommon(s, paypal=ppl),
                                     font=("Arial", 18), bd=0, highlightthickness=0, bg="#fd3303",
                                     activebackground="#000000", fg="#ffffff", activeforeground="#ffffff", pady=10)
        self.monnaieButton.place(anchor="center", x=int(self.width / 2), y=int(self.height / 3) + 75)

    def setCommon(self, session, paypal=1):
        self.widgets = []

        self.finished = False
        self.session = session

        self.paypalButton.destroy()
        self.monnaieButton.destroy()

        self.soldeAjout = tk.Label(self.root, text="Ajout via PayPal" if paypal else "Ajout via Monnaie", font=("Arial", 18), bg="#fff")
        self.soldeAjout.place(anchor="center", x=int(self.width / 2), y=int(self.height / 4))
        self.widgets.append(self.soldeAjout)

        if not paypal:
            self.connectAdmin = tk.Button(self.root, text="Connection Requise", height=1, width=20, command=self.connect,
                                          font=("Arial", 18), bd=0, highlightthickness=0, bg="#fd3303",
                                          activebackground="#000000", fg="#ffffff", activeforeground="#ffffff", pady=10)

            self.connectAdmin.place(anchor="center", x=int(self.width / 2), y=int(self.height / 3))
            self.widgets.append(self.connectAdmin)

            self.AdminInfo = tk.Label(self.root, text="", font=("arial", 14), bg="#fff")
            self.AdminInfo.place(anchor="center", x=int(self.width / 2), y=int(self.height / 3) + 50)
            self.widgets.append(self.connectAdmin)

        self.soldeAjout = tk.Label(self.root, text="  0 0 0 . 0  ", font=("Arial", 18), bg="#e2e2e2")
        self.soldeAjout.place(anchor="center", x=int(2 * self.width / 3), y=int(self.height / 2))
        self.widgets.append(self.soldeAjout)

        self._validate = tk.Button(self.root, text="Valider", font=("arial", 14), command=lambda ppl=paypal: self.validate(paypal=ppl), bg="#fd3303",
                                   activebackground="#000000", fg="#ffffff", activeforeground="#ffffff", pady=2, bd=0,
                                   highlightthickness=0)
        self._validate.place(anchor="center", x=int(2 * self.width / 3), y=int(self.height / 2) + 50)
        self.widgets.append(self._validate)

        self._cancel = tk.Button(self.root, text="Annuler", font=("arial", 14), command=self.cancel, bg="#fd3303",
                                 activebackground="#000000", fg="#ffffff", activeforeground="#ffffff", pady=2, bd=0,
                                 highlightthickness=0)
        self._cancel.place(anchor="center", x=int(2 * self.width / 3), y=int(self.height / 2) + 100)
        self.widgets.append(self._cancel)

        print("[Info] Actual grade : {}".format(session["grade"]))

        if not paypal:
            if session["grade"] == 0 or session["grade"] == (0 - 1):
                self.connect(_user=session)

        self.numericalKeyboard()

