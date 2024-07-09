import cv2
import time

def detect_eyes():
    # Load the Haar cascade file for eye detection
    eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')

    # Start video capture from the webcam
    cap = cv2.VideoCapture(0)

    while True:
        # Read a frame from the video capture
        ret, frame = cap.read()
        
        # Convert the frame to grayscale
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        # Detect eyes in the image for 3 seconds
        eyes = eye_cascade.detectMultiScale(gray, 1.1, 4)
        if(len(eyes)>0):
            delay=0
            while delay!=(3):
                eyes = eye_cascade.detectMultiScale(gray, 1.1, 4)
                if(len(eyes)>0):
                    time.sleep(1)
                    delay+=1
                else:
                    break
            if(delay==3):
                # print("detected baby")
                cap.release()
                cv2.destroyAllWindows()
                return "Detected"
                
        # Draw rectangles around the eyes
        # for (x, y, w, h) in eyes:
        #     # cv2.putText(frame, 'Eyes Detected', (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (36,255,12), 2)
        #     cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
        
        # # # Display the frame
        # cv2.imshow('Eye Detection', frame)
        
        # # Break the loop when the 'q' key is pressed
        # if cv2.waitKey(1) & 0xFF == ord('q'):
        #     break

    # Release the VideoCapture object and close the windows
    cap.release()
    cv2.destroyAllWindows()
    
detect_eyes()