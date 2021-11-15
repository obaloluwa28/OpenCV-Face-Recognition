import numpy as np
import cv2
import pickle

# from signal import signal, SIGTERM, SIGHUP
# from rpi_lcd import LCD
# lcd = LCD()

# def safe_exit(signum, frame):
#     exit(1)

count = 0

recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read("src/recognizers/face-trainner.yml")

# face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'src/cascades/data/haarcascade_frontalface_alt2.xml')
face_cascade = cv2.CascadeClassifier(
    'src/cascades/data/haarcascade_frontalface_alt.xml')

labels = {"person_name": 1}
with open("src/pickles/face-labels.pickle", 'rb') as f:
    og_labels = pickle.load(f)
    labels = {v: k for k, v in og_labels.items()}

cap = cv2.VideoCapture(0)

while(True):

    # Capture frame-by-frame
    _, frame = cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    for (x, y, w, h) in faces:
        roi_gray = gray[y:y+h, x:x+w]  # (ycord_start, ycord_end)
        roi_color = frame[y:y+h, x:x+w]
        # recognize? deep learned model predict keras tensorflow pytorch scikit learn
        id_, conf = recognizer.predict(roi_gray)
        if conf >= 4 and conf <= 85:
            print("id:", id_)
            print(labels[id_])
            font = cv2.FONT_HERSHEY_SIMPLEX
            name = labels[id_]
            color = (255, 255, 255)
            stroke = 2
            cv2.putText(frame, name, (x, y), font, 1,
                        color, stroke, cv2.LINE_AA)
        color = (255, 0, 0)  # BGR 0-255
        stroke = 2
        end_cord_x = x + w
        end_cord_y = y + h
        cv2.rectangle(frame, (x, y), (end_cord_x, end_cord_y), color, stroke)
        count += 1
    # Display the resulting frame
    cv2.imshow('frame', frame)
    if cv2.waitKey(20) & 0xFF == ord('q'):
        break
    if count > 5:
        # Display on LCD "Enrolling New Face"
        # signal(SIGTERM, safe_exit)
        # signal(SIGHUP, safe_exit)
        # lcd.text("Attendance Marked", 1)
        # lcd.text(name+"Present", 2)
        print("Final Label:", name)
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
