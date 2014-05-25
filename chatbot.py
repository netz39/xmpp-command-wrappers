#!/usr/bin/python2.7

import xmpp
import argparse
import sys
import module_ampel as ampel
from parser import Command


def messageCB(conn, msg):
    reply = None
    user = xmpp.protocol.JID(msg.getFrom())
    print "%s: %s\n" %(user, msg.getBody())
    # answer with same Thread ID ...
    print msg.getType()
    cmd = Command(msg.getBody())
    print cmd.getToken()
    print messageCB.tokens
    if str(cmd.getToken()) in messageCB.tokens:
        to = messageCB.tokens[str(cmd.getToken())]
        to_cmd = Command(to.getBody())
        cmd.setToken(to_cmd.getToken())
        reply = to.buildReply(text = cmd.toString())
        reply.setType("chat")
        print reply.getBody()
        print reply.getThread()
        print reply.getType()
        conn.send(reply)
        return None

    messageCB.tokens[str(messageCB.token)] = msg
    if cmd.getPrefix() == "ampel":
        ampel.process(cmd, conn, messageCB.token)
    messageCB.token += 1

messageCB.token = 0
messageCB.tokens = {}

def stepOn(conn):
    """ parse next piece of stuff """
    try:
        conn.Process(1)
    except KeyboardInterrupt: return 0
    return 1

def goOn(conn):
    """ loopy loop"""
    while stepOn(conn):
        pass

if __name__ == '__main__':

    # argparsing ...
    parser = argparse.ArgumentParser(description="Python Bot wrapping xmpp-Protocols into easier xmpp-Protocols")
    parser.add_argument('-jid','--jabber_id', help='Jabber-ID, foo@example.org', default=None)
    parser.add_argument('-pw', '--password', help='password', default=None)
    args = parser.parse_args()

    # connect to jabber server
    jid = xmpp.JID(args.jabber_id)
    conn = xmpp.Client(jid.getDomain(), debug=[])
    connres = conn.connect()
    if not connres:
        print "Unable to connect to server %s!"%jid.getDomain()
        sys.exit(1)
    else:
        print "Connected to %s"%jid.getDomain()
    if connres<>'tls':
        print "Warning: unable to estabilish secure connection - TLS failed!"
        sys.exit(2)
    # authenticate
    authres = conn.auth(jid.getNode(),args.password)
    if not authres:
        print "Unable to authenticate, check user/password"
        sys.exit(1)

    # register stuff
    conn.RegisterHandler('message',messageCB)
    conn.sendInitPresence()
    print "Bot started."
    goOn(conn)
