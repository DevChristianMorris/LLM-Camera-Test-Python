import cv2
import openai
import time
import pygame
import base64

# Initialize OpenAI API
openai.api_key = 'api key'

# Path to your pre-recorded "Hello" MP3 file
hello_mp3_path = 'hello.mp3'

# Initialize pygame mixer
pygame.mixer.init()

# Function to capture a photo from the laptop camera
def capture_photo():
    cam = cv2.VideoCapture(0)
    ret, frame = cam.read()
    if ret:
        photo_path = 'photo.jpg'
        cv2.imwrite(photo_path, frame)
    cam.release()
    return photo_path

# Function to encode the photo to base64
def encode_photo_to_base64(photo_path):
    with open(photo_path, 'rb') as photo_file:
        photo_base64 = base64.b64encode(photo_file.read()).decode('utf-8')
    return photo_base64

# Function to check if a human is waving in the photo using GPT-4
def check_waving(photo_base64):
    response = openai.ChatCompletion.create(
        model="gpt-4-vision",  # Assuming the model that can analyze images is named "gpt-4-vision"
        messages=[
            {"role": "system", "content": "You are an assistant that can analyze images."},
            {"role": "user", "content": f"Here is an image encoded in base64: {photo_base64}. Can you describe what is happening in the image and check if a human is waving?"}
        ]
    )
    description = response.choices[0].message['content']
    print("GPT-4 Description:", description)
    return 'waving' in description.lower()

# Function to play the "Hello" MP3
def say_hello():
    pygame.mixer.music.load(hello_mp3_path)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        time.sleep(1)

# Main loop to capture photos and check for waving humans every 60 seconds
while True:
    photo_path = capture_photo()
    photo_base64 = encode_photo_to_base64(photo_path)
    if check_waving(photo_base64):
        say_hello()
    time.sleep(60)
