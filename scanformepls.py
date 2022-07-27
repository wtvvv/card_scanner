import pyautogui
import keyboard
import time
from threading import Thread
from threading import Event

FILENUMBER_BEGIN = 1438
FILENAME = "UGO00xxxx_common_12MP"
canScan = True
canCancel = False

def scanCard(filenumber, exitEvent):
    print('scanning')
    global canScan
    global canCancel
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
        exit()
    #rename
    x, y, width, height = pyautogui.locateOnScreen('newimagebox.png')
    pyautogui.rightClick(x, y)
    pyautogui.move(20, 20)
    pyautogui.click()
    pyautogui.write(FILENAME.replace('xxxx', str(filenumber)), interval = 0.1)
    time.sleep(1)
    x, y = pyautogui.locateCenterOnScreen('renamebutton.png')
    pyautogui.click(x, y)

    #implement alert!!!
    pyautogui.alert(text='NEEEEEEEEEXXXXXTTTTTTTT CAAAAAARRRRRRRDDDDDDD PLLLEAAASEE', title='Scan finished', button='OK')
    #exit
    canScan = True
    canCancel = False
    print("finished scanning")
    exit()

def cancelCard(exitEvent):
    print('cancelling')
    global canScan
    global canCancel
    exitEvent.set()
    time.sleep(0.5)
    #cancel
    pyautogui.click(1751, 981)
    #delete
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
    time.sleep(0.2)
    x, y = pyautogui.locateCenterOnScreen('yesbutton.png')
    pyautogui.click(x, y)
    exitEvent.clear()
    #exit
    canScan = True
    canCancel = False
    print("finished cancelling")
    exit()

if __name__ == "__main__":
    #go to Regula software
    x, y = pyautogui.locateCenterOnScreen('regulabutton.png')
    pyautogui.click(x, y)

    #setup
    exitEvent = Event()
    filenumber = FILENUMBER_BEGIN
    pyautogui.moveTo(165, 545)
    pyautogui.scroll(2000)
    pyautogui.scroll(-28)

    while True:
        if keyboard.is_pressed('ctrl+space') and canScan:
            canScan = False
            canCancel = True
            scanThread = Thread(target = scanCard, args=(filenumber, exitEvent))
            scanThread.start()
            filenumber += 1

        if keyboard.is_pressed('ctrl+x') and canCancel:
            canScan = False
            canCancel = False
            filenumber -= 1
            cancelThread = Thread(target = cancelCard, args=(exitEvent, ))
            cancelThread.start()
        
        if keyboard.is_pressed('ctrl+alt+r') and canScan and not canCancel:
            filenumber = pyautogui.prompt(text='Enter starting file number', title='' , default='')
        
        if keyboard.is_pressed('esc'):
            exitEvent.set()
            break
        
    print('exiting main thread...')
