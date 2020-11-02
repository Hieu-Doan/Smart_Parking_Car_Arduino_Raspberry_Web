# Smart_Parking_Car_Arduino_Raspberry_Web
How to run ?
Arduino:
0. Add Library of folder "Library_for_System": Sketch-> Add File-> Choose...
1. Load code arduino "System" into the board.

Server:
Create account in "ThingSpeak"
Create your channel in "ThingSpeak"

Raspberry:
0. Library settings needed:
	Python (3.5.3)
	OpenCV (4.1.0)
	Pip (9.0.1)
	Pyserial (3.4)
	PyYAML (5.3.1)
	Numpy (1.12.1)
	Imutils (0.5.3)
	paho.mqtt.client (1.5.0)
	picamera (1.13) 
	Pillow (4.0.0)
1. Connect wifi or 3G.
2. Connect to Arduino use USB port.
3. Open file Main.py
4. Add password, channelID, apikey of your thingspeak
5. Change the related path .yml
6. Check USB port ttyACM*.   (Often ttyACM0 or ttyACM1)
7. Check select Camera in cap & cap1. 
Run 
If you want to training chars. Its on file "Training_KNN_Character_Recognition_Python-master"

Webserver:
Run file webparkingcar

