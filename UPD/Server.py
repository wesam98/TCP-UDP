##########################################################
#                Functions of the UDP Server            #
# Create and bind a socket to an IP and port.           #
# Wait for data from a client and process it.           #
# Execute received commands and send back responses.    #
# Maintain communication until the client stops.        #
##########################################################

import socket
import sys

# Create a socket
def create_socket():
    try:
        global host
        global port
        global s

        host = "192.168.0.102"
        port = 50000
        # AF_INET means we will use IPV4, SOCK_DGRAM means we will use UDP Protocol
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        print("Socket Created")

    except socket.error as msg:
        print("Socket creation failed" + str(msg))

# Binding the socket
def bind_socket():
    retries = 3
    while retries > 0:
        try:
            global host
            global port
            global s

            print("Socket binding started on port " + str(port))
            s.bind((host, port))  # Bind the socket to the specified host and port
            break  # Successfully bound, exit the loop
        except socket.error as msg:
            retries -= 1
            if retries > 0:
                print(f"Socket binding failed: {msg}. Retrying... {retries} attempts left.")
            else:
                print("Failed to bind the socket after 3 attempts. Exiting...")
                sys.exit()

# Send commands to the client
def send_command():
    while True:
        # infinite loop to be able to send many commands to client
              cmd = input("Enter any command: ")
              if cmd == "quit":
                  print("Closing the connection...")
                  s.close()
                  sys.exit()
            # data is sent through the network in form of bits (encoded)
              if  len(str.encode(cmd)) > 0:
                  conn, client_address = s.recvfrom(1024)
                  print(f"Connected to client at {client_address}")
                  s.sendto(cmd.encode("utf-8"),client_address)
                  # receiving the client response and concert it into readable format "utf-8", 1024 size of each chunk of data
                  client_response = str(s.recv(1024), "utf-8")
                  print(f"client_response: {client_response}", end="") #ens="" to move to a new line after printing



# Main function
def main():
    create_socket()
    bind_socket()
    send_command()


main()