from socket import *
#assign server name
serverName = 'localhost'
#assign port number
serverPort = 12002
#set up TCP connection
clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((serverName, serverPort))
again = "Y"
while (again=="y") | (again=="Y"):
    #get [number][operation][number] (NO SPACES)
    message = raw_input('Input math operation(note spaces are not used) [number][operation code][number]:')
    #get decimal for chance of dropping packet
    print ("\n ")
    print ("-->> At Client message to send out: '" + message + "'")
    #send message to server
    clientSocket.send(message)
    #receive response from server
    modifiedMessage = clientSocket.recv(1026)
    #split message up into array it is in the form of [result] [status code] there is space between them
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

print (" ")
print ("++++   Client Program Ends   ++++")
print (" ")

clientSocket.close()
