# Import des librairies
import tkinter as tk
from PIL import ImageTk, Image
import time
import os
import sys

# Import des "Feuilles" de GUI
import Handlers.GUI.Home as handlerGuiHome
import Handlers.DataBase.db as databaseHandler
import Handlers.MFRC522.handler as rfidHandler
import Handlers.GUI.Admin.Level1 as handlerGuiAdmin1
import Handlers.GUI.Admin.Level2 as handlerGuiAdmin2
import Handlers.GUI.Admin.Level3 as handlerGuiAdmin3
import Handlers.GUI.User.Level1 as handlerGuiUser1
import Handlers.GUI.User.Level2 as handlerGuiUser2
import Handlers.GUI.User.Level3 as handlerGuiUser3
import Handlers.GUI.Keyboard as handlerVirualKeyboard

import Handlers.GUI.common as commonGUI


##
##               |--> Level 2 (ACHAT)
##               |
##  UTILISATEUR -|--> Level 4 (Ajouter Du credit)
##  Level 1      |
##  Selection de |--> Level 3 (HISTOrique)
##  Histo ou
##  achat


handlers = {} # definition des Handlers, instances des Feuilles
session = {} # definition de l'équivalent de $_SESSION

def Print(data): # redéfinition de print pour qu' il aille dans un fichier de log
    print("{} {}".format(time.strftime("%d %b %y, %H:%M:%S", time.localtime()), data))

Print("[Start]") # On informe que ça démare

dbInst = databaseHandler.DataBaseHandler("/home/pi/TechDistri/Handlers/DataBase/params.xml") # on ouvre une instance des base de donnée avec .xml en config
queries = dbInst.getAvailableQueries() # on récupere les différentes requetes déja disponible
_parameters = dbInst.getQuery(queries["getParameters"])
parameters = {}
for (Id, Name, Value, Type) in _parameters:
    parameters[Name] = {}
    parameters[Name]["id"] = Id
    parameters[Name]["value"] = Value
    parameters[Name]["type"] = Type

Print("|-- [DataBase] Connected") # on informe
rfidInst = rfidHandler.RFIDHandler() # on ouvre une instance du lecteur RFID
rfidInst.start() # on le démarre
Print("|-- [MFRC522] Connected")

root = tk.Tk() # on démarre le gui pricipal
commonGUIinst = commonGUI.commonGUIs()
Print("|-- [GUI] Started")
root.attributes('-fullscreen', True) # on lui affecte l'écran
root.configure(background="white")
root.config(cursor="crosshair")

#ts = tk.PhotoImage(file="Resources/ts.jpg") <- Does not work
original = Image.open("/home/pi/TechDistri/Resources/ts.jpg") # on ouvre le logo
resized = original.resize((200, 105), Image.ANTIALIAS) # on le redimentionne

ts = ImageTk.PhotoImage(resized) # on le convertit en compatible gui

original = Image.open("/home/pi/TechDistri/Resources/home.jpg") #idem
resized = original.resize((47, 47), Image.ANTIALIAS)

home = ImageTk.PhotoImage(resized)

original = Image.open("/home/pi/TechDistri/Resources/exit.png") #idem
resized = original.resize((47, 47), Image.ANTIALIAS)

exit = ImageTk.PhotoImage(resized)

original = Image.open("/home/pi/TechDistri/Resources/scrollDown.png") #idem
resized = original.resize((28, 17), Image.ANTIALIAS)

scrollDown = ImageTk.PhotoImage(resized)

original = Image.open("/home/pi/TechDistri/Resources/scrollUp.png") #idem
resized = original.resize((28, 17), Image.ANTIALIAS)

scrollUp = ImageTk.PhotoImage(resized)

original = Image.open("/home/pi/TechDistri/Resources/scrollLeft.png") #idem
resized = original.resize((17, 28), Image.ANTIALIAS)

scrollLeft = ImageTk.PhotoImage(resized)

original = Image.open("/home/pi/TechDistri/Resources/scrollRight.png") #idem
resized = original.resize((17, 28), Image.ANTIALIAS)

scrollRight = ImageTk.PhotoImage(resized)

original = Image.open("/home/pi/TechDistri/Resources/trash.png") #idem
resized = original.resize((47, 47), Image.ANTIALIAS)

trash = ImageTk.PhotoImage(resized)

def clearTk(toClr): # definition de la fonction d' éfacage du gui
    for widget in toClr.winfo_children():
        widget.destroy()

def quit(): # stopper le programme
    Print("[Stop]")
    try:
        root.destroy()
    except:
        pass
    exited=True
    Print("|-- [GUI] Killed")
    rfidInst.stop = True
    rfidInst.join()
    Print("|-- [MFRC522] Killed")
    dbInst.cursor.close()
    dbInst.conn.close()
    Print("|-- [DataBase] Killed")
    sys.exit()

root.bind('<Escape>',lambda e: quit())

def update(): # update du gui
    try:
        root.update()
        pass
    except:
        pass
"""
    try:
        root.update_idletasks()
    except:
        pass"""

#definition des Instances des Feuilles
handlers["home"] = handlerGuiHome.HomeHandler(root, ts, rfidInst)
handlers["keyboard"] = handlerVirualKeyboard.VirtualKeyboard(name="Clavier")
handlers["admin"] = {}
handlers["admin"]["level1"] = handlerGuiAdmin1.AdminHandler(root, ts, home)
handlers["admin"]["level2"] = handlerGuiAdmin2.AdminHandler(root, ts, home, rfidInst, dbInst, queries, handlers["keyboard"], trash, commonGUIinst, scrollLeft, scrollRight, session)
handlers["admin"]["level3"] = handlerGuiAdmin3.AdminHandler(root, ts, home, rfidInst, dbInst, queries, handlers["keyboard"], trash, commonGUIinst, scrollLeft, scrollRight, session)
handlers["user"] = {}
handlers["user"]["level1"] = handlerGuiUser1.UserHandler(root, ts)
handlers["user"]["level2"] = handlerGuiUser2.UserHandler(root, ts)
handlers["user"]["level3"] = handlerGuiUser3.UserHandler(root, ts, scrollUp, scrollDown)
handlers["home"].set() # on envoie le gui

session["bypassAll"] = False # on désactive le bypass

def deco(): # activation du bypass
    session["bypassAll"]= True
    print("Deconnexion !")

def gotohome(): # activation du bypass
    session["bypassHome"]= True
    session["bypassAll"]= True
    print("Going to home")

def showRemanent(): # affichage des infos de base de l'utilisateur
    height = root.winfo_screenheight()
    width = root.winfo_screenwidth()
    lNom = tk.Label(root, text="Nom : "+str(session["nom"]), font=("Arial", 14), anchor='n', background="white")
    lNom.place(anchor="nw", x=30, y=18)

    lreset = tk.Button(root, image=exit, highlightthickness = 0, bd = 0, bg="#fff", command=deco)
    lreset.place(anchor="se", x=width-30, y=height-18)

    lpnom = tk.Label(root, text="Prenom : "+str(session["pnom"]), font=("Arial", 14), anchor='n', background="white")
    lpnom.place(anchor="nw", x=30, y=48)

    lgrade = tk.Label(root, text="Grade : "+str(session["gradeInText"]), font=("Arial", 14), anchor='n', background="white")
    lgrade.place(anchor="nw", x=30, y=78)

    limage = tk.Label(root, image=ts, background="white")
    limage.place(anchor="ne", x=width, y=0)

    lhome = tk.Button(root, image=home, background="white", highlightthickness = 0, bd = 0, bg="#fff", command=gotohome)
    lhome.place(anchor="sw", x=30, y=height-18)

def userHandler():
    Print("[GUI] Starting User Gui")
    showRemanent() # on affiche les infos de base de l'user
    handlers["user"]["level1"].set(session)
    while handlers["user"]["level1"].selection == 0 and session["bypassAll"] == False: # rien
        update() # why not ?

    clearTk(root)

    if handlers["user"]["level1"].selection == 1: # achat
        showRemanent()
        products = dbInst.getProducts()
        handlers["user"]["level2"].set(session, parameters, products)
        update()
        while not handlers["user"]["level2"].canceled and session["bypassAll"] == False:
            update()

        try:
            handlers["user"]["level2"].cancel()
            Print("Auto Canceled Command")
        except:
            pass


        if handlers["user"]["level2"].validated and handlers["user"]["level2"].selection["qty"]!=0:
            print("Validated")
            selectedQty = handlers["user"]["level2"].selection["qty"]
            totalToPay = handlers["user"]["level2"].selection["total"]
            creditResult = handlers["user"]["level2"].selection["final"]
            productId = handlers["user"]["level2"].ActiveProduct["id"]
            productName= handlers["user"]["level2"].ActiveProduct["nomc"]
            updated=False
            try:
                productName = productName if selectedQty == 1 else str(selectedQty)+"x "+productName
                dbInst.edit(queries["updateStock"].format(selectedQty, productId))
                dbInst.edit(queries["transacToServer"].format(session["uuid"], totalToPay, productName))
                dbInst.edit(queries["updateCredits"].format(totalToPay, session["uuid"]))
            except:
                pass
        else:
            print("Canceled")
        handlers["user"]["level2"].canceled = False
        handlers["user"]["level2"].validated = False
    elif handlers["user"]["level1"].selection == 2: #Historique des transactions
        showRemanent()
        transacBuffer = dbInst.getQuery(queries["getTransaction"].format(session["uuid"]))
        transac = []
        index = -1
        labels=[]

        for(_id, _from, _to, _value, _date, _info) in transacBuffer:
            transac.append({})
            transac[index]["id"] = _id
            transac[index]["from"] = _from
            transac[index]["to"] = _to
            transac[index]["value"] = _value
            transac[index]["date"] = _date
            transac[index]["info"] = _info

        handlers["user"]["level3"].set(transac)



session["bypassHome"] = False
exited = False

while True: # boucle infinie
    if exited:
        break
    if(session["bypassAll"]): # si on est bypassé, on le remet a 0 le bypass et le gui
        clearTk(root)
        handlers["admin"]["level1"].isSelected = False
        handlers["admin"]["level1"].selected = 0
        if(session["bypassHome"]):
            rfidInst.readed = True
            rfidInst.lastId = session["badgeInProcess"]
            rfidInst.id = session["badgeInProcess"]
            print("go to home {} {}".format(rfidInst.readed, rfidInst.lastId))
        else:
            handlers["home"].set()
            session["bypassAll"]= False # on débypass
            session["bypassHome"] = False

    try:
        update()
    except:
        exited=True
        quit()

    if(rfidInst.readed and rfidInst.lastId != None): # avons-nous un badge ?
        session["bypassAll"]= False # on débypass
        session["bypassHome"] = False
        session["badgeInProcess"] = rfidInst.lastId # on stocke le badge dans session
        Print("[INFO] Scanned {}".format(session["badgeInProcess"]))
        rfidInst.readed = False # la lecture a ete faite
        Print("|-- [DataBase] Searching with badge {}".format(session["badgeInProcess"]))

        # --------- INFO UTILISATEUR ---------
        user = dbInst.getQuery(queries["getUserInfo"].format(session["badgeInProcess"]))
        userQty = 0

        for (badgeId, uuid, nom, pnom, grade, credit, GradeCustom) in user:
            userQty += 1
            session["uuid"] = uuid
            session["nom"] = nom
            session["pnom"] = pnom
            session["grade"] = grade
            session["credit"] = credit
            session["gradeCustom"] = GradeCustom
            Print("|-- [DataBase] Found : {} {}, Grade:{}, Credit:{}, UUID:{}".format(pnom, nom, grade, credit, uuid))

        if(userQty == 0):
            Print("[Error] User with badge {} was not found !".format(session["badgeInProcess"]))
            session["valide"] = False
        elif(userQty == 1):
            session["valide"] = True
            Print("[Instance] User with badge {} was found !".format(session["badgeInProcess"]))
        else:
            session["valide"] = False
            Print("[Error] To many user with badge {} was found !".format(session["badgeInProcess"]))
        # --------- FIN DEBROUILLE TOI --------- ps: le mur est sur ta gauche !

        if(session["valide"]): # si la session est validée par la db
            Print("[Instance] Continuing ...")
            if(grade == 1): # grade utilisateur standard
                # --------- SOMMES NOUS EN PRESENCE D'UN PERMANENT ---------
                permanences = dbInst.getQuery(queries["getGrade"].format(session["uuid"]))
                for (id, date) in permanences:
                    if(date == time.strftime("%y-%m-%d", time.localtime())):
                        session["grade"]=2 # on lui met le grade a l'user

            # --------- ON TRANSFORME LE GRADE EN TEXTE LISIBLE PAR UN USER STANDARD ---------
            if(session["grade"] == 0):
                session["gradeInText"] = "admin"
                session["sAdmin"] = False
            elif(session["grade"] == 2):
                session["gradeInText"] = "permanent"
                session["sAdmin"] = False
            elif(session["grade"] == (0-1)):
                session["gradeInText"] = "super-admin"
                session["grade"] = 0
                session["sAdmin"] = True
            else:
                session["grade"] = 1
                session["gradeInText"] = "user"
                session["sAdmin"] = False

            if session["gradeCustom"] != "-1":
                session["gradeInText"] = session["gradeCustom"]

            # --------- FIN ---------
            Print("[Instance] Grade found : {}".format(session["gradeInText"]))
            clearTk(root) # on clean
            Print("[GUI] Cleaned")
            Print("[GUI] Starting for this grade ...")


            if(session["grade"] == 0): # si on est admin
                showRemanent() # on affiche les infos de base de l'user
                handlers["admin"]["level1"].set(session) # on affiche le reste de l'ui
                # fonction blocante d'attente d'un boutton
                while(handlers["admin"]["level1"].isSelected == False and session["bypassAll"] == False):
                    update() # on l'update parcequ'on a rien d'autre a faire
                    #print(bypassAll) # on bypass Hall 9000 (All -> Hall ;)!!

                if session["bypassAll"]: # si on est bypassé (retour a la maison)
                    print("Bypass")
                    clearTk(root)
                else: # sinon
                    session['adminSelection'] = handlers["admin"]["level1"].selected # on stocke ce sur quoi on a appuyé (user, admin ou permanent)
                    Print("[GUI] {} was selected".format(session['adminSelection']))
                    clearTk(root) # on efface
                    if(session["adminSelection"] == 3): # si on va en user
                        userHandler() # on envoie user
                    elif(session["adminSelection"] == 1): # admin
                        print("[GUI] Starting Admin Gui")
                        showRemanent()
                        handlers["admin"]["level2"].set(session) # on affiche l'admin, le vrai
                        actualSession = handlers["admin"]["level2"]
                        actualSessionId = 2
                        while session["bypassAll"] == False:
                            while not(actualSession.finished) and not(actualSession.pageChanging) and session["bypassAll"] == False:
                                update()
                            if actualSession.pageChanging:
                                if actualSessionId == 2:
                                    actualSession = handlers["admin"]["level3"]
                                    actualSessionId = 3
                                else:
                                    actualSession = handlers["admin"]["level2"]
                                    actualSessionId = 2
                                handlers["admin"]["level2"].pageChanging = False
                                handlers["admin"]["level3"].pageChanging = False
                                clearTk(root)
                                showRemanent()
                                actualSession.set(session)
                                update()
                    elif(session["adminSelection"] == 2): #permanent
                        pass
                    else: # jico (just in case of)
                        userHandler()
            elif(session["grade"] == 2): # on est permanent
                pass
            else: # on est user
                userHandler()
        else:
            Print("[Instance] Rebooting ...")

# hey ! inspecteur gadget
# The law is law !
