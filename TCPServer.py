from socket import *
import re
#assign port number
serverPort = 12002
#TCP socket creation
serverSocket = socket(AF_INET, SOCK_STREAM)
#bind port to socket
serverSocket.bind(('', serverPort))
#listen to the socket in order to recieve packets
serverSocket.listen(1)
print ("The server is ready to receive\n")
while True:
    #create socket get address
    connectionSocket, addr = serverSocket.accept()
    #recieve message form client
    message = connectionSocket.recv(1026)
    print ("-->> At Server receved message is: '" + message.decode() + "'")
    splitmsg = re.split("([+-/*])", message.replace(" ", ""))
    #i used penalties to keep track of number or operation errors in client message
    penalties = 0
    #if the length of the array is more than 3 there is an issue its not in format number operator number
    if(not(len(splitmsg)==3)):
        penalties = penalties + 1
        print("!!!!!!!!!!invalid input!!!!!!!!!!\n")
        print ("<<-- At Server modified message to send back: '" + "status code 300" + "\n")
        #message sent back in format of [result] [status code]
        connectionSocket.send("-1 300")
    else:
        #number(not a number) operator number
        if((splitmsg[0]).isdigit() == False):
            penalties = penalties + 1
            print("!!!!!!!!!!invalid first input not correct length!!!!!!!!!!\n")
            print ("<<-- At Server modified message to send back: '"+ "-1 \n"  + "status code 300" + "\n")
            #message sent back in format of [result] [status code]
            connectionSocket.send("-1 300")
        #number operator number(not a number)
        if((splitmsg[2]).isdigit() == False):
            penalties = penalties + 1
            print("!!!!!!!!!!invalid second input!!!!!!!!!!\n")
            print ("<<-- At Server modified message to send back: '"+ "-1 \n"  + "status code 300" + "\n")
            #message sent back in format of [result] [status code]
            connectionSocket.send("-1 300")
        #number operator(not an operator) number
        if(not(splitmsg[1] == '-' or splitmsg[1] == '+' or splitmsg[1] == '*' or splitmsg[1] == '/')):
            penalties = penalties + 1
            print("!!!!!!!!!!invalid operation input!!!!!!!!!!\n")
            print ("<<-- At Server modified message to send back: '"+ "-1 \n" + "status code 300" + "\n")
            #message sent back in format of [result] [status code]
            connectionSocket.send("-1 300")

    #message input violates no restrictions above
    if(penalties == 0):
        operator = splitmsg[1]
        #if subtract
        if operator == '-' :
            modifiedMessage = str(int(splitmsg[0]) - int(splitmsg[2]))
            print ("<<-- At Server modified message to send back: '" + modifiedMessage + "'\n"+ "status code 200" + "\n")
            #message sent back in format of [result] [status code]
            connectionSocket.send(str(modifiedMessage+" 200"))
        #if add
        if operator == '+' :
            modifiedMessage = str(int(splitmsg[0]) + int(splitmsg[2]))
            print ("<<-- At Server modified message to send back: '" + modifiedMessage + "'\n"+ "status code 200" + "\n")
            #message sent back in format of [result] [status code]
            connectionSocket.send(str(modifiedMessage+" 200"))
        #if multiply
        if operator == '*' :
            modifiedMessage = str(int(splitmsg[0]) * int(splitmsg[2]))
            print ("<<-- At Server modified message to send back: '" + modifiedMessage + "'\n"+ "status code 200" + "\n")
            #message sent back in format of [result] [status code]
            connectionSocket.send(str(modifiedMessage+" 200"))
        #if divide but not zero
        if ((operator == '/') and (not (int(splitmsg[2]) == 0)) ):
            modifiedMessage = str(int(splitmsg[0]) / int(splitmsg[2]))
            print ("<<-- At Server modified message to send back: '" + modifiedMessage + "'\n"+ "status code 200" + "\n")
            #message sent back in format of [result] [status code]
            connectionSocket.send(str(modifiedMessage+" 200"))
        #if divide by zero then not valid operation
        if((operator == '/') and (int(splitmsg[2]) == 0)):
            modifiedMessage = -1
            print("!!!!!!!!!!divide by 0!!!!!!!!!!\n")
            print ("<<-- At Server modified message to send back: '"+ "-1 \n"  + "status code 300" + "\n")
            #message sent back in format of [result] [status code]
            connectionSocket.send("-1 300")
