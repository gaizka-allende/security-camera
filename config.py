# Configuration settings
MAX_SCREENSHOTS = 5  # Number of screenshots to keep 

# Video settings
VIDEO_LENGTH_SECONDS =  5 # Length of output video in seconds
FPS = 30  # Frames per second in output video
SCREENSHOT_INTERVAL = 5  # Seconds between screenshots
TOTAL_FRAMES = VIDEO_LENGTH_SECONDS * FPS  # Total frames needed for one video (900 frames)

# Cleanup settings
CLEANUP_DAYS = 1  # Number of days to keep videos before deleting 

# OpenAI settings
OPENAI_PROMPT = """Analyze this video and tell me if there are any significant changes or movements. 
Focus on:
1. People entering or leaving
2. Major object movements
3. Lighting changes
4. Any unusual activity
Please be concise and only mention notable changes.""" 

# At the start of your script
DISPLAY_WINDOW = False  # Set this to False for headless operation

# Then where you have window operations
if DISPLAY_WINDOW:
    cv2.namedWindow("Camera")
    # ... other window-related operations 