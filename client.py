##################################################################################
# Written by Karl Tomecek 06/23/2019                                             #
# Program Name: client.py                                                        #
# Week 7 Assignment                                                              #
# Comments: Modeled from code retrieved from                                     #
# https://stackoverflow.com/questions/7749341/basic-python-client-socket-example #
#                                                                                #
# Cipher Generator from:                                                         #
# https://gist.github.com/dssstr/aedbb5e9f2185f366c6d6b50fad3e4a4                #                                                               #
##################################################################################

#Import Socket library
import socket



def clearScreen():
    for i in range(15): #clear the screen
        print('\n')
        
def sendRequestForServerNamecheck():
    clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    clientsocket.connect(('localhost', 9500))
    #Send that text to the server
    clientsocket.sendall(bytes('client', 'UTF-8'))
    #Now listen for the response
    buf = clientsocket.recv(64).decode("utf-8")
    if len(buf) > 0:
        #Now that we have server name save it in variable
        serverName = buf
        print('Getting Server Name: ', serverName)
    #Close the connection and wait for more text to send
    clientsocket.close
    return serverName

def sendCARequestForpublicKey(serverName):
    clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    clientsocket.connect(('localhost', 9700))
    #Send that text to the server
    clientsocket.sendall(bytes('client, ' + serverName, 'UTF-8'))
    #Now listen for the response
    buf = clientsocket.recv(64).decode("utf-8")
    #Now get the publicKey
    if len(buf) > 0:
        print('Now getting public Key form CA: ')
        publicKey = buf
        print ("public Key received: ", publicKey)
    #Close the connection and wait for more text to send
    clientsocket.close
    return publicKey

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

def sendCipherKeyToServer(cipherKey):
    clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    clientsocket.connect(('localhost', 9500))
    #Send cipher key to the server
    clientsocket.sendall(bytes(cipherKey, 'UTF-8'))
    print('Encrypted message sent to server')
    
def main():
    #'Clear' the screen
    clearScreen()
    serverName = sendRequestForServerNamecheck()
    publicKey = sendCARequestForpublicKey(serverName)
    sessionCipher = sessionCipherKey('session cipher key', publicKey,'e')
    sendCipherKeyToServer(sessionCipher)
    
#Start the client
main()