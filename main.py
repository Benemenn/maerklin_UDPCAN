import udpCAN_Listener as listener

# Define the UDP server's IP address and port
UDP_IP = "192.168.0.84" #this is your computers IP adress !
UDP_PORT = 15730

def main():
    udpCanListener = listener.UDPCANListener(UDP_IP, UDP_PORT)

    while True:
        try:
            udpCanListener.receiveFromUDP()

        except KeyboardInterrupt:
            udpCanListener.closeSocket()
            break

if __name__ == "__main__":
    main()