import socket
from CANSPEC import CANFRAME


class UDPCANListener:
    def __init__(self, UDP_IP, UDP_PORT, debug = False):
        #create variables and assign them
        self.UDP_IP             = UDP_IP
        self.UDP_PORT           = UDP_PORT
        self.debug              = debug
        self.data               = b''
        self.addr               = ''
        self.readable_data      = ""
        self.data_bytes_list    = []

        # Create a UDP socket
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        #initialize the UDP Socket
        self.initUDPConnection()

    def initUDPConnection(self):
        # Bind the socket to the specified IP address and port
        self.sock.bind((self.UDP_IP, self.UDP_PORT))

        print(f"Listening on {self.UDP_IP}:{self.UDP_PORT}...")

    def receiveFromUDP(self):
        # Receive data from the socket
        self.data, self.addr = self.sock.recvfrom(1024)
        self.readable_data = ' '.join(f'{byte:02X}' for byte in self.data)  # make bytes format more readable

        self.data_bytes_list = ['{:02X}'.format(byte) for byte in self.data]

        self.displayReadableData(self.data_bytes_list, self.readable_data, self.addr)

    def closeSocket(self):
        # Close the socket when Ctrl+C is pressed
        print("Closing the UDP socket...")
        self.sock.close()

    def displayReadableData(self, data_bytes_list, readable_data, addr):
        canFrame = CANFRAME.CANFRAME(data_bytes_list)

        # Print the received data in byte form
        if self.debug: print(f"Received readable data: {readable_data}")
        print(
            f"Received data (Raw Bytes): Identifier: {canFrame.CANMSGIdentifier.identifier_list} Data length: {canFrame.CANMSGDlc} Data: {canFrame.CANMSGData}  from {addr}")

        canFrame.explainIdentifier()

        canFrame.printData()

#        del canFrame #usually not necessary, garbage collector will handle memory

