# TechDistri
 ---------------   DEVELOPPEMENT EN COURS CODE NON ACCESSIBLE POUR LE MOMENT   ---------------

Distributeur automatique du Technistub créé avec la particpation de Christophe de Sabbata, Morgan Jourdin, Guillaume Strub et Vincent Sahler

Ceci est le code du distributeur du technistub, il est écrit pour correspondre avec un écran tactile 7" Raspberry Pi officiel et un Raspberry Pi 3
Il a besoin de :
  - Un lecteur MFRC522 et sa librairie MFRC522-python
  - Une base de donnée hébergée en local (mysql)

Le script tourne sous Python 3 avec une interface Tkinter.
Deux alias ont été définis, pour les définirs : 
  - echo "alias python='python3'" >> ~/.profile
  - echo "alias startApp='python ~/dev/main.py'" >> ~/.profile
  
Voir fichier "install.sh"
