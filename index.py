import pyautogui;
import time;

def wait_for_and_click_modal():
    button_image = 'target.png'  # Save a screenshot of the accept button
    
    while True:
        time.sleep(3);
        pyautogui.PAUSE = 3;
        try:
            # Look for the button on screen
            button_location = pyautogui.locateOnScreen(button_image, confidence=0.8)
            
            if button_location:
                button_x, button_y = pyautogui.center(button_location)
                
                pyautogui.click(button_x, button_y)
                print("Clicked!")
                
        except Exception as e:
            print(f"Error: {e}")
        

# Run the function
wait_for_and_click_modal()