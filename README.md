# Listen to Märklins CAN-Protocol 

This is done via the UDP Gateway the CS3 is starting when it is enabled.

This repo contains python files for a listener and a sender.
The listener interpretes the data that comes in via udp and display it readable.
The sender imitates the CS3 commands to control the model train. The CAN commands that are sent via UDP to the CS3 are interpreted and put on the CAN bus.

The Märklin CAN documentation can be found here : [Märklin CAN](https://streaming.maerklin.de/public-media/cs2/cs2CAN-Protokoll-2_0.pdf)
