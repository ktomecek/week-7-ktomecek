##################################################################################
# Written by Karl Tomecek 06/23/2019                                             #
# Program Name: ca.py                                                            #
# Week 7 Assignment                                                              #
# Comments: Modeled from code retrieved from                                     #
# https://stackoverflow.com/questions/7749341/basic-python-client-socket-example #
#                                                                                #
##################################################################################

#Import Socket library
import socket


def clearScreen():
    for i in range(15): #clear the screen
        print('\n')

def main():
    #'Clear' the screen
    clearScreen()
    
    serverName = ''
    publicKey = ''
    # Start listening for an input stream
    serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serversocket.bind(('localhost', 9700))
    serversocket.listen(5) # become a server socket, maximum 5 connections

    #Main processing loop
    print("CA STARTED...LISTENING ON PORT 9700")
    while True:
        #Open a connection on port 9700
        connection, address = serversocket.accept()
        #Wait for inbound data
        buf = connection.recv(64).decode("utf-8")
        #If data is received, process it as per the assignment
        if len(buf) > 0:
            if ('client' in buf):
                print('Client seeks public key validation')
                if (serverName in buf):
                    print('Sending public key to client', buf)
                    connection.sendall(bytes(publicKey, 'UTF-8'))
            else:
                # Register server name
                serverName, publicKey = buf.split(',')
                #for this program, just user single servername.  Can be list in practice.
                print('Incoming Server Name Registration - Server: ', serverName)
                print('Incoming Server Public Key: ', publicKey)
                connection.send(bytes('Server Name Registered','UTF-8'))
                print('\nCurrent Registry:')
                print ('Server Name: ', serverName,'Public Key: ', publicKey)

#Start the CA server
main()