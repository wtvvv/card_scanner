import pyautogui
import keyboard
import time
from threading import Thread
from threading import Event

FILENUMBER_BEGIN = 1433
FILENAME = "UGO00xxxx_common_12MP"
scanning = False
cancelling = False

def scanCard(filenumber, exitEvent):
    global scanning
    print('scanning')
    #scan
    pyautogui.click(1660, 980)
    exitEvent.wait(40)
    if exitEvent.is_set():
        exit()
    #rotate
    rotated = False
    while not rotated:
        # try:
        #     pyautogui.locateCenterOnScreen('renamebutton.png')
        # except ImageNotFoundException:
        #     pass
        time.sleep(2)
        if(not (pyautogui.locateCenterOnScreen('rotatebutton.png') is None)):
            pyautogui.click(974, 57)
            rotated = True
    exitEvent.wait(10)
    if exitEvent.is_set(): 
        scanning = False
        exit()

    #rename
    x, y, width, height = pyautogui.locateOnScreen('newimagebox.png')
    pyautogui.rightClick(x, y)
    pyautogui.move(20, 20)
    pyautogui.click()
    pyautogui.write(FILENAME.replace('xxxx', str(filenumber)), interval = 0)
    time.sleep(1)
    x, y = pyautogui.locateCenterOnScreen('renamebutton.png')
    pyautogui.click(x, y)
    scanning = False
    print("finished scanning")

def cancelCard(exitEvent):
    global cancelling
    global scanning
    exitEvent.set()
    time.sleep(0.5)
    #cancel
    pyautogui.click(1751, 981)
    #delete
    
    ###
    # deleted = False
    # while not deleted:
    #     try:
    #         pyautogui.locateOnScreen('newimagebox.png')
    #     except ImageNotFoundException:
    #         pass
    ###
    deleted = False
    while not deleted:
        time.sleep(2)
        if(not (pyautogui.locateOnScreen('newimagebox.png') is None)):
            deleted = True

    # time.sleep(15)
    x, y, width, height  = pyautogui.locateOnScreen('newimagebox.png')
    pyautogui.click(x, y)
    pyautogui.rightClick()
    pyautogui.move(20,40)
    pyautogui.click()
    time.sleep(0.5)
    x, y = pyautogui.locateCenterOnScreen('yesbutton.png')
    pyautogui.click(x, y)
    exitEvent.clear()

    cancelling = False
    scanning = False
    print("finished cancelling")
    exit()

if __name__ == "__main__":
    #go to Regula software!!!

    #setup
    exitEvent = Event()
    filenumber = FILENUMBER_BEGIN
    pyautogui.moveTo(165, 545)
    pyautogui.scroll(2000)
    pyautogui.scroll(-28)
    #set 12MP and single-page!!!

    while True:
        if keyboard.is_pressed('ctrl+s') and not scanning:
            scanning = True
            scanThread = Thread(target = scanCard, args=(filenumber, exitEvent))
            scanThread.start()
            time.sleep(0.5)
            filenumber += 1
            #change scanning variable!!!

        if keyboard.is_pressed('ctrl+c') and not cancelling:
            cancelling = True
            print("interrupt")
            cancelThread = Thread(target = cancelCard, args=(exitEvent, ))
            cancelThread.start()
            time.sleep(0.5)
            filenumber -= 1
            #change cancelling variable!!!
        
        if keyboard.is_pressed('esc'):
            exitEvent.set()
            break
        
    print('exited')

        #set up disable key_detect!!!
        # if keyboard.is_pressed(hotkey(Ctrl))
