import cv2
import yaml
refPt = []                  #tạo danh sách
cropping = False
data = []

cap = cv2.VideoCapture(2)

while True:
    ret, frame = cap.read()
    #frame = cv2.resize(frame, (1280, 720))
    cv2.imshow("Click 'q' to take photo", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        cv2.imwrite("/home/pi/Desktop/System/datasets/Smart_Parking_Car.jpg", frame)
        break

file_path = "/home/pi/Desktop/System/datasets/test.yml"
img = cv2.imread("/home/pi/Desktop/System/datasets/Smart_Parking_Car.jpg")

def yaml_loader(file_path):
    with open(file_path, "r") as file_descr:
        data = yaml.load(file_descr)
        return data

def yaml_dump(file_path, data):
    with open(file_path, "a") as file_descr:
        yaml.dump(data, file_descr)

def yaml_dump_write(file_path, data):
    with open(file_path, "w") as file_descr:
        yaml_dump(data, file_descr)

def click_and_crop(event, x ,y, flag, param):
    current_pt = {'id': 0, 'points': []}
    global refPt, cropping
    if event == cv2.EVENT_LBUTTONDBLCLK:
        refPt.append((x,y))         #lưu tọa độ điểm dánh dấu (x,y)
        cropping = False
    if len(refPt) == 4:
        if data == []:          #nếu list trống (thường là vòng lặp đầu tiên vì data chưa có gì)
            if yaml_loader(file_path) != None:              #nếu file path đã có dữ liệu rồi ( "!= None" = đã có rồi)
                data_already = len(yaml_loader(file_path))
            else:
                data_already = 0
        else:                   #chép vào data từ lần thứ 2 trở đi
            if yaml_loader(file_path) != None:
                data_already = len(data) + len(yaml_loader(file_path))
            else:
                data_already = len(data)

        cv2.line(img, refPt[0], refPt[1], (0, 255, 0), 2)    #cv2.line(tên hình, tọa độ đầu, tọa độ cuối, màu sắc, đồ dày)
        cv2.line(img, refPt[1], refPt[2], (0, 255, 0), 2)    #refPt[?] là vị trí của thứ ? trong danh sách của refPt
        cv2.line(img, refPt[2], refPt[3], (0, 255, 0), 2)
        cv2.line(img, refPt[3], refPt[0], (0, 255, 0), 2)

        temp_lst1 = list(refPt[2])      #2
        temp_lst2 = list(refPt[3])      #3
        temp_lst3 = list(refPt[0])      #0
        temp_lst4 = list(refPt[1])      #1

        current_pt['points'] = [temp_lst1, temp_lst2, temp_lst3, temp_lst4]
        current_pt['id'] = data_already
        data.append(current_pt)

        refPt = []
#image = cv2.resize(img, None, fx = 0.6, fy = 0.6)          #chỉnh sửa kích thước khung hình
clone = img.copy()
cv2.namedWindow("Double click to mark points")
cv2.imshow("Double click to mark points",img)
cv2.setMouseCallback("Double click to mark points", click_and_crop)

#keep looping until the 'q' key is pressed
while True:
    #display the image and wait for a keypress
    cv2.imshow("Double click to mark points", img)
    key = cv2.waitKey(1)
    if key == ord('q'):
        break
#data list into yaml file
if data != []:
    yaml_dump(file_path, data)
cv2.destroyAllWindows()

