#!/usr/bin/python

import urllib
import urllib2
import logging
import subprocess
import config

def response_image(receipter_id, img_path, img_type):
    subprocess.call([
        'curl',
        '-F', 'recipient={{"id":{}}}'.format(receipter_id),
        '-F', 'message={"attachment":{"type":"image", "payload":{}}}',
        '-F', 'filedata=@{};type=image/{}'.format(img_path, img_type),
        'https://graph.facebook.com/v2.6/me/messages?access_token={}'.format(config.TOKEN)])

def response_text(receipter_id, text):
    """Send text to sender_id"""
    logging.debug("Send message to %s: %s", type(receipter_id), type(text))
    url = 'https://graph.facebook.com/v2.6/me/messages'
    values = {
        'message': {'text': text},
        'recipient': {'id': receipter_id},
        'access_token': config.TOKEN
    }
    data = urllib.urlencode(values)
    logging.debug("Data: %s", data)
    req = urllib2.Request(url, data.encode('utf8'))
    logging.debug("HTTP Request: %s", req)
    response = urllib2.urlopen(req)
    result = response.read()
    logging.debug(result)
