<<<<<<< HEAD

import cv2
import mediapipe as mp
import pyautogui
import time
import os,sys


PPT_FILE_PATH = r"C:\Users\leston\Downloads\EV analysis.pptx"

hand=mp.solutions.hands
drawing=mp.solutions.drawing_utils
hands=hand.Hands(static_image_mode=False, max_num_hands=1,min_detection_confidence=0.7,min_tracking_confidence=0.7)
cap = cv2.VideoCapture(0)
previous_finger_count= 0
last_gesture_time= 0
gesture_cooldown=0.5

def count_fingers(hand_landmarks):
    finger_tips=[4,8,12,16,20] 
    finger_joints=[3,6,10,14,18]
    fingers_up=0

    # thumb_tip = hand_landmarks.landmark[finger_tips[0]]
    # thumb_pip = hand_landmarks.landmark[finger_pips[0]]
    # if thumb_tip.x < thumb_pip.x:
    #     fingers_up += 1
    for i in range(1, 5):
        tip=hand_landmarks.landmark[finger_tips[i]]
        joint=hand_landmarks.landmark[finger_joints[i]]
        if tip.y<joint.y:  
            fingers_up += 1
    return fingers_up
def open_powerpoint(file_path):
    if not os.path.exists(file_path):
        print("patth wrong")
        return False
    os.startfile(file_path)
    time.sleep(1)
    pyautogui.click()
    pyautogui.press('f5')
    time.sleep(2)
    return True
print("1 Previous Slide")
print(" 2 FINGERS Next Slide")
print("Press 'q'to quit")
if not open_powerpoint(PPT_FILE_PATH):
    print("error")
    sys.exit(1)
while True:
    success, frame = cap.read()
    if not success:
        print("fail")
        break
    # frame = cv2.flip(frame, 1)
#convert to bgr to rgb
    rgb=cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
    results=hands.process(rgb)
    current_time=time.time()
    gesture=None
    finger_count=0
    
    #main part
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            #not requierd only for visiblity
            drawing.draw_landmarks(
                frame,hand_landmarks,hand.HAND_CONNECTIONS)
            finger_count=count_fingers(hand_landmarks)
            if current_time-last_gesture_time>gesture_cooldown:
                if finger_count==1 and previous_finger_count!=1:
                    gesture='previous'
                    pyautogui.press('left')  
                    print("previous")
                    last_gesture_time=current_time
                    previous_finger_count=finger_count
                elif finger_count==2 and previous_finger_count!=2:
                    pyautogui.press('right') 
                    print("next")
                    last_gesture_time=current_time
                    previous_finger_count=finger_count
                # rests wehn diff fing count shown
                elif finger_count!=1 and finger_count!=2:
                    previous_finger_count=0
                    last_gesture_time=current_time

    else:
        #it rests when there is no hand detected 
        previous_finger_count = 0
    
    # Display information on screen
    # Background rectangle for better visibility
    # overlay = frame.copy()
    # cv2.rectangle(overlay, (0, 0), (400, 150), (0, 0, 0), -1)
    # cv2.addWeighted(overlay, 0.6, frame, 0.4, 0, frame)
    
    # if results.multi_hand_landmarks:
    #     # Show finger count
    #     cv2.putText(frame, f"Fingers: {finger_count}", (10, 40), 
    #                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        
    #     # Show action
    #     if finger_count == 1:
    #         cv2.putText(frame, "Action: PREVIOUS", (10, 80), 
    #                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 0), 2)
    #     elif finger_count == 2:
    #         cv2.putText(frame, "Action: NEXT", (10, 80), 
    #                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 0), 2)
    #     else:
    #         cv2.putText(frame, "Action: None", (10, 80), 
    #                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (128, 128, 128), 2)
    
    # cv2.putText(frame, "Press 'q' to quit", (10, frame.shape[0] - 20), 
    #            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1)
    cv2.imshow("frame",frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
# cap.release()
# cv2.destroyAllWindows()
# hands.close()
=======

import cv2
import mediapipe as mp
import pyautogui
import time
import os
import subprocess
import sys


PPT_FILE_PATH = r"C:\Users\leston\Desktop\TIme series Final ppt.pptx"

mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7
)

# Initialize webcam
cap = cv2.VideoCapture(0)

# Variables for gesture control
previous_finger_count = 0
last_gesture_time = 0
gesture_cooldown = 0.5  # Seconds between gestures

def count_fingers(hand_landmarks):
   
    finger_tips = [4, 8, 12, 16, 20] 
    finger_pips = [3, 6, 10, 14, 18]
    
    fingers_up = 0

    thumb_tip = hand_landmarks.landmark[finger_tips[0]]
    thumb_pip = hand_landmarks.landmark[finger_pips[0]]
    if thumb_tip.x < thumb_pip.x:  # Thumb is extended (left hand logic)
        fingers_up += 1
    
    # Other four fingers (check if tip is above pip joint)
    for i in range(1, 5):
        tip = hand_landmarks.landmark[finger_tips[i]]
        pip = hand_landmarks.landmark[finger_pips[i]]
        
        if tip.y < pip.y:  # Finger tip is above pip joint
            fingers_up += 1
    
    return fingers_up

def open_powerpoint(file_path):
    """
    Open PowerPoint file and start slideshow
    """
    if not os.path.exists(file_path):
        print(f"ERROR: PowerPoint file not found at: {file_path}")
        print("Please update the PPT_FILE_PATH variable in the script.")
        return False
    
    try:
        print(f"Opening PowerPoint: {file_path}")
        
        # Open the file
        os.startfile(file_path)
        
        # Wait for PowerPoint to open
        print("Waiting for PowerPoint to open...")
        time.sleep(5)
        
        # Start slideshow (F5)
        print("Starting slideshow...")
        time.sleep(1)
        pyautogui.press('f5')
        time.sleep(2)
        
        print("✓ PowerPoint slideshow started!")
        return True
        
    except Exception as e:
        print(f"ERROR opening PowerPoint: {e}")
        return False

# Main program
print("=" * 50)
print("Hand Gesture PowerPoint Controller")
print("=" * 50)
print("\nControls:")
print("  👆 1 FINGER  → Previous Slide")
print("  ✌️  2 FINGERS → Next Slide")
print("  Press 'q' to quit")
print("=" * 50)

# Open PowerPoint file
if not open_powerpoint(PPT_FILE_PATH):
    print("error")
   
    sys.exit(1)

while True:
    success, frame = cap.read()
    if not success:
        print("Failed to read from camera")
        break
    
    # Flip frame horizontally for mirror effect
    frame = cv2.flip(frame, 1)
    
    # Convert to RGB for MediaPipe
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    
    # Process the frame
    results = hands.process(rgb_frame)
    
    current_time = time.time()
    gesture_detected = None
    finger_count = 0
    
    # If hands are detected
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            # Draw hand landmarks
            mp_drawing.draw_landmarks(
                frame, 
                hand_landmarks, 
                mp_hands.HAND_CONNECTIONS,
                mp_drawing.DrawingSpec(color=(0, 255, 0), thickness=2, circle_radius=2),
                mp_drawing.DrawingSpec(color=(255, 255, 255), thickness=2)
            )
            
            # Count fingers
            finger_count = count_fingers(hand_landmarks)
            
            # Only trigger action when finger count CHANGES and cooldown has passed
            if current_time - last_gesture_time > gesture_cooldown:
                if finger_count == 1 and previous_finger_count != 1:
                    gesture_detected = 'previous'
                    pyautogui.press('left')  # Previous slide
                    print("◀ Previous Slide (1 finger)")
                    last_gesture_time = current_time
                    previous_finger_count = finger_count
                    
                elif finger_count == 2 and previous_finger_count != 2:
                    gesture_detected = 'next'
                    pyautogui.press('right')  # Next slide
                    print("▶ Next Slide (2 fingers)")
                    last_gesture_time = current_time
                    previous_finger_count = finger_count
                
                # Reset previous finger count when showing different number
                elif finger_count != 1 and finger_count != 2:
                    previous_finger_count = 0
    else:
        # Reset when no hand is detected
        previous_finger_count = 0
    
    # Display information on screen
    # Background rectangle for better visibility
    overlay = frame.copy()
    cv2.rectangle(overlay, (0, 0), (400, 150), (0, 0, 0), -1)
    cv2.addWeighted(overlay, 0.6, frame, 0.4, 0, frame)
    
    if results.multi_hand_landmarks:
        # Show finger count
        cv2.putText(frame, f"Fingers: {finger_count}", (10, 40), 
                   cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        
        # Show action
        if finger_count == 1:
            cv2.putText(frame, "Action: PREVIOUS", (10, 80), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 0), 2)
        elif finger_count == 2:
            cv2.putText(frame, "Action: NEXT", (10, 80), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 0), 2)
        else:
            cv2.putText(frame, "Action: None", (10, 80), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.8, (128, 128, 128), 2)
        
        # Show gesture feedback
        if gesture_detected:
            action_text = "◀ PREVIOUS SLIDE" if gesture_detected == 'previous' else "▶ NEXT SLIDE"
            cv2.putText(frame, action_text, (10, 120), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
    else:
        cv2.putText(frame, "No hand detected", (10, 40), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)
        cv2.putText(frame, "Show your hand!", (10, 80), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)
    
    # Display instructions at bottom
    cv2.putText(frame, "Press 'q' to quit", (10, frame.shape[0] - 20), 
               cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1)
    
    # Show the frame
    cv2.imshow('Hand Gesture PPT Control', frame)
    
    # Break loop with 'q' key
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Cleanup
cap.release()
cv2.destroyAllWindows()
hands.close()
print("\n" + "=" * 50)
print("Program ended.")
print("=" * 50)
>>>>>>> 925a7363a449d56ef1fed634595f459bf6f85d20
