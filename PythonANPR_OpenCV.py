# ANPR using OpenCV
# Github - tomhobsonxd
# Website - http://tahobson.com/

import cv2
import imutils
import time
import json
import re
import os
import numpy as np
import pytesseract
from datetime import datetime
from os import path

screenCnt = None
capture = cv2.VideoCapture(0)  # Main source for video/image input. See README for more info.

while True:  # Run the program continuously.
    while screenCnt is None:  # Repeat process while no plate has been detected.
        _, img = capture.read()

        img = cv2.resize(img, (640, 480))

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  # convert to grey scale
        gray = cv2.bilateralFilter(gray, 11, 17, 17)  # Blur to reduce noise
        edged = cv2.Canny(gray, 30, 200)

        # Perform Edge detection
        # find contours in the edged image, keep only the largest
        # ones, and initialise the screen contour
        cnts = cv2.findContours(edged.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        cnts = imutils.grab_contours(cnts)
        cnts = sorted(cnts, key=cv2.contourArea, reverse=True)[:10]
        screenCnt = None

        # loop over the contours
        for c in cnts:
            # approximate the contour
            peri = cv2.arcLength(c, True)
            approx = cv2.approxPolyDP(c, 0.018 * peri, True)

            # if our approximated contour has four points, then
            # we can assume that we have found our screen
            if len(approx) == 4:
                screenCnt = approx
            break

        # Loop capture section and check for contours, if 0, loop again, if 1, break and continue.

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

    # Read the number plate and removes spaces and special characters.
    text = pytesseract.image_to_string(Cropped, config='--psm 11')
    for k in text.split("\n"):
        text = (re.sub(r"[^a-zA-Z0-9]+", '', k))
    print("Detected Number is:", text)  # Prints out the OCR output with the text processing.

    # Open the plates.json file and looks for a text match
    with open('plates.json') as json_file:
        data = json.load(json_file)
        for p in data['plates']:
            a = p['plate']
            for k in a.split("\n"):
                plateFix = (re.sub(r"[^a-zA-Z0-9]+", '', k))  # Removes special characters and spaces
            if plateFix == text:
                print("Plate '" + p['plate'] + "' is in the database")  # Prints out the plate found in the database.
                now = datetime.now()  # Gets current time
                current_time = now.strftime("%H-%M-%S")  # Saves current time to string
                if path.exists("output/images"):  # Checks for image save path
                    os.chdir('output/images/')  # If true, change directory to img output
                else:
                    os.makedirs("output/images/")  # If false, create the directory
                    os.chdir('output/images/')  # Change directory to img output
                fileName = text + '_-_' + current_time + '.jpg'  # Creates a filename for the image
                cv2.imwrite(fileName, img, params=None)  # Writes image to file
                #
                # This space can be used to activate the garage door/gate either
                # by using a relay module or another method. More data can be logged if needed
                # by grabbing more info from the JSON file. i.e. Number of times the vehicle has visited,
                # when it arrived and left etc..
                #
                # exit(0)  # Ends program with exit code 0. REMOVE FOR FINAL IMPLEMENTATION!!!

    # cv2.imshow('Cropped', Cropped)  # Shows the cropped image.
    # cv2.imshow('image', img)  # Shows image with detection.

    #  key = cv2.waitKey(1)  # Wait for the Key 'C' to be pressed
    time.sleep(1)  # Pauses script for 1 second before repeating. Reduce this time for final version
    screenCnt = None  # Set the screenCnt value to 'None' to reset the parameter.
    cv2.destroyAllWindows()  # Close the image windows if any are open.
