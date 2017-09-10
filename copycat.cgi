#!/usr/bin/python3

import sys, os
import codecs
import json
import logging
import urllib
import urllib.request

VERIFY_TOKEN = 'TOKEN'
PAGE_ACCESS_TOKEN = 'TOKEN'

def parse_query():
    from urllib import parse
    url = os.environ["REQUEST_URI"]
    query = parse.parse_qs(parse.urlparse(url).query)
    return query

def send_text_message(sender_id, text):
    logging.debug("send message")
    logging.debug(text)
    url = 'https://graph.facebook.com/v2.6/me/messages'
    values = {'message': {'text': text},
              'recipient': {'id': sender_id},
              'access_token': PAGE_ACCESS_TOKEN}
    data = urllib.parse.urlencode(values)
    req = urllib.request.Request(url, data.encode('utf8'))
    response = urllib.request.urlopen(req)
    result = response.read()
    logging.debug(result)

def received_message(event):
    logging.debug('message received')
    if 'text' in event['message'] and event['message']['text']:
        send_text_message(event['sender']['id'], event['message']['text'])
    elif 'attachments' in event['message']:
        send_text_message(event['sender']['id'], 'I got some interesting thing')
        logging.debug('non-text received')

def main():
    print("Content-Type: text/html")
    print("")
    query = parse_query()
    logging.debug(query)
    if 'hub.mode' in query and 'hub.verify_token' in query and 'hub.challenge' in query:
        if 'subscribe' in query['hub.mode'] and VERIFY_TOKEN in query['hub.verify_token']:
            print(query['hub.challenge'][0], end='')
            return
    raw_data = sys.stdin.read()
    logging.debug(raw_data)
    form = json.loads(raw_data)
    if 'page' == form['object']:
        for entry in form['entry']:
            for event in entry['messaging']:
                if 'message' in event:
                    received_message(event)
                    return
                else:
                    logging.info("Received unknown event")
                    logging.info(event)

    print('Something wrong')


sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())
with open("chatbot.err", "a") as log:
    logging.basicConfig(filename='chatbot.log', level=logging.DEBUG)
    sys.stderr = log
    main()

