#!/usr/bin/python

import socket
import threading
import logging
import json
import time
import servomotor
import response
import thermometer
import camera
import pm2_5
import config
import light

logging.basicConfig(level=logging.DEBUG)

def handle_request(client_socket):
    request = json.loads(client_socket.recv(1024))
    logging.debug("Reveived: %s", request)
    client_socket.send("ACK!\r\n")        # send back a packet
    client_socket.close()
    text = request['message']['text'].lower()
    sender_id = request['sender']['id'].encode('utf8')
    if u'pic' in text:
        camera.response_picture(sender_id)
    elif u'pm' in text:
        response.response_text(sender_id, pm2_5.PM_DB.discription())
    elif u'temp' in text or u'tmp' in text:
        thermometer.response_temperature(sender_id)
    elif u'turn left' in text:
        servomotor.turn_left()
    elif u'turn right' in text:
        servomotor.turn_right()
    elif u'light on' in text:
        light.on()
    elif u'light off' in text:
        light.off()
    else:
        response.response_text(sender_id, "Try: picture, PM2.5, temperature.")

def server_thread(server):
    while True:
        client, addr = server.accept()
        logging.debug("Accepted connection from: %s:%d", addr[0], addr[1])
        client_handler = threading.Thread(target=handle_request, args=(client,))
        client_handler.start()

def run_server(bind_ip, bind_port):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((bind_ip, bind_port))
    server.listen(5)
    logging.debug("Listening on %s:%d", bind_ip, bind_port)
    server_handler = threading.Thread(target=server_thread, args=(server,))
    server_handler.start()

def main():
    run_server(config.BIND_IP, config.BIND_PORT)
    pm2_5.start_sensor()
    need_check = True
    while True:
        time.sleep(60)
        if time.localtime().tm_hour in (8, 12, 16, 20):
            if need_check == True:
                print "==============check PM avg==============="
                print pm2_5.PM_DB.avg
                pm_1hr = pm2_5.PM_DB.avg[60][1]
                pm_10hr = pm2_5.PM_DB.avg[600][1]
                msg = None
                if pm_1hr > 55 or pm_10hr > 55:
                    msg = 'Air quality: RED - Unhealthy'
                elif pm_1hr > 30 or pm_10hr > 30:
                    msg = 'Air quality: Orange - Unhealthy for Sensitive Groups'
                elif pm_1hr > 12 or pm_10hr > 12:
                    msg = 'Air quality: Yellow - Moderate'
                if msg is not None:
                    for id in config.MESSGENGER_ID_LIST:
                        response.response_text(id, msg)
            need_check = False
        else:
            need_check = True

if __name__ == '__main__':
    main()
