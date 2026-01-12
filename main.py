import time
from collections import deque
import cv2
import mediapipe as mp
import numpy as np
from spotify_controller import SpotifyController


# ==== Paramters =================================================

COOLDOWN_SEC = 1.0      
HISTORY_LEN = 5       
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
        last_timestamps = deque(maxlen=HISTORY_LEN)

        while True:
            ret, frame = cap.read()
            if not ret:
                break
            
            frame_vis, x_norm, spread_y  = detector.process_frame(frame)

            scale_percent = 0.95 
            width = int(frame_vis.shape[1] * scale_percent)
            height = int(frame_vis.shape[0] * scale_percent)
            dim = (width, height)
            frame_resized = cv2.resize(frame_vis, dim, interpolation=cv2.INTER_AREA)

            # if hand detected change the last positions.
            if x_norm is not None and spread_y is not None:
                now = time.time()
                last_x_values.append(x_norm)
                last_spread_y.append(spread_y)
                last_timestamps.append(now)

                # we need to detect two positions to consider change
                if len(last_x_values) >= 2:
                    dx = last_x_values[-1] - last_x_values[0]
                    dy = last_spread_y[0] - last_spread_y[-1]
                    dt = last_timestamps[-1] - last_timestamps[0]
                    vx = dx / dt if dt > 0 else 0 
                    vy = dy / dt if dt > 0 else 0  

                    if now - last_action_time > COOLDOWN_SEC:
                        
                        if dx > SWIPE_THRESHOLD:
                            sp.next_track(dx=dx, vx=vx) 
                            last_action_text = f"Next track (vx: {vx:.2f})"
                            last_action_time = now
                            last_x_values.clear()
                            last_timestamps.clear()

                        elif dx < -SWIPE_THRESHOLD:
                            sp.previous_track(dx=dx, vx=vx)
                            last_action_text = f"Prev track (vx: {vx:.2f})"
                            last_action_time = now
                            last_x_values.clear()
                            last_timestamps.clear()

                        elif abs(dy) > Fist_threshold:
                            sp.toggle_play(dy=dy, vy=vy) 
                            last_action_text = f"Play/Pause (vy: {vy:.2f})"
                            last_action_time = now
                            last_spread_y.clear()
                            last_timestamps.clear()
            else:
                last_x_values.clear()
                last_spread_y.clear()
                last_timestamps.clear()

            # plot the last command
            if last_action_text:
                cv2.putText(frame_resized, f"Last action: {last_action_text}",(20, 80),cv2.FONT_HERSHEY_SIMPLEX, 0.7,(0, 255, 255), 2)

            cv2.imshow("Hand Spotify control (MediaPipe)", frame_resized)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cap.release()
        detector.close()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
