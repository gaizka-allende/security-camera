import cv2
import time
from datetime import datetime
import os
from config import SCREENSHOT_INTERVAL
import numpy as np
import telegram_send
import asyncio
from asyncio import sleep

# Move these constants to the top with other constants
HEADLESS = True
ALERT_INTERVAL = 10  # seconds
last_alert_time = 0  # Track when we last sent an alert

# Create necessary directories if they don't exist
if not os.path.exists('images'):
    os.makedirs('images')

# Initialize camera
cam = cv2.VideoCapture(0)

# Create window
if not HEADLESS:
    cv2.namedWindow("Camera")

# Initialize variables
previous_frame = None

# Define async function for sending telegram messages
async def send_telegram_alert(current_time, motion_percentage, img_name, max_retries=3):
    try:
        # Open the file in binary mode
        with open(img_name, 'rb') as image_file:
            print(f"Sending alert with image: {img_name}")
            await telegram_send.send(
                messages=[f"Motion detected at {current_time} - Change: {motion_percentage:.2f}%"],
                files=[image_file]
            )
            print("Alert sent successfully")
    except Exception as e:
        print(f"Error sending Telegram alert: {str(e)}")
        print(f"Error type: {type(e)}")
        import traceback
        traceback.print_exc()

while True:
    # Capture frame
    ret, frame = cam.read()
    if not ret:
        print("Failed to grab frame")
        break

    # Display frame
    if not HEADLESS:
        cv2.imshow("Camera", frame)

    # Convert frame to grayscale for motion detection
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (21, 21), 0)

    # Initialize previous_frame on first run
    if previous_frame is None:
        previous_frame = gray
        continue

    # Compute difference between current and previous frame
    frame_diff = cv2.absdiff(previous_frame, gray)
    thresh = cv2.threshold(frame_diff, 25, 255, cv2.THRESH_BINARY)[1]
    thresh = cv2.dilate(thresh, None, iterations=2)

    # Calculate the percentage of changed pixels
    motion_pixels = np.sum(thresh > 0)
    total_pixels = thresh.size
    motion_percentage = (motion_pixels / total_pixels) * 100

    # Define motion threshold (adjust this value as needed)
    motion_threshold = 1.0  # 1% of pixels changed
    motion_detected = motion_percentage > motion_threshold
    
    if motion_detected:
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Check if enough time has passed since last alert
        current_timestamp = time.time()
        if current_timestamp - last_alert_time >= ALERT_INTERVAL:
            print(f"\nMotion detected at {current_time} - Change: {motion_percentage:.2f}%")
            
            # Save the frame that triggered the detection
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            img_name = os.path.join("images", f"motion_{timestamp}.png")
            cv2.imwrite(img_name, frame)
            print(f"Motion frame saved: {img_name}")

            # Run the async function to send telegram alert
            asyncio.run(send_telegram_alert(current_time, motion_percentage, img_name))
            
            # Update the last alert time
            last_alert_time = current_timestamp

    # Update previous frame
    previous_frame = gray

    # Wait for screenshot interval, checking for 'q' press to quit
    start_time = time.time()
    while (time.time() - start_time) < SCREENSHOT_INTERVAL:
        key = cv2.waitKey(1)
        if key & 0xFF == ord('q'):
            print("Q pressed, closing...")
            cam.release()
            if not HEADLESS:
                cv2.destroyAllWindows()
            exit()

# Cleanup
cam.release()
if not HEADLESS:
    cv2.destroyAllWindows()
