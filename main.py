import pyautogui
import time
import math
from PIL import ImageStat

import pytesseract
from pytesseract import Output
from fuzzywuzzy import fuzz

import cv2
import numpy as np

import os

pytesseract.pytesseract.tesseract_cmd = r"C:\Users\amki.AD\AppData\Local\Programs\Tesseract-OCR\tesseract.exe"

def tesseract_ocr(file):
    #text = cv2.imread(file)
    gs = cv2.cvtColor(file, cv2.COLOR_BGR2GRAY)
    thr = cv2.threshold(gs, 80, 255, cv2.THRESH_BINARY)[1]
    #thr = cv2.adaptiveThreshold(gs,255,cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 7, 10)
    d = pytesseract.image_to_string(thr, output_type=Output.DICT, lang='eng', config="--psm 7")

    #cv2.imshow('gs',gs)
    #cv2.imshow('thr',thr)
    #cv2.waitKey(0)
    #cv2.destroyAllWindows()
    return d['text']

def is_text_match(strA, strB):
    if(fuzz.ratio(strA,strB) > 51):
        return True
    return False

# read bananas image template
template = cv2.imread('bobber1.png', cv2.IMREAD_UNCHANGED)
hh, ww = template.shape[:2]

# extract bananas base image and alpha channel and make alpha 3 channels
base = template[:,:,0:3]
alpha = template[:,:,3]
alpha = cv2.merge([alpha,alpha,alpha])

searchBoxSize = 600

searchBoxOffsetX = 1600
searchBoxOffsetY = 800

offset2 = round(searchBoxSize/2)
offset4 = round(searchBoxSize/4)

searchBoxX = searchBoxOffsetX-offset2
searchBoxY = searchBoxOffsetY-offset4

def cv_findBobber(x,y):
    image = pyautogui.screenshot(region=(searchBoxX,searchBoxY,searchBoxSize,searchBoxSize))
    img = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)

    # do masked template matching and save correlation image
    correlation = cv2.matchTemplate(img, base, cv2.TM_CCORR_NORMED, mask=alpha)
    # set threshold and get all matches
    threshhold = 0.95
    loc = np.where(correlation >= threshhold)

    pts = list(zip(*loc[::-1]))

    if(len(pts) < 1):
        return

    return pts[0]

    # draw matches 
    result = img.copy()
    for pt in pts:
        cv2.rectangle(result, pt, (pt[0]+ww, pt[1]+hh), (0,0,255), 1)
        print(pt)
    
    cv2.imshow('base',base)
    cv2.imshow('alpha',alpha)
    cv2.imshow('result',result)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    

def click():
    pyautogui.mouseDown()
    time.sleep(0.01)
    pyautogui.mouseUp()
        
def dist(aX, aY, bX, bY):
    x = pow(abs(aX-bX), 2)
    y = pow(abs(aY-bY), 2)
    return math.sqrt(pow(x, 2) + pow(y, 2))

#def is_lava_background(x, y, size=60):
#    """Check if the area around coordinates is mostly red (lava)"""
#    region = (max(0, x - size//2), max(0, y - size//2), size, size)
#    screenshot = pyautogui.screenshot(region=region)
#    stats = ImageStat.Stat(screenshot)
#    r, g, b = stats.mean[0], stats.mean[1], stats.mean[2]
#    print(f"Avg color R:{r:.0f} G:{g:.0f} B:{b:.0f}")
#    return r > 150 and r > g * 2 and r > b * 2

screenWidth, screenHeight = pyautogui.size()
print(f"W: {screenWidth} h: {screenHeight}")

def throwBobber(x,y):
    pyautogui.moveTo(x, y)
    click()
    time.sleep(0.7)

def handleBite(everything, targetItem, x,y):
    screenX = x + searchBoxX
    screenY = y + searchBoxY
    print(f"BITE! @{x}/{y} screen: {screenX}/{screenY}")
    if(everything):
        click()
        return True

    screenshot = pyautogui.screenshot(region=(screenX-120,screenY-100,290,100))
    cvimg = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
    res = tesseract_ocr(cvimg)
    if(is_text_match(res,targetItem)):
        click()
        return True
    else:
        print(f"{res} is probably not {targetItem}. Waiting...")
        time.sleep(0.5)
        return False
    #cv2.imshow("screen",cvimg)
    #cv2.waitKey(0)
    #cv2.destroyAllWindows()
    #cv2.imwrite(f"item_{time.time()}.png",cvimg)

def check(everything, targetItem):
    lastExec = time.time()
    lastBobberX = 0
    lastBobberY = 0
    while True:
        now = time.time()
        if lastExec + 1/15 > now:
            continue
        lastExec = now
        bobberPos = cv_findBobber(searchBoxOffsetX,searchBoxOffsetY)
        if(bobberPos is None):
            print("NO BOBER!")
            continue
        bobberX = (bobberPos[0]).item()
        bobberY = (bobberPos[1]).item()
        if(lastBobberX == 0 and lastBobberY == 0):
            lastBobberX = bobberX
            lastBobberY = bobberY
            print(f"First BOBER @{bobberX}/{bobberY}")
            continue
        distance = dist(lastBobberX,lastBobberY,bobberX,bobberY)
        if(distance > 2):
            print(f"BOBER CATCH @{bobberX}/{bobberY} d: {distance}")
            if(handleBite(everything, targetItem, bobberX,bobberY)):
                return
            else:
                lastBobberX = bobberX
                lastBobberY = bobberY
                continue

fish_everything=False
fish_for="Hellstone Crate"
for i in range(50):
    print(f"Throw {i}")
    throwBobber(searchBoxOffsetX,searchBoxOffsetY)
    check(fish_everything, fish_for)
    time.sleep(1)

print("EXIT")