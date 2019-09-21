#!/usr/local/bin/python3

"""Cgi for messenger
This cgi just reply same contex(copy cat), And pass message to reponser
"""
import sys
import os
import codecs
import json
import logging
import urllib
import urllib.request
from urllib import parse
import socket
import config

def notify_responser(request):
    """Responser can run in same machine or not"""
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((config.RESPONSER_IP, config.RESPONSER_PORT))
    client.send(request.encode('utf8'))
    response = client.recv(4096)
    logging.debug("Response: %s", response)
    client.close()

def parse_query():
    try:
        url = os.environ["REQUEST_URI"]
        query = parse.parse_qs(parse.urlparse(url).query)
    except KeyError as e:
        query = {}
    return query

def send_text_message(sender_id, text):
    logging.debug("Send message to %s: %s", sender_id, text)
    url = 'https://graph.facebook.com/v2.6/me/messages'
    values = {
        'message': {'text': text},
        'recipient': {'id': sender_id},
        'access_token': config.PAGE_ACCESS_TOKEN
    }
    data = urllib.parse.urlencode(values)
    req = urllib.request.Request(url, data.encode('utf8'))
    response = urllib.request.urlopen(req)
    result = response.read()
    logging.debug(result)

def received_message(event):
    """Reply same message."""
    logging.debug('Message received')
    if 'text' in event['message'] and event['message']['text']:
        send_text_message(event['sender']['id'], event['message']['text']) #just a copy cat
        request = json.dumps(event)
        notify_responser(request) #remove this line, if no responser
    elif 'attachments' in event['message']:
        send_text_message(event['sender']['id'], 'I got some interesting thing')
        logging.debug('Attachments received: %s',)

def main():
    print("Content-Type: text/html")
    print("")
    query = parse_query()
    logging.debug("Query: %s", query)
    if 'hub.mode' in query and 'hub.verify_token' in query and 'hub.challenge' in query:
        if 'subscribe' in query['hub.mode'] and config.VERIFY_TOKEN in query['hub.verify_token']:
            print(query['hub.challenge'][0], end='')
            return
    raw_data = sys.stdin.read()
    logging.debug("HTPP POST: %s", raw_data)
    form = json.loads(raw_data)
    logging.debug("JSON: %s", form)
    if form['object'] == 'page':
        for entry in form['entry']:
            for event in entry['messaging']:
                if 'message' in event:
                    received_message(event)
                    return
                else:
                    logging.info("Received unknown event: %s", event)
    print('Something wrong!')


logging.basicConfig(filename='chatbot.log', level=logging.DEBUG)
sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())
try:
    main()
except:
    logging.exception("Exception!")
