import cv2
import time
import pygame
import mediapipe as mp

# Path to your pre-recorded "Hello" MP3 file
hello_mp3_path = 'hello.mp3'

# Initialize pygame mixer
pygame.mixer.init()

# Initialize MediaPipe Hands
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(static_image_mode=True, max_num_hands=1, min_detection_confidence=0.5)
mp_drawing = mp.solutions.drawing_utils

# Function to capture a photo from the laptop camera
def capture_photo():
    cam = cv2.VideoCapture(0)
    ret, frame = cam.read()
    if ret:
        photo_path = 'photo.jpg'
        cv2.imwrite(photo_path, frame)
    cam.release()
    return photo_path

# Function to check if a human is waving in the photo
def check_waving(photo_path):
    image = cv2.imread(photo_path)
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    results = hands.process(image_rgb)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_drawing.draw_landmarks(image, hand_landmarks, mp_hands.HAND_CONNECTIONS)
            # For simplicity, consider any detected hand as waving
            return True
    return False

# Function to play the "Hello" MP3
def say_hello():
    pygame.mixer.music.load(hello_mp3_path)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        time.sleep(1)

# Main loop to capture photos and check for waving humans every 60 seconds
while True:
    photo_path = capture_photo()
    if check_waving(photo_path):
        say_hello()
    time.sleep(60)
