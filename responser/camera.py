#!/usr/bin/python

import picamera
import response

TMP_IMAGE = 'image.jpg'
TMP_IMAGE_TYPE = 'jpeg'

def response_picture(receipter_id):
    response.response_text(receipter_id, "taking picture...")
    try:
        camera = picamera.PiCamera()
        camera.vflip = true
        camera.resolution = (2592, 1944)
        camera.capture(TMP_IMAGE)
    finally:
        camera.close()
    response.response_image(receipter_id, TMP_IMAGE, TMP_IMAGE_TYPE)
