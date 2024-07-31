import face_recognition
import cv2 as cv
import numpy as np
import os

video_capture = cv.VideoCapture(0)

encoding_list = [] # Contains face encodings in HOG patterns
teacher_name_list = [] # Contains a list of names 
face_locations = []
face_encodings = []
face_names = []
process_this_frame = True # Allows to process everyother frame for FPS
count = 0
attendance = []

# Will load and add names to lists
for filename in os.listdir("teacher_photos"):
    if filename.endswith(".jpg"):  # Adjust extension if needed
        encoding_list.append(face_recognition.face_encodings(face_recognition.load_image_file("teacher_photos/" + filename))[0])
        teacher_name_list.append(filename[:-4])

while True:
    
    print(attendance)
    # Grab a single frame of video
    ret, frame = video_capture.read()

    video_capture.set(cv.CAP_PROP_FOURCC, cv.VideoWriter_fourcc('M', 'J', 'P', 'G'))
    video_capture.set(cv.CAP_PROP_FPS, 30)
    fps = int(video_capture.get(5))
    print("fps:", fps)

    # Only process every other frame of video to save time
    if process_this_frame:
        # Resize frame of video to 1/4 size for faster face recognition processing
        small_frame = cv.resize(frame, (0, 0), fx=0.25, fy=0.25)

        # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
        rgb_small_frame = small_frame[:, :, ::-1]
        
        # Find all the faces and face encodings in the current frame of video
        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

        face_names = []
        for face_encoding in face_encodings:
            # See if the face is a match for the known face(s)
            matches = face_recognition.compare_faces(encoding_list, face_encoding)
            name = "Unknown"

            # # If a match was found in encoding_list, just use the first one.
            # if True in matches:
            #     first_match_index = matches.index(True)
            #     name = teacher_name_list[first_match_index]

            # Or instead, use the known face with the smallest distance to the new face
            
            # Implement New Code Here
            face_distances = face_recognition.face_distance(encoding_list, face_encoding)
            best_match_index = np.argmin(face_distances)
            if matches[best_match_index]:
                name = teacher_name_list[best_match_index]
                count += 1
                if count >= 60:
                    count = 0;
                    attendance.append(name)
                    
            else: 
                count = 0

            face_names.append(name)

    process_this_frame = not process_this_frame


    # Display the results
    for (top, right, bottom, left), name in zip(face_locations, face_names):
        # Scale back up face locations since the frame we detected in was scaled to 1/4 size
        top *= 4
        right *= 4
        bottom *= 4
        left *= 4

        # Draw a box around the face
        cv.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

        # Draw a label with a name below the face
        cv.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv.FILLED)
        font = cv.FONT_HERSHEY_DUPLEX
        cv.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

    # Display the resulting image
    cv.imshow('Video', frame)

    # Hit 'q' on the keyboard to quit!
    if cv.waitKey(1) & 0xFF == ord('q'):
        break

# Release handle to the webcam
video_capture.release()
cv.destroyAllWindows()

