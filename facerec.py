# facerec.py
import cv2, sys, numpy, os
import serial
from time import sleep

size = 4
fn_haar = 'haarcascade_frontalface_default.xml'
fn_dir = 'att_faces'
fn_name = sys.argv[1]

# Part 1: Create fisherRecognizer
print('Training...')
# Create a list of images and a list of corresponding names
(images, lables, names, id) = ([], [], {}, 0)
for (subdirs, dirs, files) in os.walk(fn_dir):
    for subdir in dirs:
        names[id] = subdir
        subjectpath = os.path.join(fn_dir, subdir)
        for filename in os.listdir(subjectpath):
            path = subjectpath + '/' + filename
            lable = id
            images.append(cv2.imread(path, 0))
            lables.append(int(lable))
        id += 1
(im_width, im_height) = (112, 92)

# Create a Numpy array from the two lists above
(images, lables) = [numpy.array(lis) for lis in [images, lables]]

# OpenCV trains a model from the images
# NOTE FOR OpenCV2: remove '.face'
model = cv2.createFisherFaceRecognizer()
model.train(images, lables)

# Part 2: Use fisherRecognizer on camera stream
haar_cascade = cv2.CascadeClassifier(fn_haar)
webcam = cv2.VideoCapture(0)

# added

servoTiltPos = 90
servoPanPos = 90
servoStep = 1

ser = serial.Serial('/dev/ttyACM0', 9600)

# end added

while True:
    (rval, frame) = webcam.read()
    frame=cv2.flip(frame,1,0)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    mini = cv2.resize(gray, (gray.shape[1] / size, gray.shape[0] / size))

    # added

    midScreenX = (gray.shape[1] / size) / 2
    midScreenY = (gray.shape[0] / size) / 2
    tolX = 0.1 * (gray.shape[1] / size)
    tolY = 0.1 * (gray.shape[0] / size)

    # end added

    faces = haar_cascade.detectMultiScale(mini)
    for i in range(len(faces)):
        face_i = faces[i]
        (x, y, w, h) = [v * size for v in face_i]
        face = gray[y:y + h, x:x + w]
        face_resize = cv2.resize(face, (im_width, im_height))

        # Try to recognize the face
        prediction = model.predict(face_resize)
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 3)

        # Write the name of recognized face
        # [1]
        # attempt unknown

        if prediction[1]<400:
            cv2.putText(frame,
            '%s - %.0f' % (names[prediction[0]],prediction[1]),
            (x-10, y-10), cv2.FONT_HERSHEY_PLAIN,1,(0, 255, 0))
        else:
            cv2.putText(frame,
            'Unknown',
            (x-10, y-10), cv2.FONT_HERSHEY_PLAIN,1,(0, 255, 0))

        # end attempt unknown
        # cv2.putText(frame,
        #     '%s - %.0f' % (names[prediction[0]],prediction[1]),
        #     (x-10, y-10), cv2.FONT_HERSHEY_PLAIN,1,(0, 255, 0))

        if (names[prediction[0]] == fn_name):

            # added, servo

            midFaceX = face_i[0] + (face_i[2] / 2)
            midFaceY = face_i[1] + (face_i[3] / 2)

            # print("midFaceX = " + str(midFaceX))
            # print("midScreenX = " + str(midScreenX))
            # print("midScreenX - tol = " + str(midScreenX - tolX))
            #
            # print("midFaceY = " + str(midFaceY))
            # print("midScreenY = " + str(midScreenY))
            # print("midScreenY - tol = " + str(midScreenY - tolY))

            # Check face position in relation to screen mid
            if midFaceY < midScreenY - tolY:
                if servoTiltPos <= 175:
                    servoTiltPos += servoStep
            elif midFaceY > midScreenY + tolY:
                if servoTiltPos >= 5:
                    servoTiltPos -= servoStep
            if midFaceX < midScreenX - tolX:
                if servoPanPos <= 175:
                    servoPanPos += servoStep
            elif midFaceX > midScreenX + tolX:
                if servoPanPos >= 5:
                    servoPanPos -= servoStep

            print('Tilt pos' + str(servoTiltPos))
            print('Pan pos' + str(servoPanPos))
            ser.write('t'+str(servoTiltPos)+'\n')
            ser.write('p'+str(servoPanPos)+'\n')
            sleep(0.1)

            # end, servo

    cv2.imshow('OpenCV', frame)
    key = cv2.waitKey(10)
    if key == 27:
        break
