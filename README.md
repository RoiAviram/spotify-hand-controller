# Spotify Hand Controller 🎧✋

Control Spotify with simple hand gestures using your webcam, powered by Python, OpenCV and MediaPipe.

---

## What is this?

Spotify Hand Controller is a small side project that lets you control Spotify playback using hand gestures in front of your webcam.

Under the hood it:

* Captures frames from your webcam (OpenCV)
* Uses MediaPipe to detect your hand and landmarks
* Tracks the motion and shape of the hand
* Maps gestures (swipe / fist) to Spotify playback actions

Currently it is implemented and tested on Windows.

Main files:

* `main.py` – the main Python script that opens the webcam, detects gestures and controls Spotify.
* `spotify_controller.py` – helper for sending commands to Spotify.
* `run_spotify_with_hand_control.bat` – optional Windows batch file that opens Spotify and runs `main.py` together (the user must edit the paths inside it to match where the project is saved).

---

## Demo

See demo on linkedin:

<img width="1841" height="891" alt="Screenshot 2026-01-12 142813" src="https://github.com/user-attachments/assets/02a718fa-1ec3-4964-9401-05e5a288688a" />

---

## Quickstart

### Option A – Run with Python (recommended)

1. Clone or download this repository.
2. Open a terminal (CMD or PowerShell) in the project folder, for example by running:
   `cd "Spotify Hand Controller"`
3. Make sure Python 3 is installed (3.10 or newer recommended).
4. (Optional but recommended) create and activate a virtual environment:

   * `python -m venv .venv`
   * `.venv\Scripts\activate`
5. Install the main dependencies (adjust if needed to your code):

   * `pip install opencv-python mediapipe`
   * If you use a Spotify API wrapper (for example `spotipy`), also run:
     `pip install spotipy`
6. Run the controller:
   `python main.py`

### Option B – Use the batch file (run_spotify_with_hand_control.bat)

This batch file can open the Spotify desktop app and run the hand controller script (`main.py`).

Steps:

1. Right–click `run_spotify_with_hand_control.bat` and choose “Edit”.
2. Inside the file, update any absolute paths so they match the place where you saved this project on your computer (and your Python path, if it is hard-coded there).
3. Save the file.
4. Double–click `run_spotify_with_hand_control.bat` to start Spotify and the controller.

---

## Usage

1. Open the Spotify desktop app and start playing any song or playlist once.
   Important: right now the script expects active playback. If you try to skip or pause when nothing is playing, Spotify may return an error and the script can exit.

2. Run the controller with `python main.py` (or via the batch file as described above).

3. Stand in front of the webcam and use these gestures (assuming this is how they are implemented in the code):

* Swipe your hand to the right → Next track
* Swipe your hand to the left → Previous track
* Quickly open and close a fist → Play / Pause

Tips:

* Make sure your hand is well lit and clearly visible.
* Keep a reasonable distance from the camera.
* Try to keep the background around your hand relatively clean so MediaPipe can detect it easily.

---

## Architecture (high level)

* Input: frames from the webcam (OpenCV VideoCapture).
* Computer vision layer: MediaPipe Hands to detect hand landmarks in each frame.
* Gesture logic: track landmark positions over the last frames and classify patterns as horizontal swipe left / right or quick open–close fist.
* Spotify control: map each gesture to a Spotify action, for example next track, previous track, play / pause.

Depending on the implementation, Spotify can be controlled via keyboard/media keys, the Spotify desktop app, or the Spotify Web API (for example with the `spotipy` library).

---

## Limitations

* Tested only on Windows on a single machine.
* Requires a working webcam, Spotify desktop app and a valid Spotify account.
* Currently you need to start playback manually once in Spotify. If there is no active playback, some commands (next / previous / pause) may fail and cause the script to exit.
* Long-running stability (several hours of continuous use) has not been fully tested.
* Gestures are currently hard-coded for this setup.
* The batch file (`run_spotify_with_hand_control.bat`) contains absolute paths that each user must change to match their own installation.

---

## Roadmap (ideas)

* Make gestures configurable via a simple config file.
* Add a calibration step per user (hand size, camera distance).
* Improve robustness in different lighting conditions.
* Add better error handling when there is no active Spotify playback.
* Package as an easy-to-install Windows app or tray application.

---

## Why I built this

I wanted a fun way to combine:

* Real-time computer vision (OpenCV and MediaPipe)
* Simple gesture recognition
* A real-world integration with an app I actually use every day (Spotify)

This project is also part of my portfolio as an Electrical and Computer Engineering, showcasing my interest in:

* Computer vision
* Real-time systems
* Practical, product-oriented tools built around everyday use cases.
