import cv2 as cv;
import face_recognition

img = cv.imread('teacher_photos/Eric-Berngen-240x300.jpg')

rgb = cv2.cvtColor(img, cv2.COLORBGR2RGB)

img_encode = face_recognition.face_encodings(rgb)[0]

cv.imshow('Cat', img)

cv.waitKey(0)