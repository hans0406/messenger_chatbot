import response
import subprocess

subprocess.call(['/sbin/modprobe', 'w1-gpio'])
subprocess.call(['/sbin/modprobe', 'w1-therm'])

def response_temperature(reciepter_id):
    """Read temperature from SEN08011P"""
    with open('/sys/bus/w1/devices/28-00000569c7dd/w1_slave', 'r') as thermo_file:
        temp = thermo_file.readlines()[-1][-6:-2]
    response.response_text(reciepter_id, "Temperature: {}.{}\r\n".format(temp[:2], temp[2:]))
