import socket
import time

# Define the target IP address and port
UDP_IP = "192.168.0.167"  # Replace with the target IP address
UDP_PORT = 15731  # Replace with the target port number

# Create a UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

try:
    # Message to send as bytes

    message = bytes([0x00, 0x00, 0x47, 0x6A, 0x05, 0x00, 0x00, 0x00, 0x00, 0x01, 0x00, 0x00, 0x00])  # disable emergency-halt and drive
    sock.sendto(message, (UDP_IP, UDP_PORT))

    #message = bytes([0x00, 0x01, 0x73, 0x32, 0x05, 0x63, 0x73, 0x4B, 0x98, 0x01, 0x00, 0x00, 0x00])  #?
    #sock.sendto(message, (UDP_IP, UDP_PORT))

    #message = bytes([0x00, 0x01, 0x73, 0x32, 0x05, 0x00, 0x00, 0x00, 0x00, 0x01, 0x00, 0x00, 0x00])  # disable emergency-halt but dont drive
    #sock.sendto(message, (UDP_IP, UDP_PORT))

    print(f"Sent message to {UDP_IP}:{UDP_PORT}: {message}")

finally:
    # Close the socket when done
    sock.close()
