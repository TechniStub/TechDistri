# Import des librairies
import tkinter as tk
from PIL import ImageTk, Image
import time
import os

# Import des "Feuilles" de GUI
import Handlers.GUI.Home as handlerGuiHome
import Handlers.DataBase.db as databaseHandler
import Handlers.MFRC522.handler as rfidHandler
import Handlers.GUI.Admin.Level1 as handlerGuiAdmin1
import Handlers.GUI.User.Level1 as handlerGuiUser1


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
Print("|-- [GUI] Started")
root.attributes('-fullscreen', True) # on lui affecte l'écran
root.configure(background="white")
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

def clearTk(toClr): # definition de la fonction d' éfacage du gui
    for widget in toClr.winfo_children():
        widget.destroy()

def quit(): # stopper le programme
    Print("[Stop]")
    root.destroy()
    Print("|-- [GUI] Killed")
    rfidInst.stop = True
    rfidInst.join()
    Print("|-- [MFRC522] Killed")
    dbInst.cursor.close()
    dbInst.conn.close()
    Print("|-- [DataBase] Killed")

root.bind('<Escape>',lambda e: quit())

def update(): # update du gui
    root.update()
    root.update_idletasks()

#definition des Instances des Feuilles
handlers["home"] = handlerGuiHome.HomeHandler(root, ts, rfidInst)
handlers["admin"] = {}
handlers["admin"]["level1"] = handlerGuiAdmin1.AdminHandler(root, ts, home)
handlers["user"] = {}
handlers["user"]["level1"] = handlerGuiUser1.UserHandler(root, ts)
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

session["bypassHome"] = False

while True: # boucle infinie
    if(session["bypassAll"]): # si on est bypassé, on le remet a 0 le bypass et le gui
        session["bypassAll"]= False
        clearTk(root)
        handlers["admin"]["level1"].isSelected = False
        handlers["admin"]["level1"].selected = 0
        if(session["bypassHome"]):
            print("go to home")
            session["bypassHome"] = False
            rfidInst.readed = True
            rfidInst.lastId = session["badgeInProcess"]
        else:
            handlers["home"].set()

    try:
        update()
    except:
        exit()
        quit()

    if(rfidInst.readed and rfidInst.lastId != None): # avons-nous un badge ?
        session["badgeInProcess"] = rfidInst.lastId # on stocke le badge dans session
        Print("[INFO] Scanned {}".format(session["badgeInProcess"]))
        rfidInst.readed = False # la lecture a ete faite
        Print("|-- [DataBase] Searching with badge {}".format(session["badgeInProcess"]))

        # --------- INFO UTILISATEUR ---------
        user = dbInst.getQuery(queries["getUserInfo"].format(session["badgeInProcess"]))
        userQty = 0

        for (badgeId, uuid, nom, pnom, grade, credit) in user:
            userQty += 1
            session["uuid"] = uuid
            session["nom"] = nom
            session["pnom"] = pnom
            session["grade"] = grade
            session["credit"] = credit
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
                if(session["nom"] == "LABORDE" and session["pnom"] == "Stephane"):
                    session["gradeInText"] = ""
                else :
                    session["gradeInText"] = "admin"
            elif(session["grade"] == 2):
                session["gradeInText"] = "permanent"
            else:
                session["grade"] = 1
                session["gradeInText"] = "user"
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
                        Print("[GUI] Starting User Gui")
                        showRemanent() # on affiche les infos de base de l'user
                        products = dbInst.getProducts()
                        handlers["user"]["level1"].set(session, parameters, products)
                        update()
                    elif(session["adminSelection"] == 2):
                        pass
                    else:
                        pass
            elif(session["grade"] == 2): # on est permanent
                pass
            else: # on est user
                pass
        else:
            Print("[Instance] Rebooting ...")

# hey ! inspecteur gadget
# The law is law !
