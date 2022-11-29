import time
import os
import cv2
from VideoGet import VideoGet
from VideoShow import VideoShow
import face_recognition
def imgProcess(frame, img_counter,  path):
    if not os.path.exists(path):
        os.makedirs(path)
    img_name = "anh_{}.png".format(img_counter)
    faceInfos = face_recognition.face_locations(frame)
    for faceInfo in faceInfos:

    # Print the location of each face in this image
        top, right, bottom, left = faceInfo
        face_image = frame[top:bottom, left:right]
        cv2.imwrite(os.path.join(path, img_name), face_image)
        img_reload = cv2.imread(os.path.join(path, img_name))
        cv2.imwrite(os.path.join(path, img_name),cv2.resize(img_reload, dsize=(160, 160), interpolation=cv2.INTER_CUBIC))

    cv2.putText(frame, "{:.0f} image(s)".format(img_counter),
        (10, 450), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255, 255, 255))
    return frame

def threadBoth(source, path):
    """
    Dedicated thread for grabbing video frames with VideoGet object.
    Dedicated thread for showing video frames with VideoShow object.
    Main thread serves only to pass frames between VideoGet and
    VideoShow objects/threads.
    """

    video_getter = VideoGet(source).start()
    video_shower = VideoShow(video_getter.frame).start()
    img_counter = 1
    while True:
        if video_getter.stopped or video_shower.stopped:
            video_shower.stop()
            video_getter.stop()
            break

        frame = video_getter.frame
        video_shower.frame = frame
        frame = imgProcess(frame, img_counter, path)
        time.sleep(1)
        img_counter += 1
        if (img_counter >40): break
    video_shower.stop()
    video_getter.stop()

ur_name = input('Enter your name: ')
path = './Dataset/FaceData/raw/{}'.format(ur_name)
threadBoth(0,path)
