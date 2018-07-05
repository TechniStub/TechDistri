# TechDistri
### 1. Description

Distributeur automatique du Technistub créé avec la particpation de Christophe de Sabbata, Morgan Jourdin, Guillaume Strub et Vincent Sahler

Ceci est le code du distributeur du technistub, il est écrit pour correspondre avec un écran tactile 7" Raspberry Pi officiel et un Raspberry Pi 3
Il a besoin de :
  - Un lecteur MFRC522 et sa librairie MFRC522-python
  - Une base de donnée hébergée en local (mysql)

Le script tourne sous Python 3 avec une interface Tkinter.

### 2. Installation

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

Pour installer le programme : 
```
sudo apt-get install git
cd ~
git clone https://github.com/TechniStub/TechDistri.git
echo "alias startApp='python3 ~/TechDistri/main.py'" >> ~/.bashrc
```
Et
```
sudo apt-get install python3 pip3
pip3 install spi
```
