xmpp-command-wrappers
=====================

abstraction layer for xmpp-controlled devices

xmpp Kontrolle für Ampel und Tür sinnvoll rekodieren

commads:
ampel.set
$token
1 color
red|green|none
[1 modus
blink|solid]
ampel.status
$token

## Requirements:

xmpppy – sadly this did not install with pip, but did with easy_install.
argparse – for Command-Line-Argument-Parsing

