import pyautogui
import keyboard
import time
from threading import Thread
from threading import Event

FILENUMBER_BEGIN = 1782
FILENAME = "UGO00xxxx_common_12MP"
FILEMENU_REGION = (5, 286, 320, 708) #set to None if unknown
YES_OR_RENAME_REGION = (850, 450, 360, 160) #set to None if unknown
ROTATE_REGION = (900, 15, 250, 75) #set to None if unknown
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
    #rename
    doneScanning = False
    while not doneScanning:
        # try:
        #     pyautogui.locateCenterOnScreen('renamebutton.png')
        # except ImageNotFoundException:
        #     pass
        time.sleep(2)
        if(not (pyautogui.locateCenterOnScreen('rotatebutton.png', region=ROTATE_REGION) is None)):
            doneScanning = True
    x, y, width, height = pyautogui.locateOnScreen('newimagebox.png',  region=FILEMENU_REGION)
    pyautogui.rightClick(x, y)
    pyautogui.move(20, 20)
    pyautogui.click()
    pyautogui.write(FILENAME.replace('xxxx', str(filenumber)), interval = 0.1)
    time.sleep(0.2)
    x, y = pyautogui.locateCenterOnScreen('renamebutton.png', region=YES_OR_RENAME_REGION)
    pyautogui.click(x, y)    
    time.sleep(1)

    #rotate
    pyautogui.click(974, 57)
    exitEvent.wait(6)
    if exitEvent.is_set():
        exit()

    #alert
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
        if(not (pyautogui.locateOnScreen('newimagebox.png', region=FILEMENU_REGION) is None)):
            deleted = True
    # time.sleep(15)
    x, y, width, height  = pyautogui.locateOnScreen('newimagebox.png', region=FILEMENU_REGION)
    pyautogui.click(x, y)
    pyautogui.rightClick()
    time.sleep(0.2)
    
    # pyautogui.move(20,40)
    # pyautogui.click()
    # time.sleep(0.2)
    x, y, width, height = pyautogui.locateOnScreen('deletebutton.png', region=FILEMENU_REGION)
    pyautogui.click(x, y)
    pyautogui.sleep(0.3)

    x, y = pyautogui.locateCenterOnScreen('yesbutton.png', region=YES_OR_RENAME_REGION)
    pyautogui.click(x, y)
    exitEvent.clear()
    #implement alert!!!
    #exit
    canScan = True
    canCancel = False
    print("finished cancelling")
    exit()

#implement rename function!!!

if __name__ == "__main__":
    #go to Regula software
    try:
        regulaX, regulaY = pyautogui.locateCenterOnScreen('regulabutton.png')
        pyautogui.click(regulaX, regulaY)
    except TypeError:
        pass
    pyautogui.alert('set to 12MP and single-page format')

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
            try:
                pyautogui.confirm('Enter option Gfg', buttons =['A', 'B', 'C'])
                filenumber = int(pyautogui.prompt(text='Enter starting file number', title='' , default=''))
            except:
                pass

        if keyboard.is_pressed('esc'):
            exitEvent.set()
            break
        
    print('exiting main thread...')

#turn button presses into a function?!!!
#def buttonpress():

#implement dynamic click for scan, rotate, and cancel!!!
#implement clicking regulabutton before clicking anything else!!!
#change ALL time.sleep(x) into event.wait(x)
