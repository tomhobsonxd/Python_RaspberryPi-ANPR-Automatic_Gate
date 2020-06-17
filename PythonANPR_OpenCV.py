#ANPR using OpenCV
#Github - tomhobsonxd

import cv2
import imutils
import time
import json
import re
import os
import numpy as np
import pytesseract
from datetime import datetime
screenCnt = None

while True:
    while screenCnt is None:
        capture = cv2.VideoCapture(0)
        _, img = capture.read()

        img = cv2.resize(img, (640, 480))

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  # convert to grey scale
        gray = cv2.bilateralFilter(gray, 11, 17, 17)  # Blur to reduce noise
        edged = cv2.Canny(gray, 30, 200)  # Perform Edge detection
    # find contours in the edged image, keep only the largest
    # ones, and initialize our screen contour
        cnts = cv2.findContours(edged.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        cnts = imutils.grab_contours(cnts)
        cnts = sorted(cnts, key=cv2.contourArea, reverse=True)[:10]
        screenCnt = None

    # loop over our contours
        for c in cnts:
        # approximate the contour
            peri = cv2.arcLength(c, True)
            approx = cv2.approxPolyDP(c, 0.018 * peri, True)

        # if our approximated contour has four points, then
        # we can assume that we have found our screen
            if len(approx) == 4:
                screenCnt = approx
            break

        #Loop capture section and check for contours, if 0, loop again, if 1, break and continue.

        print("No contour detected")



    cv2.drawContours(img, [screenCnt], -1, (0, 255, 0), 3)

# Masking the part other than the number plate
    mask = np.zeros(gray.shape, np.uint8)
    new_image = cv2.drawContours(mask, [screenCnt], 0, 255, -1, )
    new_image = cv2.bitwise_and(img, img, mask=mask)

# Now crop
    (x, y) = np.where(mask == 255)
    (topx, topy) = (np.min(x), np.min(y))
    (bottomx, bottomy) = (np.max(x), np.max(y))
    Cropped = gray[topx:bottomx + 1, topy:bottomy + 1]

# Read the number plate
    text = pytesseract.image_to_string(Cropped, config='--psm 11')
    for k in text.split("\n"):
        text = (re.sub(r"[^a-zA-Z0-9]+", '', k))
    print("Detected Number is:", text)

    with open('plates.json') as json_file:
        data = json.load(json_file)
        for p in data['plates']:
            a = p['plate']
            for k in a.split("\n"):
                plateFix = (re.sub(r"[^a-zA-Z0-9]+", '', k))
            if plateFix == text:
                print("Plate '" + p['plate'] + "' is in the database")
                now = datetime.now()
                current_time = now.strftime("%H-%M-%S")
                os.chdir('output/images/')
                fileName = text + '_-_' + current_time + '.jpg'
                cv2.imwrite(fileName, img, params=None)
                exit(0)

    #cv2.imshow('Cropped', Cropped)
    cv2.imshow('image',img)

    key = cv2.waitKey(1)
    time.sleep(1)
    screenCnt = None
    cv2.destroyAllWindows()
