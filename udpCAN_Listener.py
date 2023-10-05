import socket
import binascii

# Define the UDP server's IP address and port
UDP_IP = "192.168.0.79" #this is your computers IP adress !
UDP_PORT = 15730

class UDPCANListener:
    def __init__(self, UDP_IP, UDP_PORT, debug = False):
        self.UDP_IP     = UDP_IP
        self.UDP_PORT   = UDP_PORT
        self.debug      = debug
        self.initUDPConnection()
        self.data = b''
        self.addr = ''
        self.readable_data = ""
        self.data_bytes_list = []

    def initUDPConnection(self):
        # Create a UDP socket
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        # Bind the socket to the specified IP address and port
        self.sock.bind((UDP_IP, UDP_PORT))

        print(f"Listening on {UDP_IP}:{UDP_PORT}...")

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
        CANMSGIdentifier = list(data_bytes_list)[:4]
        CANMSGDlc = list(data_bytes_list)[4:5]
        CANMSGData = list(data_bytes_list)[5:14]

        # Print the received data in byte form
        if self.debug: print(f"Received readable data: {readable_data}")
        print(
            f"Received data (Raw Bytes): Identifier: {CANMSGIdentifier} Data length: {CANMSGDlc} Data: {CANMSGData}  from {addr}")

        self.explainIdentifier(CANMSGIdentifier)

        print("Data: ", end="")
        for databyte in CANMSGData:
            print(f"{hex(int(databyte, 16))} ", end="")
        print("\n")

    def explainIdentifier(self, canIdentifier):

        completeIdentifierHEX = canIdentifier[0] + canIdentifier[1] + canIdentifier[2] + canIdentifier[3]
        # print(f'Complete CAN IDENTIFIER in HEX: {completeIdentifierHEX}')

        completeIdentifierBINARY = format(int(completeIdentifierHEX, 16), '032b')
        print(f"Complete CAN IDENTIFIER in BINARY: {completeIdentifierBINARY}")

        msgPrio1 = completeIdentifierBINARY[3:5]
        msgPrio2 = completeIdentifierBINARY[5:7]
        msgCmd = completeIdentifierBINARY[7:15]
        msgResp = completeIdentifierBINARY[15:16]
        msgHash = completeIdentifierBINARY[16:22] + completeIdentifierBINARY[25:]

        # print(f"In BINARY: Prio1: {msgPrio1}, Prio2: {msgPrio2}, Cmd: {msgCmd}, Resp: {msgResp}, Hash: {msgHash}")
        print(
            f"In HEX: Prio1: {hex(int(msgPrio1, 2))}, Prio2: {hex(int(msgPrio2, 2))}, Cmd: {hex(int(msgCmd, 2))}, Resp: {hex(int(msgResp, 2))}, Hash: {hex(int(msgHash, 2))}")

        if self.debug:
            for hex_string in canIdentifier:
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


