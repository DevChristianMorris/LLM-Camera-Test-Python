import cv2
import openai
import time
import os
from playsound import playsound

# Initialize OpenAI API
openai.api_key = 'sk-proj-j6CV8XzFuDHh1vf5z9CXT3BlbkFJSFC7GD7KGFIV5nJoIinz'

# Path to your pre-recorded "Hello" MP3 file
hello_mp3_path = 'path_to_your_hello.mp3'

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
    with open(photo_path, 'rb') as photo:
        response = openai.Image.create(file=photo, purpose="analyze", description="Check if a human is waving")
    # Assuming the response contains a field indicating if a human is waving
    return 'waving' in response['data']['analyzed_features']

# Function to play the "Hello" MP3
def say_hello():
    playsound(hello_mp3_path)

# Main loop to capture photos and check for waving humans every 60 seconds
while True:
    photo_path = capture_photo()
    if check_waving(photo_path):
        say_hello()
    time.sleep(60)
