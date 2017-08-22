import cv2
import sys

cascPath = sys.argv[1]
cascPath_2 = sys.argv[2]
faceCascade = cv2.CascadeClassifier(cascPath)
soccerCascade = cv2.CascadeClassifier(cascPath_2)

video_capture = cv2.VideoCapture(0)

while True:
    # Capture frame-by-frame
    ret, frame = video_capture.read()

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = faceCascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=4,
        minSize=(22, 22),
        flags=cv2.CASCADE_SCALE_IMAGE
    )
    soccers = soccerCascade.detectMultiScale(
	gray,
	scaleFactor=1.1,    
	minNeighbors=4,
	minSize=(22,22),
	flags=cv2.CASCADE_SCALE_IMAGE
    )
    # Draw a rectangle around the faces
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
    for (x, y, w, h) in soccers:
	cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
    # Display the resulting frame
    cv2.imshow('Video', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything is done, release the capture
video_capture.release()
cv2.destroyAllWindows()
