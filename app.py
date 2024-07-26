from flask import Flask, render_template, Response
import cv2
import face_recognition
import numpy as np
import os

app = Flask(__name__)

# Initialize video capture
video_capture = cv2.VideoCapture(0)

# Load teacher images and encodings
teacher_list = []
encoding_list = []
teacher_name_list = []

for filename in os.listdir("teacher_photos"):
    if filename.endswith(".jpg"):  # Adjust extension if needed
        teacher_list.append(face_recognition.load_image_file("teacher_photos/" + filename))

for filename in os.listdir("teacher_photos"):
    if filename.endswith(".jpg"):  # Adjust extension if needed
        teacher_name_list.append(filename[:-4])

for teacher in teacher_list:
    encoding_list.append(face_recognition.face_encodings(teacher)[0])

# Initialize some variables
face_locations = []
face_encodings = []
face_names = []
process_this_frame = True

count = 0

attendance = []

def generate_frames():
    global process_this_frame, face_locations, face_encodings, face_names, count, attendance

    while True:
        success, frame = video_capture.read()
        if not success:
            break
        else:
            # Only process every other frame of video to save time
            if process_this_frame:
                # Resize frame of video to 1/4 size for faster face recognition processing
                small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

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

                    # Or instead, use the known face with the smallest distance to the new face
                    face_distances = face_recognition.face_distance(encoding_list, face_encoding)
                    best_match_index = np.argmin(face_distances)
                    if matches[best_match_index]:
                        name = teacher_name_list[best_match_index]
                        count += 1
                        if count >= 60:
                            count = 0
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
                cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

                # Draw a label with a name below the face
                cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
                font = cv2.FONT_HERSHEY_DUPLEX
                cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

            # Encode the frame as JPEG
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()

            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
