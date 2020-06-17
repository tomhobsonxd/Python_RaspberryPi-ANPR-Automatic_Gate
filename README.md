## Python ANPR using OpenCV

ANPR (Automatic Number Plate Recognition) using OpenCV (opencv-python) for image processing and Tesseract (pytesseract) for OCR
***
## Installation

The steps below assume you already have Python and `pip` installed. I am using Python 3.8 for this example as it is the most up-to-date at the time of creation.

### OpenCV-Python, Tesseract & pytesseract
***
#### Open-CV-python

To install the opencv-python libraries, run:

`pip install opencv-python`

Then install imutils using,

`pip install imutils`
***
#### Tesseract

##### Windows

Follow the guide from here: [Tesseract at UB Mannheim](https://github.com/UB-Mannheim/tesseract/wiki)

##### Linux/MacOS

Follow the guide from here: [Tesseract-OCR](https://github.com/tesseract-ocr/tesseract/wiki)
***
#### pytesseract

To install, run:

`pip install pytesseract`


## Useful Information

When setting up the image source with:

`capture = cv2.VideoCapture(0)`

The function `cv2.VideoCapture()` takes multiple arguments.

The following arguments can be used:
- `VideoCapture(0)` uses the deafult camera
- `VideoCapture(stream:\\ip.address:port)` uses a web stream
- `VideoCapture("path/to/video/file")` uses a video/motion-jpeg file

Read about it here: [VideoCapture::VideoCapture](https://docs.opencv.org/2.4/modules/highgui/doc/reading_and_writing_images_and_video.html#videocapture)
and here: [VideoCapture()](https://docs.opencv.org/3.4/d8/dfe/classcv_1_1VideoCapture.html#a57c0e81e83e60f36c83027dc2a188e80)
