"""
Normal usage:
    if used, do nothing
    if lock-box, LOCK
    if idle, LOCK
LOCK mode:
    if unlock-box, UNLOCK
    if usage, SCREENSHOT
"""
import sys
print(sys.version)

import pyautogui as pg
import time, cv2
from datetime import datetime

pg.FAILSAFE = False

mouse_stable = False
locked = False
global_start = time.time()
start = global_start

locked_check_delay = 5
locked_move_delay = 120
unlocked_check_delay = 100
unlocked_move_delay = 100
autolock_when_unclocked = False


def screenshot(now):
    try:
        #init the cam
        video_capture = cv2.VideoCapture(0)
        #get a frame from cam
        ret, frame = video_capture.read()
        #write that to disk
        cv2.imwrite(f'./data/{now}.png', frame)
        print(f'{now} SCREENSHOOT taken!')
    except:
        pass

def runtime():
    return time.time()-global_start

while True:
    p1 = pg.position()
    x = p1[0]
    y = p1[1]
    now = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

    if x<242 and x>185 and y<1193 and y>1155 and locked==False:#LOCK
        locked=True
        print('LOCKED!')
    if x<56 and x>0 and y<1193 and y>1155 and locked==True:#UNLOCK
        locked=False
        print('UNLOCKED!')

    if locked==True:
        time.sleep(locked_check_delay)
        p2=pg.position()
        if p1!=p2:           #LOCKED, UNSTABLE
            mouse_stable = False
            print(f'{now} locked={locked}, mouse_stable={mouse_stable}, position={p2}, runtime={round(runtime(),5)}, LOCKED and SCREENSHOOTING!')
            screenshot(now)
        elif p1==p2:      #LOCKED, STABLE
            with open('mouse.log', 'w') as f:
                f.write(str(runtime))
            mouse_stable = True
            print(f'{now} locked={locked}, mouse_stable={mouse_stable}, position={p2}, runtime={round(runtime(),5)}, LOCKED & STABLE')   
            if int(time.time()-start)>locked_move_delay: #LOCKED, MOVE MOUSE
                print(f'{now} locked={locked}, mouse_stable={mouse_stable}, position={p2}, runtime={round(runtime(),5)}, LOCKED, MOVING!') 
                pg.moveTo(212, 1182) #first pinned icon
                pg.click()
                pg.moveTo(252, 1182) #second pinned icon
                pg.click()
                #pg.moveTo(p1[0], p1[1]) #starting point
                start = time.time()
    elif locked==False:
        time.sleep(unlocked_check_delay)
        p2=pg.position()
        print(f'{now} locked={locked}, mouse_stable={mouse_stable}, position={p2}, runtime={round(runtime(),5)}, NORMAL USAGE')   
        if p1==p2 and int(time.time()-start)>unlocked_move_delay: #UNLOCKED, MOVE & LOCK
            print(f'{now} locked={locked}, mouse_stable={mouse_stable}, position={p2}, runtime={round(runtime(),5)}, MOVING')  
            #pg.moveTo(212, 1182, 0.5) #first pinned icon
            #pg.click()
            pg.moveTo(252, 1182, 0.5) #second pinned icon
            pg.click()
            pg.moveTo(p2)
            pg.hotkey('alt','tab')
            mouse_stable = True
            if autolock_when_unclocked==True:
                print(f'{now} locked={locked}, mouse_stable={mouse_stable}, position={p2}, runtime={round(runtime(),5)}, UNLOCKED & STABLE, LOCKING!')
                locked = True