import pyautogui;
import time;

while True:
    time.sleep(5);
    pyautogui.PAUSE = 0.5;

    try:
        imgPosition = pyautogui.locateCenterOnScreen('target.png', confidence=0.5);

        pyautogui.moveTo(imgPosition, duration=1);

        pyautogui.click(imgPosition);
    except pyautogui.ImageNotFoundException:
        print('Image not found');