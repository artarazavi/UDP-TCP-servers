from socket import *
import re
import random
#assign port number
serverPort = 12000
#UDP socket creation
serverSocket = socket(AF_INET, SOCK_DGRAM)
#bind port to socket
serverSocket.bind(('', serverPort))
print ("The server is ready to receive\n")
while True:
    #message recieved in format "n[operation]n [probability of dropping packet in decimal format]""
    messagercv, clientAddress = serverSocket.recvfrom(2048)
    #split up message to extract parts
    rcvdecarr = messagercv.split(" ")

    if(len(rcvdecarr) == 2):
        #in index 1 that is the probability of dropping the packetr decimal
        rcvdec = rcvdecarr[1]
        #delete probability of dropping the packet from the array because you already stored it
        rcvdecarr.pop(1)
        #turn array now with only the numbers and operation code in it back into a string to be processed for calculation
        message = ''.join(rcvdecarr)
        #convert string decimal to decimal
        isfloat = True
        #only processed if decimal formal is valid
        try:
            decimalrcv = float(rcvdec)
        except ValueError:
            isfloat = False
        #make sure value is float
        randompick = 0
        if(isfloat == True):
            #[float(x.strip(' "')) for x in rcvdec]
            #deal with entering values over 1.0 ie: more than 100% chance of package dropping
            if(decimalrcv > 1.0):
                decimalrcv = 1.0
            #convert to percent
            dropzero = decimalrcv * 100
            #100%-probability of dropping paacket = probability of not dropping a packet
            dropone = 100-dropzero
            #make array of (probability of dropping)* #0s and (probability of not dropping)*#1s
            my_list = [1] * int(dropone)  + [0] * int(dropzero)
            #pick random item from list
            randompick = random.choice(my_list)
            #bellow what you would do if 50% probability of dropping packets
            #randompick = int(random.randint(0, 1))
            #if you picked one packet was not dropped you may processed
        #if value not float ensure loop doesnt execute
        else:
            modifiedMessage = -1
            print("!!!!!!!!!!incorrect decimal!!!!!!!!!!\n")
            print ("<<-- At Server modified message to send back: '"+ "-1 \n"  + "status code 300" + "'\n")
            #message sent back in format of [result] [status code]
            serverSocket.sendto("-1 300", clientAddress)
        if(randompick == 1):
            print ("-->> At Server receved message is: '" + message.decode() + "'")
            print ("  -->> clientAddress is: " , str(clientAddress[0]) + "/" + str(clientAddress[1]) )
            splitmsg = re.split("([+-/*])", message.replace(" ", ""))
            #i used penalties to keep track of number or operation errors in client message
            penalties = 0
            #if the length of the array is more than 3 there is an issue its not in format number operator number
            if(not(len(splitmsg)==3)):
                penalties = penalties + 1
                print("!!!!!!!!!!invalid input!!!!!!!!!!\n")
                print ("<<-- At Server modified message to send back: '" + "status code 300" + "'\n")
                #message sent back in format of [result] [status code]
                serverSocket.sendto("-1 300", clientAddress)
            else:
                #number(not a number) operator number
                if((splitmsg[0]).isdigit() == False):
                    penalties = penalties + 1
                    print("!!!!!!!!!!invalid first input not correct length!!!!!!!!!!\n")
                    print ("<<-- At Server modified message to send back: '"+ "-1 \n"  + "status code 300" + "'\n")
                    #message sent back in format of [result] [status code]
                    serverSocket.sendto("-1 300", clientAddress)
                #number operator number(not a number)
                if((splitmsg[2]).isdigit() == False):
                    penalties = penalties + 1
                    print("!!!!!!!!!!invalid second input!!!!!!!!!!\n")
                    print ("<<-- At Server modified message to send back: '"+ "-1 \n"  + "status code 300" + "'\n")
                    #message sent back in format of [result] [status code]
                    serverSocket.sendto("-1 300", clientAddress)
                #number operator(not an operator) number
                if(not(splitmsg[1] == '-' or splitmsg[1] == '+' or splitmsg[1] == '*' or splitmsg[1] == '/')):
                    penalties = penalties + 1
                    print("!!!!!!!!!!invalid operation input!!!!!!!!!!\n")
                    print ("<<-- At Server modified message to send back: '"+ "-1 \n" + "status code 300" + "'\n")
                    #message sent back in format of [result] [status code]
                    serverSocket.sendto("-1 300", clientAddress)

            #message input violates no restrictions above
            if(penalties == 0):
                operator = splitmsg[1]
                #if subtract
                if operator == '-' :
                    modifiedMessage = str(int(splitmsg[0]) - int(splitmsg[2]))
                    print ("<<-- At Server modified message to send back: '" + modifiedMessage + "'\n"+ "status code 200" + "'\n")
                    #message sent back in format of [result] [status code]
                    serverSocket.sendto(str(modifiedMessage+" 200"), clientAddress)
                #if add
                if operator == '+' :
                    modifiedMessage = str(int(splitmsg[0]) + int(splitmsg[2]))
                    print ("<<-- At Server modified message to send back: '" + modifiedMessage + "'\n"+ "status code 200" + "'\n")
                    #message sent back in format of [result] [status code]
                    serverSocket.sendto(str(modifiedMessage+" 200"), clientAddress)
                #if multiply
                if operator == '*' :
                    modifiedMessage = str(int(splitmsg[0]) * int(splitmsg[2]))
                    print ("<<-- At Server modified message to send back: '" + modifiedMessage + "'\n"+ "status code 200" + "'\n")
                    #message sent back in format of [result] [status code]
                    serverSocket.sendto(str(modifiedMessage+" 200"), clientAddress)
                #if divide but not zero
                if ((operator == '/') and (not (int(splitmsg[2]) == 0)) ):
                    modifiedMessage = str(int(splitmsg[0]) / int(splitmsg[2]))
                    print ("<<-- At Server modified message to send back: '" + modifiedMessage + "'\n"+ "status code 200" + "'\n")
                    #message sent back in format of [result] [status code]
                    serverSocket.sendto(str(modifiedMessage+" 200"), clientAddress)
                #if divide by zero then not valid operation
                if((operator == '/') and (int(splitmsg[2]) == 0)):
                    modifiedMessage = -1
                    print("!!!!!!!!!!divide by 0!!!!!!!!!!\n")
                    print ("<<-- At Server modified message to send back: '"+ "-1 \n"  + "status code 300" + "'\n")
                    #message sent back in format of [result] [status code]
                    serverSocket.sendto("-1 300", clientAddress)
    else:
                modifiedMessage = -1
                print("!!!!!!!!!!incorrect format!!!!!!!!!!\n")
                print ("<<-- At Server modified message to send back: '"+ "-1 \n"  + "status code 300" + "'\n")
                #message sent back in format of [result] [status code]
                serverSocket.sendto("-1 300", clientAddress)
