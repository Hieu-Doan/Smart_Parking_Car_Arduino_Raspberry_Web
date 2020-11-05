import cv2
import os
import time
import DetectChars
import DetectPlates
import serial
import yaml
import numpy as np
import imutils
import PossiblePlate
import threading
import paho.mqtt.client as mqtt

client = mqtt.Client()
client.username_pw_set(username="user", password="         ")  #your password
client.connect("mqtt.thingspeak.com", 1883, 60)
data1 = data2 = data3 = data4 = data5 = data6 = 0

def thingspeak_mqtt(data1, data2, data3, data4, data5, data6):
    channelID = "    "      #your channel ID
    apikey = "       "      #your apikey
    client.publish("channels/%s/publish/%s" % (channelID, apikey),
                   "field1=%s&field2=%s&field3=%s&field4=%s&field5=%s&field6=%s" % (
                   data1, data2, data3, data4, data5, data6))
# end thingspeck_mqtt    

# module level variables ##########################################################################
SCALAR_BLACK = (0.0, 0.0, 0.0)
SCALAR_WHITE = (255.0, 255.0, 255.0)
SCALAR_YELLOW = (0.0, 255.0, 255.0)
SCALAR_GREEN = (0.0, 255.0, 0.0)
SCALAR_RED = (0.0, 0.0, 255.0)

showSteps =  False

###################################################################################################
def Check_empty_parking_car():
    fn_yaml = r"/home/pi/Desktop/System/datasets/Smart_Parking_Car.yml"
    cap = cv2.VideoCapture(4)  #(0) or (1) choose camera
    
    config = {'text_overlay': True,
              'parking_overlay': True,
              'parking_detection': True,
              'park_sec_to_wait': 3}    

    video_info = {'fps': cap.get(cv2.CAP_PROP_FPS),
                  'width': int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)),
                  'height': int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)),
                  'fourcc': cap.get(cv2.CAP_PROP_FOURCC),
                  'num_of_frames': int(cap.get(cv2.CAP_PROP_FPS))}

    with open(fn_yaml, 'r') as stream:  # "r" chi đọc
        parking_data = yaml.load(stream, Loader=yaml.Loader)  # If error in this line, change "FullLoader"-->"Loader"
    parking_contours = []  
    parking_bounding_rects = []
    parking_mask = []

    for park in parking_data:
        points = np.array(park['points'])  
        id = np.array(park['id'])  
        rect = cv2.boundingRect(points)  
        points_shifted = points.copy()  
        points_shifted[:, 0] = points[:, 0] - rect[0]  
        points_shifted[:, 1] = points[:, 1] - rect[1]
        parking_contours.append(points)
        parking_bounding_rects.append(rect)
        mask = cv2.drawContours(np.zeros((rect[3], rect[2]), dtype=np.uint8), [points_shifted], contourIdx=-1,
                                color=255, thickness=-1, lineType=cv2.LINE_8)
        mask = mask == 255
        parking_mask.append(mask)

    parking_status = [False] * len(parking_data)
    parking_buffer = [None] * len(parking_data)

    video_cur_frame = 0
    video_cur_pos = 0
    while (cap.isOpened()):
        spot = 0
        occupied = 0
        video_cur_pos += 1  # Current position of the video file in seconds
        video_cur_frame += 1  # Index of the frame to be decoded/captured next
        ret, frame = cap.read()

        if ret == False:
            print("Capture Error")
            break

        frame_blur = cv2.GaussianBlur(frame.copy(), (5, 5), 3)
        frame_gray = cv2.cvtColor(frame_blur, cv2.COLOR_BGR2GRAY)
        frame_out = frame.copy()

        if config['parking_detection']:
            for ind, park in enumerate(parking_data):
                points = np.array(park['points'])
                rect = parking_bounding_rects[ind]
                roi_gray = frame_gray[rect[1]:(rect[1] + rect[3]),
                           rect[0]:(rect[0] + rect[2])]  # crop roi for faster calculation

                points[:, 0] = points[:, 0] - rect[0]  # shift contour to roi
                points[:, 1] = points[:, 1] - rect[1]
                # print(np.std(roi_gray), np.mean(roi_gray))
                status = np.std(roi_gray) < 20 and np.mean(roi_gray) > 50    
                # If detected a change in parking status, save the current time
                if status != parking_status[ind] and parking_buffer[ind] == None:
                    parking_buffer[ind] = video_cur_pos
                # If status is still different than the one saved and counter is open
                elif status != parking_status[ind] and parking_buffer[ind] != None:
                    if video_cur_pos - parking_buffer[ind] > config['park_sec_to_wait']:
                        parking_status[ind] = status
                        parking_buffer[ind] = None
                # If status is still same and counter is open
                elif status == parking_status[ind] and parking_buffer[ind] != None:
                    # if video_cur_pos - parking_buffer[ind] > config['park_sec_to_wait']:
                    parking_buffer[ind] = None

        if config['parking_overlay']:
            for ind, park in enumerate(parking_data):
                points = np.array(park['points'])
                id = np.array(park['id'])  
                if parking_status[ind]:
                    color = (0, 255, 0)  
                    spot = spot + 1
                    #print("ID empty box: ", id)  
                    if id == 1:
                        data1 = 0
                    if id == 2:
                        data2 = 0
                    if id == 3:
                        data3 = 0
                    if id == 4:
                        data4 = 0
                    if id == 5:
                        data5 = 0
                    if id == 6:
                        data6 = 0
                else:
                    color = (0, 0, 255)  
                    occupied = occupied + 1
                    if id == 1:
                        data1 = 1
                    if id == 2:
                        data2 = 1
                    if id == 3:
                        data3 = 1
                    if id == 4:
                        data4 = 1
                    if id == 5:
                        data5 = 1
                    if id == 6:
                        data6 = 1
                cv2.drawContours(frame_out, [points], contourIdx=-1, color=color, thickness=2, lineType=cv2.LINE_8)
                moments = cv2.moments(points)
                centroid = (int(moments['m10'] / moments['m00']) - 3, int(moments['m01'] / moments['m00']) + 3)
                cv2.putText(frame_out, str(park['id']), (centroid[0] + 1, centroid[1] + 1), cv2.FONT_HERSHEY_SIMPLEX,
                            0.4, (255, 255, 255), 1, cv2.LINE_AA)  
                cv2.putText(frame_out, str(park['id']), (centroid[0] - 1, centroid[1] - 1), cv2.FONT_HERSHEY_SIMPLEX,
                            0.4, (255, 255, 255), 1, cv2.LINE_AA)
                cv2.putText(frame_out, str(park['id']), (centroid[0] + 1, centroid[1] - 1), cv2.FONT_HERSHEY_SIMPLEX,
                            0.4, (255, 255, 255), 1, cv2.LINE_AA)
                cv2.putText(frame_out, str(park['id']), (centroid[0] - 1, centroid[1] + 1), cv2.FONT_HERSHEY_SIMPLEX,
                            0.4, (255, 255, 255), 1, cv2.LINE_AA)
                cv2.putText(frame_out, str(park['id']), centroid, cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 0, 0), 1,
                            cv2.LINE_AA)

        if config['text_overlay']:
            cv2.rectangle(frame_out, (1, 0), (200, 5), (255, 255, 255), 45)  
            # str_on_frame = "Frames: %d/%d" % (video_cur_frame, video_info['num_of_frames'])        
            # cv2.putText(frame_out, str_on_frame, (5,30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0,128,255), 2, cv2.LINE_AA)   
            str_on_frame = "Spot: %d Occupied: %d" % (spot, occupied)  
            cv2.putText(frame_out, str_on_frame, (5, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 128, 255), 2,
                        cv2.LINE_AA)  
            #print("occupied: ", occupied)  
            #print("spot: ", spot)  

        cv2.imshow('Smart Parking Detection', frame_out)
        cv2.moveWindow('Smart Parking Detection',720,15)
        
        thingspeak_mqtt(data1, data2, data3, data4, data5, data6)
        
        k = cv2.waitKey(1)
        if k == ord('q'):  # click "q" to come out
            break
    cap.release()
    cv2.destroyAllWindows()
#end Check_empty_parking_car
###################################################################################################
def Check_license_plate():
    while (1):
        ser = serial.Serial("/dev/ttyACM0",9600, timeout = 1)     # Check ttyACM* when it can't connect to serial
        ser.flush()
        while (True):
            line = ser.readline().decode('utf-8').rstrip('\n')  
            if line == 'I':  #change I or O for camera in or out
                ser.write(b"I\n")
                print("Check camera Way In")
                cap1 = cv2.VideoCapture(0)   # camera check license plate Way In
                break
            if line == 'O':
                ser.write(b"O\n")
                print("Check camera Way Out")
                cap1 = cv2.VideoCapture(2)   # camera check license plate Way Out
                break
        # end while
                
        ret1, frame1 = cap1.read()
        frame1 = cv2.resize(frame1, (1280, 720))
        cv2.imshow("Check License Plate", frame1)
        cv2.imwrite("LicPlateImages/test.jpg", frame1)
        time.sleep(1.5)
        
        blnKNNTrainingSuccessful = DetectChars.loadKNNDataAndTrainKNN()  # attempt KNN training
        if blnKNNTrainingSuccessful == False:  # if KNN training was not successful
            print("\nerror: KNN traning was not successful\n")  # show error message
            return  # and exit program
        # end if
        imgOriginalScene = cv2.imread("LicPlateImages/test.jpg")  # open image

        if imgOriginalScene is None:  # if image was not read successfully
            print("\nerror: image not read from file \n\n")  # print error message to std out
            os.system("pause")  # pause so user can see error mqessage
            return  # and exit program
        # end if

        listOfPossiblePlates = DetectPlates.detectPlatesInScene(imgOriginalScene)  # detect plates

        listOfPossiblePlates = DetectChars.detectCharsInPlates(listOfPossiblePlates)  # detect chars in plates

        #cv2.imshow("imgOriginalScene", imgOriginalScene)  # show scene image

        if len(listOfPossiblePlates) == 0:  # if no plates were found
            print("\n no license plates were detected\n")  # inform user no plates were found
            ser.write(b"0\n")   
        else:  
            # if we get in here list of possible plates has at leat one plate
            # sort the list of possible plates in DESCENDING order (most number of chars to least number of chars)
            listOfPossiblePlates.sort(key=lambda possiblePlate: len(possiblePlate.strChars), reverse=True)
            # suppose the plate with the most recognized chars (the first plate in sorted by string length descending order) is the actual plate
            licPlate = listOfPossiblePlates[0]

            cv2.imshow("imgPlate", licPlate.imgPlate)  # show crop of plate and threshold of plate
            cv2.imshow("imgThresh", licPlate.imgThresh)

            if len(licPlate.strChars) == 0:  # if no chars were found in the plate
                print("\n no characters were detected\n\n")  # show message
                cv2.destroyWindow("Check License Plate")
                ser.write(b"0\n")     #test  
                return  # and exit program
            # end if
            drawRedRectangleAroundPlate(imgOriginalScene, licPlate)  # draw red rectangle around plate
            print("\nlicense plate is = " + licPlate.strChars + "\n")  # write license plate text to std out            
            print("----------------------------------------")                
            writeLicensePlateCharsOnImage(imgOriginalScene, licPlate)  # write license plate text on the image
            #cv2.imshow("imgOriginalScene", imgOriginalScene)  # re-show scene image
            cv2.imwrite("imgOriginalScene.png", imgOriginalScene)  # write image out to file
            
            Encode_licPlate = licPlate.strChars.encode()   #encode string and send to Arduino
            ser.write(Encode_licPlate)
            ser.write(b"\n")
            
        # end if else      
        cap1.release()
        cv2.destroyWindow("Check License Plate") 
  #end while
# end main
###################################################################################################
def drawRedRectangleAroundPlate(imgOriginalScene, licPlate):

    p2fRectPoints = cv2.boxPoints(licPlate.rrLocationOfPlateInScene)            # get 4 vertices of rotated rect

    cv2.line(imgOriginalScene, tuple(p2fRectPoints[0]), tuple(p2fRectPoints[1]), SCALAR_RED, 2)         # draw 4 red lines
    cv2.line(imgOriginalScene, tuple(p2fRectPoints[1]), tuple(p2fRectPoints[2]), SCALAR_RED, 2)
    cv2.line(imgOriginalScene, tuple(p2fRectPoints[2]), tuple(p2fRectPoints[3]), SCALAR_RED, 2)
    cv2.line(imgOriginalScene, tuple(p2fRectPoints[3]), tuple(p2fRectPoints[0]), SCALAR_RED, 2)
# end function

###################################################################################################
def writeLicensePlateCharsOnImage(imgOriginalScene, licPlate):
    ptCenterOfTextAreaX = 0                             # this will be the center of the area the text will be written to
    ptCenterOfTextAreaY = 0

    ptLowerLeftTextOriginX = 0                          # this will be the bottom left of the area that the text will be written to
    ptLowerLeftTextOriginY = 0

    sceneHeight, sceneWidth, sceneNumChannels = imgOriginalScene.shape
    plateHeight, plateWidth, plateNumChannels = licPlate.imgPlate.shape

    intFontFace = cv2.FONT_HERSHEY_SIMPLEX                      # choose a plain jane font
    fltFontScale = float(plateHeight) / 30.0                    # base font scale on height of plate area
    intFontThickness = int(round(fltFontScale * 1.5))           # base font thickness on font scale

    textSize, baseline = cv2.getTextSize(licPlate.strChars, intFontFace, fltFontScale, intFontThickness)        # call getTextSize

            # unpack roatated rect into center point, width and height, and angle
    ( (intPlateCenterX, intPlateCenterY), (intPlateWidth, intPlateHeight), fltCorrectionAngleInDeg ) = licPlate.rrLocationOfPlateInScene

    intPlateCenterX = int(intPlateCenterX)              # make sure center is an integer
    intPlateCenterY = int(intPlateCenterY)
    ptCenterOfTextAreaX = int(intPlateCenterX)         # the horizontal location of the text area is the same as the plate

    if intPlateCenterY < (sceneHeight * 0.75):                                                  # if the license plate is in the upper 3/4 of the image
        ptCenterOfTextAreaY = int(round(intPlateCenterY)) + int(round(plateHeight * 1.6))      # write the chars in below the plate
    else:                                                                                       # else if the license plate is in the lower 1/4 of the image
        ptCenterOfTextAreaY = int(round(intPlateCenterY)) - int(round(plateHeight * 1.6))      # write the chars in above the plate
    # end if
    textSizeWidth, textSizeHeight = textSize                # unpack text size width and height
    ptLowerLeftTextOriginX = int(ptCenterOfTextAreaX - (textSizeWidth / 2))           # calculate the lower left origin of the text area
    ptLowerLeftTextOriginY = int(ptCenterOfTextAreaY + (textSizeHeight / 2))          # based on the text area center, width, and height
    # write the text on the image
    cv2.putText(imgOriginalScene, licPlate.strChars, (ptLowerLeftTextOriginX, ptLowerLeftTextOriginY), intFontFace, fltFontScale, SCALAR_YELLOW, intFontThickness)
# end function

if __name__ == "__main__":
   
    t = time.time()
    t1 = threading.Thread(target= Check_empty_parking_car)
    t2 = threading.Thread(target= Check_license_plate)
    t1.start()
    t2.start()

