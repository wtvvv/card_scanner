from select import select
import pyautogui
import keyboard
import time
from threading import Thread
from threading import Event
import tkinter as tk

gameType = "UGO00"
cardType = "common"
filenumber = 1860
# FILENUMBER_BEGIN = 1676
# FILENAME = "UGO00xxxx_common_12MP"
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
        # if(not (pyautogui.locateCenterOnScreen('rotatebutton.png', region=ROTATE_REGION) is None)):
        if(not (pyautogui.locateOnScreen('newimagebox.png',  region=FILEMENU_REGION) is None)):
            doneScanning = True
    x, y, width, height = pyautogui.locateOnScreen('newimagebox.png',  region=FILEMENU_REGION)
    pyautogui.rightClick(x, y)
    pyautogui.move(20, 20)
    pyautogui.click()
    pyautogui.write(gameType + str(filenumber) + '_' + cardType + '_12MP', interval = 0.1)
    time.sleep(0.3)
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
    try:
        x, y, width, height = pyautogui.locateOnScreen('deletebutton.png', region=FILEMENU_REGION)
        pyautogui.click(x, y)
        pyautogui.sleep(0.3)
    except TypeError:
        print(TypeError)

    x, y = pyautogui.locateCenterOnScreen('yesbutton.png', region=YES_OR_RENAME_REGION)
    pyautogui.click(x, y)
    exitEvent.clear()
    #implement alert!!!
    #exit
    canScan = True
    canCancel = False
    print("finished cancelling")
    exit()


def submit(root, selectedGameType, selectedCardType, enteredFileNumber):
    global gameType
    global cardType
    global filenumber
    if selectedGameType.get() != '':
        gameType = str(selectedGameType.get())
    if selectedCardType.get() != '':
        cardType = str(selectedCardType.get())
    if enteredFileNumber.get() != '':
        filenumber = int(enteredFileNumber.get())
    root.destroy()

def rename():
    root = tk.Tk()
    selectedGameType = tk.StringVar(root)
    selectedCardType = tk.StringVar(root)
    enteredFileNumber = tk.StringVar(root)

    tk.Label(root, text = 'Select game type:').grid(column=0, row=0, sticky=tk.W, padx=5, pady=2)
    tk.Radiobutton(root, text = 'Pokemon', variable = selectedGameType, value = "PKM00", tristatevalue=0).grid(column=0, row=1, sticky=tk.W, padx=5, pady=2)
    tk.Radiobutton(root, text = "YuGiOh", variable = selectedGameType, value = "UGO00", tristatevalue=0).grid(column=0, row=2, sticky=tk.W, padx=5, pady=2)

    tk.Label(root, text = 'Select card type:').grid(column=1, row=0, sticky=tk.W, padx=5, pady=2)
    tk.Radiobutton(root, text = 'Common', variable = selectedCardType, value = "common", tristatevalue=0).grid(column=1, row=1, sticky=tk.W, padx=5, pady=2)
    tk.Radiobutton(root, text = "Holo", variable = selectedCardType, value = "holo", tristatevalue=0).grid(column=1, row=2, sticky=tk.W, padx=5, pady=2)

    tk.Label(root, text = 'Enter new file number:').grid(column=0, row=3, sticky=tk.W, padx=5, pady=7)
    tk.Entry(root, textvariable = enteredFileNumber).grid(column=1, row=3, sticky=tk.W, padx=5, pady=7)

    tk.Button(root,text = "Submit", command=lambda: submit(root, selectedGameType, selectedCardType, enteredFileNumber)).grid(column=0, row=4, sticky=tk.E, padx=5, pady=5)
    tk.Button(root,text = "Cancel", command=root.destroy).grid(column=1, row=4, sticky=tk.W, padx=5, pady=5)

    tk.mainloop()
    return gameType + str(filenumber) + '_' + cardType + '_12MP'

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
    # pyautogui.moveTo(165, 545)
    # pyautogui.scroll(2000)
    # pyautogui.scroll(-28)
    rename()

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
                print('renaming')
                current_name = rename()
                print('finished renaming: ' + current_name)
            except:
                pass

        if keyboard.is_pressed('ctrl+up') and canScan and not canCancel:
            try:
                filenumber += 1
                pyautogui.alert(text=f'Increment filenumber to: {filenumber}', title='incremented filenumber', button='OK')
                print('increment filenumber to', filenumber)
            except:
                pass
        
        if keyboard.is_pressed('ctrl+down') and canScan and not canCancel:
            try:
                filenumber -= 1
                pyautogui.alert(text=f'Decrement filenumber to: {filenumber}', title='decremented filenumber', button='OK')
                print('increment filenumber to', filenumber)
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
