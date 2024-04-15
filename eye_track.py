import cv2
import numpy as np

cap = cv2.VideoCapture(0)

eye_cascade = cv2.CascadeClassifier('har_eye.xml')

while True:
    ret, frame = cap.read()
    
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    eyes = eye_cascade.detectMultiScale(gray, 1.3, 5)
    
    for (x, y, w, h) in eyes:
        eye_center = (x + w // 2, y + h // 2)
        cv2.circle(frame, eye_center, 3, (0, 255, 0), -1)
        
        face_center = (frame.shape[1] // 2, frame.shape[0] // 2)
        cv2.circle(frame, face_center, 3, (255, 0, 0), -1)
        
        gaze_direction = np.subtract(face_center, eye_center)
        gaze_direction = gaze_direction / np.linalg.norm(gaze_direction)
        gaze_direction = gaze_direction * 100
        
        cv2.line(frame, eye_center, tuple(eye_center + gaze_direction.astype(int)), (0, 0, 255), 2)
        
    cv2.imshow('Gaze Tracking', frame)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
        
cap.release()
cv2.destroyAllWindows()
