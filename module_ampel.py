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

ampel_xmpp_account = "i3c.wittgenstein@platon"
SET_LIGHT = 0x02
GET_LIGHT = 0x01

def color_from_i2c_byte(i2c_code):
    """compute color_from_i2c_byte"""
    i2c_byte = int(i2c_code, 16) & 0x3
    if i2c_byte == 2:
        return "green"
    if i2c_byte == 1:
        return "red"
    return "none"

def modus_from_i2c_byte(i2c_code):
    """compute color_from_i2c_byte"""
    i2c_byte = int(i2c_code, 16) & 0x8
    if i2c_byte == 0:
        return "blink"
    return "solid"


def translate_response(cmd):
    """docstring for translate_response"""
    response = Command()
    response.command = "ampel.response"
    response.setToken(cmd.getToken())
    try:
        response.params["color"] = color_from_i2c_byte(cmd.params["i2c.response"])
        response.params["modus"] = modus_from_i2c_byte(cmd.params["i2c.response"])
    except KeyError, k:
        print k
        response.params["error"] = "i2c.response missing"
    return response

def send_command_to_ampel(conn, token, i2c_command, data=None):
    """ send the new command to the ampel """
    cmd = Command("i3c.call\n%s\n1 device\n0x20\n1 command\n%s" %(token, hex(i2c_command)))
    if data:
        cmd.params["data"] = data
    cmd = xmpp.Message(ampel_xmpp_account, cmd.toString())
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
    send_command_to_ampel(conn, token, SET_LIGHT, data=hex(i2c_code))

def handle_status_command(command, conn, token):
    """handle status command -> send back current status"""
    print "Request satus from ampel"
    send_command_to_ampel(conn, token, GET_LIGHT)


def process(command, conn, token):
    """ process message send to ampel """
    if command.getPrefix() == "ampel":
        print command.getParams()
        if command.command == "ampel.set":
            handle_set_command(command, conn, token)
        if command.command == "ampel.status":
            handle_status_command(command, conn, token)
    return None
