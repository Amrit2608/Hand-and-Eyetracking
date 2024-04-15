import cv2
import mediapipe as mp
import pygame 
import time

mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands

# Set up video capture
cap = cv2.VideoCapture(0)

# Define the width and height of the frame

width = 1140
height = 740

# Set the resolution of the webcam
cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)

pygame.init()
pygame.mixer.music.load("F:/amrit song/01 - Tujh Mein Rab Dikhta Hai-(MyMp3Singer.com).mp3")



def play():
     pygame.mixer.music.play()

def pause():
     pygame.mixer.music.pause()

def unpause():
    pygame.mixer.music.unpause()


# Setup finger visibility timer
visible_timer = None




# Initialize hand tracking
with mp_hands.Hands(
    max_num_hands=2, min_detection_confidence=0.5, min_tracking_confidence=0.5
) as hands:
    while True:
        # Read frame from webcam
        ret, frame = cap.read()

        # Resize the frame to the desired size
        frame = cv2.resize(frame, (width, height))

        # Flip the frame horizontally for natural movement
        frame = cv2.flip(frame, 1)

        # Convert frame to RGB for MediaPipe
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Detect hands in the frame
        results = hands.process(frame_rgb)

        # Draw hand landmarks on the frame
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                mp_drawing.draw_landmarks(
                    frame,
                    hand_landmarks,
                    mp_hands.HAND_CONNECTIONS,
                    mp_drawing.DrawingSpec(color=(0, 0, 255), thickness=2, circle_radius=2),
                    mp_drawing.DrawingSpec(color=(0, 255, 0), thickness=2, circle_radius=2),
                )

                # Count the number of fingers shown

                if hand_landmarks.landmark[5].x < hand_landmarks.landmark[17].x: # Right hand
                    
                  tip_ids = [8, 12, 16, 20]
                  
                  finger_count = sum(
                     1 for i, lm in enumerate(hand_landmarks.landmark)
                     if i in tip_ids and lm.y < hand_landmarks.landmark[i - 2].y
                  )

                  if hand_landmarks.landmark[4].x < hand_landmarks.landmark[5].x:
                     finger_count = finger_count+1




                  cv2.putText(
                    frame,
                    f"Right hand Count: {finger_count}",
                    (850, 30),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1,
                    (0, 250, 0),
                    2,
                    cv2.LINE_AA,
                   )

                else: # Left hand
                    
                  tip_ids = [8, 12, 16, 20]

                  finger_count = sum(
                  1 for i, lm in enumerate(hand_landmarks.landmark)
                  if i in tip_ids and lm.y < hand_landmarks.landmark[i - 2].y
                  )

                  if hand_landmarks.landmark[4].x > hand_landmarks.landmark[5].x:
                     finger_count = finger_count+1
                
                  
                  cv2.putText(
                    frame,
                    f"Left Hand Count: {finger_count}",
                    (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1,
                    (0, 250, 0),
                    2,
                    cv2.LINE_AA,
                   )
                  


            #  Gesture control

                if finger_count == 2:
                    # Start timer if two fingers are visible for the first time
                    if visible_timer is None:
                        visible_timer = time.time()
                    # Check if two fingers have been visible for at least 1 seconds
                    elif time.time() - visible_timer >= 0.4:
                        play()
                    

                # Reset timer if two fingers are not visible
                elif finger_count == 3:
                    if visible_timer is None:
                        visible_timer = time.time()
                    # Check if two fingers have been visible for at least 1 seconds
                    elif time.time() - visible_timer >= 0.4:
                        pause()
                    
                elif finger_count == 4:
                    if visible_timer is None:
                        visible_timer = time.time()
                    # Check if two fingers have been visible for at least 1 seconds
                    elif time.time() - visible_timer >= 0.4:
                        unpause()

                else:    
                    visible_timer = None


                
               
                ids = [8, 16, 20]

                # for i, lm in enumerate(hand_landmarks.landmark[8,16,20]):
                if hand_landmarks.landmark[8].y > hand_landmarks.landmark[6].y and hand_landmarks.landmark[16].y > hand_landmarks.landmark[14].y and hand_landmarks.landmark[20].y > hand_landmarks.landmark[18].y and hand_landmarks.landmark[10].y > hand_landmarks.landmark[12].y:
                      cv2.putText(
                            frame,
                            f"Fuck You",
                            (400, 300),
                            cv2.FONT_HERSHEY_SIMPLEX,
                            3,
                            (0, 0, 255),
                            4,
                            cv2.LINE_AA,
                        )
                      
                  
                    
            

                # # Display the finger count on the frame
                # cv2.putText(
                #     frame,
                #     f"Finger Count: {finger_count}",
                #     (10, 30),
                #     cv2.FONT_HERSHEY_SIMPLEX,
                #     1,
                #     (0, 255, 0),
                #     2,
                #     cv2.LINE_AA,
                # )

        # Display the frame
        cv2.imshow("Hand Tracking", frame)


        

        # Exit on 'q' press
        if cv2.waitKey(1) == ord("q"):
            break

# Release the capture and destroy windows
cap.release()
cv2.destroyAllWindows()
