
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
