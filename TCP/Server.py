##########################################################
#                Functions of the Server                 #
# Create a socket.                                       #
# Bind the socket to an IP and port.                    #
# Listen for incoming client connections.               #
# Accept a connection and communicate with the client.  #
# Send commands to the client and process responses.    #
# Close the connection after finishing communication.   #
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
        # AF_INET means we will use IPV4, SOCK_STREAM means we will use TCP Protocol
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("Socket Created")

    except socket.error as msg:
        print("Socket creation failed" + str(msg))

# Binding the socket and listening for the connection
def bind_socket():
    retries = 3
    while retries > 0:
        try:
            global host
            global port
            global s

            print("Socket binding started on port " + str(port))
            s.bind((host, port))  # Bind the socket to the specified host and port
            s.listen(5)  # 5 is the max number of connections the server will be waiting for
            print(f"Server is listening on port {port}...")
            break  # Successfully bound, exit the loop
        except socket.error as msg:
            retries -= 1
            if retries > 0:
                print(f"Socket binding failed: {msg}. Retrying... {retries} attempts left.")
            else:
                print("Failed to bind the socket after 3 attempts. Exiting...")
                sys.exit()


# Establish connection with a client
def socket_accept(server_socket):
    # s.accept returns with client socket, tuple contains client's IP, port
    conn, address = s.accept()
    print("Connection is established! IP = " + address[0] + " Port = " + str(address[1]))
    send_command(conn)
    conn.close()

# Send commands to the client
def send_command(conn):
    while True:          # infinite loop to be able to send many commands to client
              cmd = input("Enter any command to send to the client ")
              if cmd == "quit":
                  print("Closing the connection...")
                  conn.close()
                  s.close()
                  sys.exit()
            # data is sent through the network in form of bits (encoded)
              if  len(str.encode(cmd)) > 0:
                 conn.send(cmd.encode("utf-8"))
                  # receiving the client response and concert it into readable format "utf-8", 1024 size of each chunk of data
                 client_response = str(conn.recv(1024), "utf-8")
                 print(f"client_response: {client_response}", end="") #ens="" to move to a new line after printing

def main():
    create_socket()
    bind_socket()
    socket_accept(s)


main()