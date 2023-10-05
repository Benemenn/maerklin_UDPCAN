import socket
import binascii

# Define the UDP server's IP address and port
UDP_IP = "192.168.0.84" #this is your computers IP adress !
UDP_PORT = 15730

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
        canFrame = CANFRAME(data_bytes_list)

        # Print the received data in byte form
        if self.debug: print(f"Received readable data: {readable_data}")
        print(
            f"Received data (Raw Bytes): Identifier: {canFrame.CANMSGIdentifier.identifier_list} Data length: {canFrame.CANMSGDlc} Data: {canFrame.CANMSGData}  from {addr}")

        canFrame.explainIdentifier()

        canFrame.printData()

#        del canFrame #usually not necessary, garbage collector will handle memory


class CANFRAME:
    def __init__(self, data_bytes_list):
        self.CANMSGIdentifier = CANIDENTIFIER(list(data_bytes_list)[:4])
        self.CANMSGDlc = list(data_bytes_list)[4:5]
        self.CANMSGData = list(data_bytes_list)[5:14]

    def printData(self):
        print("Data: ", end="")
        for databyte in self.CANMSGData:
            print(f"{hex(int(databyte, 16))} ", end="")
        print("\n")

    def explainIdentifier(self):
        self.CANMSGIdentifier.explainIdentifier()

class CANIDENTIFIER:
    def __init__(self, identifier_list):
        self.identifier_list = identifier_list
        self.msgPrio1   = ""
        self.msgPrio2   = ""
        self.msgCmd     = ""
        self.msgResp    = ""
        self.msgHash    = ""
        self.debug = False

    def explainIdentifier(self):

        completeIdentifierHEX = self.identifier_list[0] + self.identifier_list[1] + self.identifier_list[2] + self.identifier_list[3]
        # print(f'Complete CAN IDENTIFIER in HEX: {completeIdentifierHEX}')

        completeIdentifierBINARY = format(int(completeIdentifierHEX, 16), '032b')
        print(f"Complete CAN IDENTIFIER in BINARY: {completeIdentifierBINARY}")

        self.msgPrio1 = completeIdentifierBINARY[3:5]
        self.msgPrio2 = completeIdentifierBINARY[5:7]
        self.msgCmd = completeIdentifierBINARY[7:15]
        self.msgResp = completeIdentifierBINARY[15:16]
        self.msgHash = completeIdentifierBINARY[16:22] + completeIdentifierBINARY[25:]

        # print(f"In BINARY: Prio1: {msgPrio1}, Prio2: {msgPrio2}, Cmd: {msgCmd}, Resp: {msgResp}, Hash: {msgHash}")
        print(
            f"In HEX: Prio1: {hex(int(self.msgPrio1, 2))}, Prio2: {hex(int(self.msgPrio2, 2))}, Cmd: {hex(int(self.msgCmd, 2))}, Resp: {hex(int(self.msgResp, 2))}, Hash: {hex(int(self.msgHash, 2))}")

        if self.debug:
            for hex_string in self.identifier_list:
                binary_string = bin(int.from_bytes(binascii.unhexlify(hex_string), byteorder='big'))

                print(f'Hexadecimal: {hex_string}, Binary: {binary_string}')

def main():
    udpCanListener = UDPCANListener(UDP_IP, UDP_PORT)

    while True:
        try:
            udpCanListener.receiveFromUDP()

        except KeyboardInterrupt:
            udpCanListener.closeSocket()
            break

if __name__ == "__main__":
    main()


