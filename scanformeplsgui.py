from typing import Type
import pyautogui
import keyboard
import traceback
import time
from threading import Thread
from threading import Event
import tkinter as tk


FILEMENU_REGION = (5, 286, 320, 740) #set to None if unknown
# YES_OR_RENAME_REGION = (850, 450, 360, 160) #set to None if unknown
YES_OR_RENAME_REGION = None
ROTATE_REGION = (900, 15, 250, 75) #set to None if unknown
LIVEVIEW_REGION = (534, 178, 123, 40) #set to None if unknown

ROTATE_BUTTON = ("rotatebutton.png", ROTATE_REGION)
NEW_IMAGE_BOX_BUTTON = ("newimagebutton.png", FILEMENU_REGION)
RENAME_BUTTON = ("renamebutton.png", YES_OR_RENAME_REGION)
DELETE_BUTTON = ("deletebutton.png", FILEMENU_REGION)
YES_BUTTON = ("yesbutton.png", YES_OR_RENAME_REGION)
scanButtonCoord = [1660, 980]
cancelButtonCoord = [0,0]
rotateButtonCoord = [0,0]

gameType = "UGO00"
cardType = "common"
filenumber = 0000
canScan = True
canCancel = False
lidSignal = False
trackingLid = False

def search(button, region=None, waitTime=0, event=None):
    found = False
    while not found:
        if waitTime > 0:
            time.sleep(waitTime)
        if event is not None:
            if event.is_set():
                exit
        if not (pyautogui.locateOnScreen(button, region=region) is None):
            found = True
    try:
        x, y = pyautogui.locateOnScreen(button, region=region)
        return x, y
    except TypeError as e:
        print(e)

def searchCenter(button, region=None, waitTime=0, event=None):
    found = False
    while not found:
        if waitTime > 0:
            time.sleep(waitTime)
        if event is not None:
            if event.is_set():
                exit
        if not (pyautogui.locateOnScreen(button, region=region) is None):
            found = True
    try:
        x, y = pyautogui.locateCenterOnScreen(button, region=region)
        return x, y
    except TypeError as e:
        print(e)

def calibrate():
    global scanButtonCoord
    global cancelButtonCoord
    global ROTATE_REGION
    try:
        scanButtonCoord[0], scanButtonCoord[1] = pyautogui.locateCenterOnScreen("scanbutton.png")
        cancelButtonCoord[0], cancelButtonCoord[1] = pyautogui.locateCenterOnScreen("cancelbutton.png")
        x_rotateButtonCoord, y_rotateButtonCoord = pyautogui.locateCenterOnScreen("rotatebutton.png")
        ROTATE_REGION = (x_rotateButtonCoord-75, y_rotateButtonCoord-25, 150, 50)
    except TypeError as e:
        print(traceback.format_exc())

def scanCard(cancelEvent):
    global canScan
    global canCancel
    global filenumber
    #scan
    print('scanning')
    pyautogui.click(scanButtonCoord[0], scanButtonCoord[1])
    pyautogui.moveTo(1779, 338)
    cancelEvent.wait(40)
    if cancelEvent.is_set():
        exit()

    #rotate
    doneScanning = False
    while not doneScanning:
        time.sleep(2)
        if(not (pyautogui.locateCenterOnScreen('rotatebutton.png',  region=ROTATE_REGION) is None)):
            doneScanning = True
    canCancel = False #disable cancel at this stage (only allow cancel while card is scanning)
    print('\trotating')
    x, y = pyautogui.locateCenterOnScreen('rotatebutton.png',  region=ROTATE_REGION)
    pyautogui.click(x, y)
    # pyautogui.click(974, 57)
    cancelEvent.wait(6)
    if cancelEvent.is_set():
        exit()

    #rename
    print('\trenaming')
    x, y = searchCenter('newimagebox.png', FILEMENU_REGION, waitTime=1, event=cancelEvent)
    pyautogui.rightClick(x, y)
    pyautogui.move(20, 45)
    pyautogui.click()
    pyautogui.write(gameType + str(filenumber) + '_' + cardType + '_12MP', interval = 0.1)
    time.sleep(0.3)
    x, y = pyautogui.locateCenterOnScreen('renamebutton.png', region=YES_OR_RENAME_REGION)
    pyautogui.click(x, y)    
    time.sleep(2)

    #increment filenumber
    filenumber += 1

    #alert
    print('\tshowing alert')
    pyautogui.alert(text='NEEEEEEEEEXXXXXTTTTTTTT CAAAAAARRRRRRRDDDDDDD PLLLEAAASEE', title='Scan finished', button='OK')
    pyautogui.moveTo(1765, 148)
    #exit
    canScan = True
    print("finished scanning")
    exit()

def startScanThread(cancelEvent):
    global lidSignal
    global canScan
    global canCancel
    if canScan:
        lidSignal = False
        canScan = False
        canCancel = True
        scanThread = Thread(target = scanCard, args=(cancelEvent, ))
        scanThread.start()

def cancelCard(cancelEvent, exitEvent):
    print('cancelling')
    global canScan
    global canCancel
    cancelEvent.set()
    time.sleep(0.5)
    #cancel
    pyautogui.click(cancelButtonCoord[0], cancelButtonCoord[1])
    #delete
    deleted = False
    while not deleted:
        if exitEvent.is_set():
            print('exiting cancel thread...')
            exit()
        if(not (pyautogui.locateOnScreen('newimagebox.png', region=FILEMENU_REGION) is None)):
            deleted = True
    x, y, width, height  = pyautogui.locateOnScreen('newimagebox.png', region=FILEMENU_REGION)
    pyautogui.moveTo(x, y)
    time.sleep(0.5)
    pyautogui.click()
    pyautogui.rightClick()
    time.sleep(0.2)

    try:
        x, y, width, height = pyautogui.locateOnScreen('deletebutton.png', region=FILEMENU_REGION)
        pyautogui.click(x, y)
        pyautogui.sleep(0.3)
    except TypeError as e:
        print(e)

    try:
        x, y = pyautogui.locateCenterOnScreen('yesbutton.png', region=YES_OR_RENAME_REGION)
        pyautogui.click(x, y)
    except TypeError as e:
        print(e)
    
    cancelEvent.clear()
    #implement alert!!!
    #exit
    canScan = True
    canCancel = False
    print("finished cancelling")
    exit()

def startCancelThread(cancelEvent, exitEvent):
    global canScan
    global canCancel
    if canCancel:
        canScan = False
        canCancel = False
        cancelThread = Thread(target = cancelCard, args=(cancelEvent, exitEvent))
        cancelThread.start()

def trackLid(exitEvent):
    print("start tracking lid")
    global canScan
    global lidSignal
    global trackingLid
    
    lidOpen = False
    while canScan:
        print("awaiting lid open")
        while not lidOpen:
            exitEvent.wait(1)
            if exitEvent.is_set():
                print("exiting trackLid thread...")
                exit()
            if not (pyautogui.locateOnScreen('liveview.png', region = LIVEVIEW_REGION) is None):
                lidOpen = True
        print("awaiting lid close")
        while lidOpen:
            if exitEvent.is_set():
                print("exiting trackLid thread...")
                exit()
            if pyautogui.locateOnScreen('liveview.png', region = LIVEVIEW_REGION) is None:
                lidOpen = False
                
    lidSignal = True
    trackingLid = False
    print("finished tracking lid")

def on_closing(root):
    cancelEvent.set()
    print("cancelEvent is set")
    exitEvent.set()
    print("exitEvent is set")
    root.destroy()
    print("---exiting program---")

def updateFileName(selectedGameType, selectedCardType, enteredFileNumber):
    global gameType
    global cardType
    global filenumber
    if selectedGameType.get() != '':
        gameType = str(selectedGameType.get())
    if selectedCardType.get() != '':
        cardType = str(selectedCardType.get())
    if enteredFileNumber.get() != '':
        filenumber = int(enteredFileNumber.get())

    current_name = gameType + str(filenumber) + '_' + cardType + '_12MP'
    print('name updated: ' + current_name)

def updateFileNumber(enteredFileNumber):
    global filenumber
    filenumber += 1
    print('filenumber updated: ' + filenumber)

def GUI(cancelEvent, exitEvent):
    root = tk.Tk()
    selectedGameType = tk.StringVar(root)
    selectedCardType = tk.StringVar(root)
    enteredFileNumber = tk.StringVar(root)

    # scan_image = tk.PhotoImage(file="GUIscanbutton.png", width=10, height=10)
    tk.Button(root, 
            # image = scan_image,
            text = "Scan",
            width=30,
            height=10,
            command=lambda: startScanThread(cancelEvent)).grid(column = 0, row = 0, pady = 20, columnspan=2)
    tk.Button(root,
            text = "Cancel",
            width=30,
            height=10,
            command=lambda: startCancelThread(cancelEvent, exitEvent)).grid(column = 0, row = 1, pady = 20, columnspan=2)

    tk.Label(root, text = 'Select game type:').grid(column=0, row=2, sticky=tk.W, padx=5, pady=2)
    tk.Label(root, text = 'Select card type:').grid(column=0, row=4, sticky=tk.W, padx=5, pady=2)

    tk.Radiobutton(root, text = 'Pokemon', variable = selectedGameType, value = "PKM00", tristatevalue=0).grid(column=0, row=3, sticky=tk.W, padx=5, pady=0.5)
    tk.Radiobutton(root, text = 'Common', variable = selectedCardType, value = "common", tristatevalue=0).grid(column=0, row=5, sticky=tk.W, padx=5, pady=0.5)
    tk.Radiobutton(root, text = "Holo", variable = selectedCardType, value = "holo", tristatevalue=0).grid(column=0, row=6, sticky=tk.W, padx=5, pady=0.5)
    tk.Radiobutton(root, text = 'Reverse Holo', variable = selectedCardType, value = "reverse_holo", tristatevalue=0).grid(column=0, row=7, sticky=tk.W, padx=5, pady=0.5)
    tk.Radiobutton(root, text = "Symbol Holo", variable = selectedCardType, value = "symbol_holo", tristatevalue=0).grid(column=0, row=8, sticky=tk.W, padx=5, pady=0.5)
    tk.Radiobutton(root, text = 'Full Art Holo', variable = selectedCardType, value = "full_art_holo", tristatevalue=0).grid(column=0, row=9, sticky=tk.W, padx=5, pady=0.5)
    tk.Radiobutton(root, text = "Full Art Embossed Holo", variable = selectedCardType, value = "full_art_embossed_holo", tristatevalue=0).grid(column=0, row=10, sticky=tk.W, padx=5, pady=0.5)
    tk.Radiobutton(root, text = 'Full Art Pattern Holo', variable = selectedCardType, value = "full_art_pattern_common", tristatevalue=0).grid(column=0, row=11, sticky=tk.W, padx=5, pady=0.5)

    tk.Radiobutton(root, text = "YuGiOh", variable = selectedGameType, value = "UGO00", tristatevalue=0).grid(column=1, row=3, sticky=tk.W, padx=5, pady=2)
    tk.Radiobutton(root, text = 'Common', variable = selectedCardType, value = "common", tristatevalue=0).grid(column=1, row=5, sticky=tk.W, padx=5, pady=0.5)
    tk.Radiobutton(root, text = "Holo", variable = selectedCardType, value = "holo", tristatevalue=0).grid(column=1, row=6, sticky=tk.W, padx=5, pady=0.5)
    tk.Radiobutton(root, text = 'Silver Foil Holo', variable = selectedCardType, value = "silver_foil_holo", tristatevalue=0).grid(column=1, row=7, sticky=tk.W, padx=5, pady=0.5)
    tk.Radiobutton(root, text = 'Embossed Holo', variable = selectedCardType, value = "embossed_holo", tristatevalue=0).grid(column=1, row=8, sticky=tk.W, padx=5, pady=0.5)
    tk.Radiobutton(root, text = "Half Art Paral", variable = selectedCardType, value = "half_art_paral", tristatevalue=0).grid(column=1, row=9, sticky=tk.W, padx=5, pady=0.5)

    tk.Label(root, text = 'Enter new file number:').grid(column=0, row=15, sticky=tk.W, padx=5, pady=7)
    tk.Spinbox(root, from_=0, textvariable=enteredFileNumber).grid(column=1, row=15, sticky=tk.W, padx=5, pady=7)
    tk.Button(root,text = "Update", command=lambda: updateFileName(selectedGameType, selectedCardType, enteredFileNumber)).grid(column=0, row=16, sticky=tk.EW, padx=5, pady=5, columnspan=2)
    tk.Button(root,text = "Calibrate", command=calibrate).grid(column=0, row=17, sticky=tk.EW, padx=5, pady=5, columnspan=2)

    ws = root.winfo_screenwidth() # width of the screen
    hs = root.winfo_screenheight() # height of the screen
    root.geometry(f'300x{str(hs)}+{ws-300}+0') # set placement of window
    root.protocol("WM_DELETE_WINDOW", lambda: on_closing(root)) # call end program handler (set cancelEvent and exitEvent)
    tk.mainloop()

if __name__ == "__main__":
    # go to Regula software
    try:
        regulaX, regulaY = pyautogui.locateCenterOnScreen('regulabutton.png')
        pyautogui.click(regulaX, regulaY)
        time.sleep(0.5)
        scanButtonCoord[0], scanButtonCoord[1] = pyautogui.locateCenterOnScreen("scanbutton.png") #!!!
        cancelButtonCoord[0], cancelButtonCoord[1] = pyautogui.locateCenterOnScreen("cancelbutton.png") #!!!
    except TypeError as e:
        print(e)
        pass

    pyautogui.alert('set to 12MP and single-page format')

    #setup
    cancelEvent = Event()
    exitEvent = Event()
    GUI(cancelEvent, exitEvent)

    # trackLidThread = Thread(target = trackLid, args=(cancelEvent, exitEvent))
    # trackLidThread.start()

    # while True:
    #     if canScan and not trackingLid:
    #         trackLidThread = Thread(target = trackLid, args=(exitEvent, ))
    #         trackLidThread.start()
    #         trackingLid = True

    #     if (keyboard.is_pressed('ctrl+space') or lidSignal) and canScan:
    #         lidSignal = False
    #         canScan = False
    #         canCancel = True
    #         scanThread = Thread(target = scanCard, args=(cancelEvent))
    #         scanThread.start()
    #         filenumber += 1

    #     if keyboard.is_pressed('ctrl+x') and canCancel:
    #         canScan = False
    #         canCancel = False
    #         filenumber -= 1
    #         cancelThread = Thread(target = cancelCard, args=(cancelEvent, exitEvent))
    #         cancelThread.start()
        
    #     if keyboard.is_pressed('ctrl+alt+r') and canScan and not canCancel:
    #         try:
    #             print('renaming')
    #             current_name = rename()
    #             print('finished renaming: ' + current_name)
    #         except:
    #             pass

    #     if keyboard.is_pressed('ctrl+up') and canScan and not canCancel:
    #         try:
    #             filenumber += 1
    #             pyautogui.alert(text=f'Increment filenumber to: {filenumber}', title='incremented filenumber', button='OK')
    #             print('increment filenumber to', filenumber)
    #         except:
    #             pass
        
    #     if keyboard.is_pressed('ctrl+down') and canScan and not canCancel:
    #         try:
    #             if filenumber > 0:
    #                 filenumber -= 1
    #             pyautogui.alert(text=f'Decrement filenumber to: {filenumber}', title='decremented filenumber', button='OK')
    #             print('increment filenumber to', filenumber)
    #         except:
    #             pass

    #     if keyboard.is_pressed('esc'):
    #         cancelEvent.set()
    #         exitEvent.set()
    #         break
        
    print('exiting main thread...')

#implement dynamic click for scan, rotate, and cancel!!!
#change ALL time.sleep(x) into event.wait(x)


#implement clicking regulabutton before clicking anything else
###turn button presses into a function
###implement: trackLid
###implement: keypress option, not just GUI
###implement: disable "Update" button when scanning/cancelling (i.e. if canScan and not canCancel)
###implement: "Calibrate" function to remap scan/cancel/rotate button positions
