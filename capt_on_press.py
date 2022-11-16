import cv2
import os
import time
cam = cv2.VideoCapture(0)

cv2.namedWindow("Capturing")

img_counter = 1
ur_name = input('Enter your name: ')
path = 'D:/LAB_E3.1_PRJ/NetSecDay/FaceRecognition/Dataset/FaceData/raw/{}'.format(ur_name)
while True:
    for img_counter in range (1, 41):
        ret, frame = cam.read()
        if not ret:
            print("failed to grab frame")
            break
        cv2.imshow("Capturing", frame)
        k = cv2.waitKey(1)
        if not os.path.exists(path):
            os.makedirs(path)
        img_name = "anh_{}.png".format(img_counter)

        cv2.imwrite(os.path.join(path, img_name), frame)
        print("{} written!".format(img_name))    
        time.sleep(1)
    print("Done")
    break

cam.release()

cv2.destroyAllWindows()