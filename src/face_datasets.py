import cv2
import os
import json
import time
# import RPi.GPIO as GPIO

# from signal import signal, SIGTERM, SIGHUP
# from rpi_lcd import LCD
# lcd = LCD()

# def safe_exit(signum, frame):
#     exit(1)

# GPIO.setmode(GPIO.BCM)
# GPIO.setwarnings(False)
# GPIO.setup(18,GPIO.OUT)

# Detect object in video stream using Haarcascade Frontal Face
face_detector = cv2.CascadeClassifier(
    'src/cascades/data/haarcascade_frontalface_default.xml')

# For each person, one face id
face_id = 9

# Initialize sample face image
count = 0

# Value returned from the ESP-01
input_string = "130246Shodipo Gideon"
print(input_string)

matric_num = input_string[0:6]

# Start capturing video
vid_cam = cv2.VideoCapture(0)

# Save the input data from ESP-01 into a text file in Json Form so as to be accesible in future
dictionary_data = {}
dictionary_data['Matric No'] = input_string[0:6]  # assume this is a a string
dictionary_data['Fullname'] = input_string[6:]

with open('C:/Users/ola/Downloads/Oba videos/OpenCV-Face-Recognition-Python/src/store.txt', 'r+') as sf:
    if len(sf.read()) == 0:
        sf.write(json.dumps(dictionary_data, indent=2))
    else:
        sf.write(',\n' + json.dumps(dictionary_data, indent=2))
        sf.close()

# Parent Directory path
parent_dir = "C:/Users/ola/Downloads/Oba videos/OpenCV-Face-Recognition-Python/src/images/"

# define Buzzer function


def Buzz():
    for x in range(3):
        # GPIO.output(18,GPIO.HIGH)
        print("Make Sound")
        time.sleep(1)
        # GPIO.output(18,GPIO.LOW)
        print("Keep Quiet")
        time.sleep(1)
    return


if (matric_num != ""):
    # Display on LCD "Enrolling New Face"
    # signal(SIGTERM, safe_exit)
    # signal(SIGHUP, safe_exit)
    # lcd.text("Enrolling New Face,", 1)
    # lcd.text("Initializing...", 2)
    # # Buzzer Sounds 5times at {500ms interval}
    # Buzz()
    # lcd.clear()
    # # Display on LCD "Place Image Before The Camera"
    # lcd.text("Scanning...", 1)
    # lcd.text("Place your face", 2)

    # def create_dir(matric_num):
    if not os.path.isdir(matric_num):
        # Create a folder with the student's Matric Number
        path = os.path.join(parent_dir, matric_num)
        os.mkdir(path)
        print(matric_num, " created Successfully!")
    else:
        print("Folder Already Existed")

    # Change your route to the folder directory
    os.chdir(path)
    print(path)

    # Line of code to Start Camera and Take Pictures
    # Start looping
    while(True):

        # Capture video frame
        _, image_frame = vid_cam.read()

        # Convert frame to grayscale
        gray = image_frame

        # Detect frames of different sizes, list of faces rectangles
        faces = face_detector.detectMultiScale(gray, 1.3, 5)

        # Loops for each faces
        for (x, y, w, h) in faces:

            # Crop the image frame into rectangle
            cv2.rectangle(image_frame, (x, y), (x+w, y+h), (255, 0, 0), 2)

            # Increment sample face image
            count += 1

            # Save the captured image into the datasets folder
            # cv2.imwrite("User." + str(face_id) + '.' + str(count) + ".jpg", gray[y:y+h, x:x+w])

            cv2.imwrite(str(count) + ".jpg", gray[y:y+h, x:x+w])
            # Display the video frame, with bounded rectangle on the person's face
            cv2.imshow('frame', image_frame)

        # To stop taking video, press 'q' for at least 100ms
        if cv2.waitKey(100) & 0xFF == ord('q'):
            break

        # If image taken reach 100, stop taking video
        elif count > 200:
            break

        # Stop video
    vid_cam.release()

    # Close all started windows
    cv2.destroyAllWindows()

    # Clear Matric Number
    matric_num == ""

    # # Display on LCD "Successfully Enrolled Student_Name"
    # lcd.text("Done!", 1)
    # lcd.text("Enroll Successful!", 2)
    # time.sleep(3)
    # lcd.clear()
