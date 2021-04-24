# import the necessary packages
# from pyimagesearch.motion_detection.singlemotiondetector import SingleMotionDetector
from sendemail import SendEmail
from flask import Response
from flask import Flask
from flask import render_template, request, session, url_for, redirect
import threading
import argparse
import imutils
import cv2
from flask_mysqldb import MySQL
import MySQLdb
import face_recognition
import numpy as np
import winsound


video_capture = cv2.VideoCapture(0)
# initialize the output frame and a lock used to ensure thread-safe
# exchanges of the output frames (useful when multiple browsers/tabs
# are viewing the stream)
outputFrame = None
lock = threading.Lock()
# initialize a flask object
app = Flask(__name__)

app.secret_key = "12345654321"

app.config["MYSQL_HOST"] = "127.0.0.1"
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = "Sandy@260593"
app.config["MYSQL_DB"] = "database_users"
db = MySQL(app)
# initialize the video stream and allow the camera sensor to
# warmup
# # vs = VideoStream(usePiCamera=1).start()
# time.sleep(2.0)

# Load a sample picture and learn how to recognize it.
obama_image = face_recognition.load_image_file("obama.jpg")
obama_face_encoding = face_recognition.face_encodings(obama_image)[0]

# Load a second sample picture and learn how to recognize it.
biden_image = face_recognition.load_image_file("biden.jpg")
biden_face_encoding = face_recognition.face_encodings(biden_image)[0]

# Load a third sample picture and learn how to recognize it.
rk_image = face_recognition.load_image_file("rk.jpg")
rk_face_encoding = face_recognition.face_encodings(rk_image)[0]

# Load a fourth sample picture and learn how to recognize it.
prof_image = face_recognition.load_image_file("prof.jpg")
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


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        if 'username' in request.form and 'password' in request.form:
            username = request.form['username']
            password = request.form['password']
            print(username, password)
            cursor = db.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute("SELECT * FROM table_users WHERE email=%s AND password=%s", (username, password))
            info = cursor.fetchone()
            if info is not None:
                if info["email"] == username and info["password"] == password:
                    session['loginsuccess'] = True
                    return redirect(url_for('home'))

            else:
                return redirect(url_for('register'))
    return render_template("login.html")


@app.route("/home")
def home():
    if session['loginsuccess']:
        return render_template('index.html')


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        if 'name' in request.form and 'username' in request.form and 'password' in request.form:
            name = request.form['name']
            username = request.form['username']
            password = request.form['password']
            print(name, username, password)
            cursor = db.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute("INSERT INTO database_users.table_users(Name,email,password)VALUES(%s,%s,%s)",
                           (name, username, password))
            db.connection.commit()
            return render_template('login.html')
    return render_template('register.html')


@app.route("/about")
def about():
    return render_template('about.html')


@app.route("/contact")
def contact():
    return render_template('contact.html')


def detect_motion():
    # grab global references to the video stream, output frame, and
    # lock variables
    global vs, outputFrame, lock, known_face_encodings, known_face_names, video_capture
    # initialize the motion detector and the total number of frames
    # read thus far
    se = SendEmail()
    total = 0
    flag = 0
    se = SendEmail()
    # loop over frames from the video stream
    while True:

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
            flag += 1  # every beep count
            if flag == 20:
                cv2.imwrite("screenshot.png", frame)
                se.sendmail()
        total += 1
        # acquire the lock, set the output frame, and release the
        # lock
        frame = imutils.resize(frame, 1130)
        with lock:
            outputFrame = frame.copy()


def generate():
    # grab global references to the output frame and lock variables
    global outputFrame, lock, known_face_encodings, known_face_names, video_capture
    # loop over frames from the output stream
    while True:
        # wait until the lock is acquired
        with lock:
            # check if the output frame is available, otherwise skip
            # the iteration of the loop
            if outputFrame is None:
                continue
            # encode the frame in JPEG format
            (flag, encodedImage) = cv2.imencode(".jpg", outputFrame)
            # ensure the frame was successfully encoded
            if not flag:
                continue
        # yield the output frame in the byte format
        yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' +
               bytearray(encodedImage) + b'\r\n')


@app.route("/video_feed")
def video_feed():
    # return the response generated along with the specific media
    # type (mime type)
    return Response(generate(),
                    mimetype="multipart/x-mixed-replace; boundary=frame")



# check to see if this is the main thread of execution
if __name__ == '__main__':
    # construct the argument parser and parse command line arguments\
    ap = argparse.ArgumentParser()
    ap.add_argument("-i", "--ip", type=str, required=True,
                    help="ip address of the device")
    ap.add_argument("-o", "--port", type=int, required=True,
                    help="ephemeral port number of the server (1024 to 65535)")
    args = vars(ap.parse_args())
    # start a thread that will perform motion detection
    t = threading.Thread(target=detect_motion, args=())
    t.daemon = True
    t.start()
    # start the flask app
    app.run(host=args["ip"], port=args["port"], debug=True,
            threaded=True, use_reloader=False)
# release the video stream pointer
video_capture.release()
