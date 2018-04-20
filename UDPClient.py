from socket import *
import time
#assign server name
serverName = 'localhost'
#assign port number
serverPort = 12000
#set up UDP connection
clientSocket = socket(AF_INET, SOCK_DGRAM)
again = "Y"
while (again=="y") | (again=="Y"):
    #get [number][operation][number] (NO SPACES)
    messagefirst = raw_input('Input math operation(note spaces are not used) [number][operation code][number]:')
    #get decimal for chance of dropping packet
    messagesecond = raw_input('Input server drop probability (eg 80 percent input: 0.8): ')
    #append message
    message = messagefirst + " " + messagesecond
    print ("\n ")
    print ("-->> At Client message to send out: '" + messagefirst + "'")
    print ("-->> At Client probability to send out: '" + messagesecond + "'")
    #setup d for timeout
    d = 0.1
    #initialize message to empty string so you can tell when its been filled
    modifiedMessage = ""
    #go through loop while message has not been initialized and timeout is still less than 2.0sec
    while(len(modifiedMessage)==0 and d<=2.0):
        try:
            #attempt to send packet to server
            clientSocket.sendto(message,(serverName, serverPort))
            #set server timeout to d
            clientSocket.settimeout(d)
            #attempt to recieve message and server address
            modifiedMessage, serverAddress = clientSocket.recvfrom(2048)
        #if timeout pops and there is no response do 2*timeout time and try again
        except Exception as msg:
            d = d * 2

    #if you succcessfully recieved a message
    if(len(modifiedMessage)>0):
        #split up message into array it is in the form of [result] [status code] (there is a space between them)
        arrmsg = modifiedMessage.decode().split()
        #result
        calcres = arrmsg[0]
        #status code
        statuscode = arrmsg[1]
        if(statuscode == "200"):
            print ("<<-- At Client result received: '" + calcres + "'")
            print ("<<-- At Client status code received: " + "status code "+ statuscode)
        if(statuscode == "300"):
            print ("<<-- At Client status code received: " + "status code "+ statuscode)
            print ("!!!!!!!!!!there has been an error calculating your request try again!!!!!!!!!!")
        again = raw_input("Do you want to repeat? (y or Y; anything else is a NO!)")
    #if message is never recieved and timeout reaches beyond 2 seconds then you abort the connection
    else:
        again = "n"
        print("SERVER IS DEAD ABORT!")
        clientSocket.close()

print (" ")
print ("++++   Client Program Ends   ++++")
print (" ")

clientSocket.close()
