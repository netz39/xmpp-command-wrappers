#!/usr/bin/python2.7
from parser import Command
import xmpp

# ampel commands:
# set : 
# color [red | green | none]
# [modus : solid | blink]

# status
# [color]
# [modus]


def translate_response(cmdself):
    """docstring for translate_response"""
    
    pass

def send_command_to_ampel(conn, code, token):
    """ send the new command to the ampel """
    cmd = xmpp.Message("ampel.i3c@platon","i3c.call\n%s\n1 device\n0x20\n1 command\n0x2\n1 data\n%s" %(token, hex(code)))
    conn.send(cmd)

def handle_set_command(command, conn, token):
    """ handle set command and send stuff to i2c """
    color = None
    blink = False
    i2c_code = 0x0
    if "color" in command.params:
        color = command.params["color"]
        if color == "red":
            i2c_code = 0x1
        elif color == "green":
            i2c_code = 0x2
        if "modus" in command.params:
            if (command.params["modus"] == "blink"):
                blink = True
                i2c_code = i2c_code | 0x8
    print "blink: %s, color: %s, i2c_code: %s" %(blink, color, i2c_code)
    send_command_to_ampel(conn, i2c_code, token)

def process(command, conn, token):
    """ process message send to ampel """
    if command.getPrefix() == "ampel":
        print command.getParams()
        if command.command == "ampel.set":
            handle_set_command(command, conn, token)
    return None
