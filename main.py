import time
from collections import deque
import cv2
import mediapipe as mp
import numpy as np
from spotify_controller import SpotifyController


# ==== פרמטרים שאפשר לכוונן =====================================

COOLDOWN_SEC = 1.0      # זמן מינימלי בין פקודות Spotify
HISTORY_LEN = 5        # כמה פריימים משתמשים לרוב קולות על האיזור
SWIPE_THRESHOLD = 0.1
Fist_threshold = 0.1

# ================================================================

mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils


class HandRegionDetector:
    def __init__(self):
        self.hands = mp_hands.Hands(max_num_hands=1,min_detection_confidence=0.6,min_tracking_confidence=0.6,)

    def process_frame(self, frame):
        h, w, _ = frame.shape
        frame_flipped = cv2.flip(frame, 1)
        rgb = cv2.cvtColor(frame_flipped, cv2.COLOR_BGR2RGB)
        results = self.hands.process(rgb)

        text = "No hand detected"
        x_norm = None
        spread_y = None

        if results.multi_hand_landmarks:
            # take the first hand detected
            hand_landmarks = results.multi_hand_landmarks[0]

            # calculate the center of the hand and the maximum vertical diffenrences.
            xs = [lm.x for lm in hand_landmarks.landmark]
            ys = [lm.y for lm in hand_landmarks.landmark]
            cx = int(np.mean(xs) * w)
            cy = int(np.mean(ys) * h)
            x_norm = cx / w
            spread_y = np.max(ys) - np.min(ys)

            # visualization of the points and text
            mp_drawing.draw_landmarks(frame_flipped, hand_landmarks,mp_hands.HAND_CONNECTIONS)
            cv2.circle(frame_flipped, (cx, cy), 6, (0, 0, 255), -1)

            text = f"Spotify Hand Control"
            cv2.putText(frame_flipped, text, (20, 40),cv2.FONT_HERSHEY_SIMPLEX, 0.8,(255, 255, 255), 2)


        return frame_flipped, x_norm, spread_y 

    def close(self):
        self.hands.close()

def main():
        sp = SpotifyController()
        detector = HandRegionDetector()

        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            print("Could not open webcam")
            return

        last_action_time = 0.0
        last_action_text = ""
        last_x_values = deque(maxlen=HISTORY_LEN)
        last_spread_y = deque(maxlen=HISTORY_LEN)

        while True:
            ret, frame = cap.read()
            if not ret:
                break
            
            frame_vis, x_norm, spread_y  = detector.process_frame(frame)

            # אם זוהתה יד – נעדכן היסטוריה
            if x_norm is not None or spread_y is not None:
                last_x_values.append(x_norm)
                last_spread_y.append(spread_y)

                # צריך לפחות שני ערכים כדי לחשב תנועה
                if len(last_x_values) >= 2:
                    dx = last_x_values[-1] - last_x_values[0]
                    dy = last_spread_y[0] - last_spread_y[-1]
                    now = time.time()

                    if now - last_action_time > COOLDOWN_SEC:
                        
                        if dx > SWIPE_THRESHOLD:
                            sp.next_track()
                            last_action_text = "Next track (left => right)"
                            last_action_time = now
                            last_x_values.clear()

                        elif dx < -SWIPE_THRESHOLD:
                            sp.previous_track()
                            last_action_text = "Previous track (right => left)"
                            last_action_time = now
                            last_x_values.clear()

                        elif abs(dy) > Fist_threshold:
                            sp.toggle_play()
                            last_action_text = "Play/Pause"
                            last_action_time = now
                            last_spread_y.clear()
 
            else:
                last_x_values.clear()
                last_spread_y.clear()

            # plot the last command
            if last_action_text:
                cv2.putText(frame_vis, f"Last action: {last_action_text}",(20, 80),cv2.FONT_HERSHEY_SIMPLEX, 0.7,(0, 255, 255), 2)

            cv2.imshow("Hand Spotify control (MediaPipe)", frame_vis)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cap.release()
        detector.close()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
