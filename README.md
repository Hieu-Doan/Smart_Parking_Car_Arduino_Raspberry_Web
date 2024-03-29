# Smart_Parking_Car_Arduino_Raspberry_Web
## How to run 
### Arduino
0. Add Library of folder "Library_for_System": Sketch-> Add File-> Choose...
  - File library RFID1 of "Sunfounder" which I was a reference in their website but it can't turn 
    off by Select Slave pins in each RFID so that I was edited for me in this project.
1. Connection description in code Arduino.
2. Load code Arduino "System" into the board.

### Server
0. Create account in "ThingSpeak"
1. Create your channel in "ThingSpeak"

### Raspberry
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
8. Run. 

### Webserver
- Run file webparkingcar.html

## Notice
- Sometimes the identification of the license plate is not accurate.
- License plate processing time is quite slowly around 6-7s.(We use Rasberry Pi 3 B+)

## Reference
- Webserver: Design by An Nguyen (My partner)
- Link: https://github.com/ankit1khare/Automatic-Parking-Management
- Link: https://github.com/MicrocontrollersAndMore/OpenCV_3_License_Plate_Recognition_Python
- Link: https://github.com/MicrocontrollersAndMore/OpenCV_3_KNN_Character_Recognition_Python
- Link Library of Sunfounder: https://docs.sunfounder.com/projects/vincent-kit/en/latest/2.35_rfid-rc522_module.html

## Clip Demo 
- Link: https://youtu.be/WXhyleVbDTQ
