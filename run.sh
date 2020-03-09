# Flushing paypal database
rm /home/pi/TechDistri/Handlers/PayPal/db.json
echo "{}" >> /home/pi/TechDistri/Handlers/PayPal/db.json
python3 /home/pi/TechDistri/main.py
