import face_recognition
import cv2
import numpy as np
import winsound
import smtplib

flag = 0
sender = input(str("Please enter sender's email: "))
receiver = input(str("Please enter receiver's email: "))
password = input(str("Please enter your password: "))



# Get a reference to webcam #0 (the default one)
video_capture = cv2.VideoCapture(0)

# Load a sample picture and learn how to recognize it.
obama_image = face_recognition.load_image_file("homeSurvilance/obama.jpg")
obama_face_encoding = face_recognition.face_encodings(obama_image)[0]

# Load a second sample picture and learn how to recognize it.
biden_image = face_recognition.load_image_file("homeSurvilance/biden.jpg")
biden_face_encoding = face_recognition.face_encodings(biden_image)[0]

# Load a third sample picture and learn how to recognize it.
rk_image = face_recognition.load_image_file("homeSurvilance/rk.jpg")
rk_face_encoding = face_recognition.face_encodings(rk_image)[0]

# Load a fourth sample picture and learn how to recognize it.
prof_image = face_recognition.load_image_file("homeSurvilance/prof.jpg")
prof_face_encoding = face_recognition.face_encodings(prof_image)[0]


# Create arrays of known face encodings and their names
known_face_encodings = [
    obama_face_encoding,
    biden_face_encoding,
    rk_face_encoding,
    prof_face_encoding
]
known_face_names = [
    "Barack Obama",
    "Joe Biden",
    "Ahmed",
    "Prof. Mohammed Elmorsy"
]

while True:
    # Grab a single frame of video
    ret, frame = video_capture.read()
    ret, frame2 = video_capture.read()

    # ------------- movement ---------------------
    diff = cv2.absdiff(frame, frame2)
    gray = cv2.cvtColor(diff, cv2.COLOR_RGB2GRAY)  # color values will generate some error
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    _, thresh = cv2.threshold(blur, 20, 255, cv2.THRESH_BINARY)  # removing noise
    dilated = cv2.dilate(thresh, None, iterations=3)  # selecting our point of attention after removing noise
    countours, _ = cv2.findContours(dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)  # bounding box
    # cv2.drawContours(frame1, countours, -1, (255,0,0), 2)
    # ------------- movement ---------------------




    # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
    rgb_frame = frame[:, :, ::-1]

    # Find all the faces and face enqcodings in the frame of video
    face_locations = face_recognition.face_locations(rgb_frame)
    face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

    # Loop through each face in this frame of video
    for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
        # See if the face is a match for the known face(s)
        matches = face_recognition.compare_faces(known_face_encodings, face_encoding)

        name = "Unknown"

        # If a match was found in known_face_encodings, just use the first one.
        # if True in matches:
        #     first_match_index = matches.index(True)
        #     name = known_face_names[first_match_index]

        # Or instead, use the known face with the smallest distance to the new face
        face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
        best_match_index = np.argmin(face_distances)
        if matches[best_match_index]:
            name = known_face_names[best_match_index]


        # Draw a box around the face
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)

        # Draw a label with a name below the face
        cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 255, 0), cv2.FILLED)
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

    for c in countours:
        if cv2.contourArea(c) < 5000 or known_face_names == True:
            continue
        x, y, w, h = cv2.boundingRect(c)
        cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
        winsound.Beep(500, 200)
        # winsound.PlaySound('alert.wav', winsound.SND_ASYNC)
        flag += 1   # every beep count
        if(flag == 20):

            message = "This email was sent by our security system. There might be someone/something moving" \
                      " in your room. " \
                      "Please check the video and ensure your safety. Thank you."

            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(sender, password)
            print("login successful")
            server.sendmail(sender, receiver, message)
            print("Email has been sent to ", receiver)

        # if cv2.contourArea(c) < 5000:
        #     continue



    # Display the resulting image
    cv2.imshow('MyCam', frame)

    # Hit 'q' on the keyboard to quit!
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release handle to the webcam
video_capture.release()
cv2.destroyAllWindows()