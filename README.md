# TechDistri
## 1. Description

Distributeur automatique du Technistub créé avec la particpation de Christophe de Sabbata, Morgan Jourdin, Guillaume Strub et Vincent Sahler

Ceci est le code du distributeur du technistub, il est écrit pour correspondre avec un écran tactile 7" Raspberry Pi officiel et un Raspberry Pi 3
Il a besoin de :
  - Un lecteur MFRC522 et sa librairie MFRC522-python
  - Une base de donnée hébergée en local (mysql)

Le script tourne sous Python 3.5.3 avec une interface Tkinter.

## 2. Installation
### 2.1 Système

Pour tourner l'écran :
```
sudo nano /boot/config.txt
```
Et y insérer à la fin 
```
display_rotate=3
lcd_rotate=3
```

Pour tourner le tactile automatiquement au démarage :
```
sudo apt-get install xinput
sudo echo "DISPLAY=:0.0 xinput --set-prop 'FT5406 memory based driver' 'Coordinate Transformation Matrix' 0 -1 1 1 0 0 0 0 1" >> ~/.profile
```

### 2.2 Programme
#### 2.2.1 Script
Pour installer le programme : 
```
sudo apt-get install git
cd ~
git clone https://github.com/TechniStub/TechDistri.git
echo "alias startApp='python3 ~/TechDistri/main.py'" >> ~/.bashrc
echo "export PYTHONPATH='${PYTHONPATH}:/home/pi/TechDistri/Handlers/MFRC522'" >> ~/.bashrc
```

#### 2.2.2 Dépendences
```
sudo apt-get install python3 pip3
```

Et installez SPI-Py, paypalrestsdk et qrcode avec python3

### 2.3 MySQL
#### 2.3.1 Installation

Installez une base MySQL.

Créez un utilisateur pour la machine 127.0.0.1 uniquement :
  Ces parametres seront renseignés dans le fichier /Handlers/DataBase/params.xml, dans <parameter/>

#### 2.3.2 Configuration
```
sudo mysql -u root < ~/TechDistri/deploy.sql
```
