## Installationshinweise für einen Raspi mit HypriotOS 

##### Voraussetzungen:

Python 3.5.3   
pip3  
evtl. Nachinstallation mit 

```
sudo apt-get install python3-pip
```
    
---
    
##### Installation:    

```
cd ProGlove
pip3 install -r requirements.txt
```
Proglove-Box an USB-Port anschließen, dann:

```
dmesg | grep tty  
```
Ausgabe:
```
.... cdc_acm 1-1.2:1.0: ttyACM0: USB ACM device
```     
Checken der Rechte:
```   
pirate@iotreadykit08:~$ ls -l /dev/ttyACM0
crw-rw---- 1 root dialout 166, 0 Aug 22 20:21 /dev/ttyACM0
```
Jeder User darf jetzt vom ttyACM0 lesen:
```
sudo usermod -a -G dialout $USER
```    
Raspi neu starten mit abgezogenem Proglove, dann Proglove wieder in den USB-Port einstecken.
Starten der Anwendung:
```
cd ProGlove
python3 proglove
```  
Im Fall der Ausgabe:
```
ImportError: libxslt.so.1: cannot open shared object file: No such file or directory  
```
hilft:
```
sudo apt-get install libxslt-dev
```    
dann nochmals:
```
pirate@iotreadykit08:~/ProGlove$ python3 proglove
 * Serving Flask app "Proglove Webservice" (lazy loading)
 * Environment: production
   WARNING: Do not use the development server in a production environment.
   Use a production WSGI server instead.
 * Debug mode: off
```