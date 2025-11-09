import pyautogui
import time
import webbrowser

# === CONFIGURATION ===
CONTACT_NAME = "SE - AI-B3 - 1"  # Use this variable instead of hardcoding
MESSAGE = " I’m pleased to share that I’ve successfully completed all Week-1 videos, assignments, tasks, and certification-Questionaries.\
The relevant code snippets have been uploaded to the designated GitHub repository, and I humbly seek your kind review and valuable feedback.(Auto Message)"
WHATSAPP_WEB_URL = "https://web.whatsapp.com/"

# === SCRIPT START ===
print("Starting WhatsApp automation in 5 seconds...")
print("Please make sure WhatsApp Web is open and logged in.")
time.sleep(5)

# Step 1: Open WhatsApp Web
webbrowser.open(WHATSAPP_WEB_URL)
print("Opening WhatsApp Web...")
time.sleep(8)

# Step 2: Search for the contact
print(f"Searching for contact: {CONTACT_NAME}")
pyautogui.click(x=107, y=186)  # Click search bar
time.sleep(1)
pyautogui.typewrite(CONTACT_NAME)  # Fixed: Use variable with proper quotes
time.sleep(2)

# Step 3: Click on the contact
pyautogui.click(x=138, y=330)  # Click first result
time.sleep(2)

# Step 4: Type and send message
print(f"Sending message: {MESSAGE}")
pyautogui.typewrite(MESSAGE)
time.sleep(1)
pyautogui.press('enter')

print("Message sent successfully!")