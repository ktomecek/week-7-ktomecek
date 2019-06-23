##################################################################################
# Written by Karl Tomecek 06/23/2019                                             #
# Program Name: server.py                                                        #
# Week 4 Assignment                                                              #
# Comments: Modeled from code retrieved from                                     #
# https://stackoverflow.com/questions/7749341/basic-python-client-socket-example #
#                                                                                #
##################################################################################

#Import Socket library
import socket
serverName = 'the_server'
publicKey = ''

def clearScreen():
    for i in range(15): #clear the screen
        print('\n')

def registerServerName(sname):
        clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        clientsocket.connect(('localhost', 9700))
        #Send that text to the server
        clientsocket.sendall(bytes(sname, 'UTF-8'))
        #Now listen for the response
        buf = clientsocket.recv(64).decode("utf-8")
        if len(buf) > 0:
            #Now that there is a response, display to user
            print(buf)
        #Close the connection and wait for more text to send
        clientsocket.close

def publicKeyEnter():
    getInput = True
    #'Clear' the screen
    while (getInput == True):
        clearScreen()
        print('Please enter public key to register server with:')
        newPublicKey = input()
        if len(newPublicKey) > 0:
            getInput = False
    return newPublicKey

def getIncomingMessage(publicKey):
    #Start listening for an input stream
    serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serversocket.bind(('localhost', 9500))
    serversocket.listen(5) # become a server socket, maximum 5 connections

    #Main processing loop
    print("SERVER STARTED...LISTENING ON PORT 9500")
    while True:
        #Open a connection on port 9500
        connection, address = serversocket.accept()
        #Wait for inbound data
        buf = connection.recv(64).decode("utf-8")
        #If data is received, process it as per the assignment
        if len(buf) > 0:
            print('Incoming message from a client')
            if ('client'in buf):
                print('Sending client server name: ', serverName)
                # server responds to the client with its server name
                connection.sendall(bytes(serverName, 'UTF-8'))
            else:
                receiveCipherKey = buf
                print ('Cipher Key received: ', receiveCipherKey)
                ssk = sessionCipherKey(receiveCipherKey, publicKey, 'd')
                if (ssk == 'session cipher key'):
                    print('Session cipher key decrypted successfully, communications allowed')
                else:
                    print ('Invalid session cipher key.  No communications allowed')
            # Now decrypt

   #This cipher from https://gist.github.com/dssstr/aedbb5e9f2185f366c6d6b50fad3e4a4
    #Author: flipperbw
def sessionCipherKey(txt='', key='', typ='d'):
    universe = [c for c in (chr(i) for i in range(32,127))]
    uni_len = len(universe)
    if not txt:
        print ('Needs text.')
        return
    if not key:
        print ('Needs key.')
        return
    if typ not in ('d', 'e'):
        print ('Type must be "d" or "e".')
        return
    if any(t not in universe for t in key):
        print ('Invalid characters in the key. Must only use ASCII symbols.')
        return
    ret_txt = ''
    k_len = len(key)
    for i, l in enumerate(txt):
        if l not in universe:
            ret_txt += l
        else:
            txt_idx = universe.index(l)
            k = key[i % k_len]
            key_idx = universe.index(k)
            if typ == 'd':
                key_idx *= -1
            code = universe[(txt_idx + key_idx) % uni_len]
            ret_txt += code
    return ret_txt

def main():
    publicKey = publicKeyEnter()
    registerServerName(serverName + ',' + publicKey)
    getIncomingMessage(publicKey)
    
#Start the server
main()