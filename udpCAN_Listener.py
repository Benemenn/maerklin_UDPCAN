import socket
import binascii
import re

# Define the UDP server's IP address and port
UDP_IP = "192.168.0.79"
UDP_PORT = 15730

debug = True

# Create a UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Bind the socket to the specified IP address and port
sock.bind((UDP_IP, UDP_PORT))

print(f"Listening on {UDP_IP}:{UDP_PORT}...")

while True:
    try:
        # Receive data from the socket
        data, addr = sock.recvfrom(1024)
        readable_data = ' '.join(f'{byte:02X}' for byte in data) #make bytes format more readable

        data_bytes_list = ['{:02X}'.format(byte) for byte in data]


        CANMSGIdentifier = list(data_bytes_list)[:4]
        CANMSGDlc = list(data_bytes_list)[4:5]
        CANMSGData = list(data_bytes_list)[5:14]

        # Print the received data in byte form
        if debug: print(f"Received readable data: {readable_data}")
        print(f"Received data (Raw Bytes): Identifier: {CANMSGIdentifier} Data length: {CANMSGDlc} Data: {CANMSGData}  from {addr} \n")


        #print(f"transfered into list: {data_bytes_list}")

    except KeyboardInterrupt:
        # Close the socket when Ctrl+C is pressed
        print("Closing the UDP socket...")
        sock.close()
        break

