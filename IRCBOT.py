import socket
import os
from modules import *

server = "jjhsk.com"
channel = "#help"
botnick = "PokeBot"
currdir = os.getcwd()
moduledir = "modules/"
modimp = "modules."

def ping(msg):
    ircsock.send(bytes("PONG :" + msg + "\r\n",'UTF-8'))

def sendmsg(chan , msg):
    ircsock.send(bytes("PRIVMSG "+ chan +" :"+ msg +"\n",'UTF-8'))

def joinchan(chan):
    ircsock.send(bytes("JOIN "+ chan +"\n",'UTF-8'))

def hello(msg):
    newmsg = msg
    newmsg = newmsg.partition(":")[2].partition(":")[0]
    chan = newmsg.partition(" ")[2].partition(" ")[2].replace(" ","")
    if chan == botnick:
        chan = newmsg.partition("!")[0]
    ircsock.send(bytes("PRIVMSG "+ chan +" :Hello!\n",'UTF-8'))

ircsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ircsock.connect((server, 6667)) # Here we connect to the server using port 6667
ircsock.send(bytes("USER "+ botnick +" "+ botnick +" "+ botnick +" :yo\n",'UTF-8'))
ircsock.send(bytes("NICK "+ botnick +"\n",'UTF-8')) # here we actually assign the nick to the bot

joinchan(channel) # Join the channel using the functions we previously defined
CommDict = {}

CommandList = []
ModuleList = []
for root, dirs, files in os.walk(currdir + "/" + moduledir):
    for file in files:
        if file.endswith(".py") and not "__" in file:
            Filename = file
            Filename = Filename.replace(".py","")
            comm = eval(Filename + "." + "GiveDict")
            ModDict = comm()
            for item in list(ModDict.keys()):
                CommandList.append(item)
                ModuleList.append(ModDict[item])

x = 0
for item in CommandList:
    CommDict[CommandList[x]] = ModuleList[x]
    x += 1


while 1: # Be careful with these! It might send you to an infinite loop
    ircmsg = ircsock.recv(2048).decode('UTF-8') # receive data from the server
    ircmsg = ircmsg.rstrip() # removing any unnecessary linebreaks.
    print(ircmsg) # Here we print what's coming from the server

    if ircmsg.find(":Hello "+ botnick) != -1 or ircmsg.find(":hello "+ botnick) != -1:
        hello(ircmsg)
    if ircmsg.find("PING :") != -1:
        response = ircmsg.partition(":")[2]
        ping(response)
    if ircmsg.find(":!Help") != -1:
        newmsg = ircmsg
        newmsg = newmsg.partition(":")[2].partition(":")[0]
        chan = newmsg.partition(" ")[2].partition(" ")[2].replace(" ","")
        if chan == botnick:
            chan = newmsg.partition("!")[0]

        OutString = ""
        for item in list(CommDict.keys()):
            OutString = OutString + item + " "
        sendmsg(chan, OutString)

    if ircmsg.find(":!") != -1:
        #This finds the intended destination of the message
        newmsg = ircmsg
        newmsg = newmsg.partition(":")[2].partition(":")[0]
        chan = newmsg.partition(" ")[2].partition(" ")[2].replace(" ","")
        if chan == botnick:
            chan = newmsg.partition("!")[0]
        
        ircmsg = str(ircmsg.partition(":")[2].partition(":")[2])
        commandname = ircmsg.partition(" ")[0]
        if commandname in CommDict:
            ResponseMsg = eval(CommDict[commandname] + "." + "ReceiveMsg(\"" + ircmsg + "\")")
            if type(ResponseMsg) is list:
                x = 0
                for item in ResponseMsg:
                    sendmsg(chan, ResponseMsg[x])
                    x += 1
            else:
                if type(ResponseMsg) is not type(None):
                    sendmsg(chan, ResponseMsg)
                else:
                    sendmsg(chan,"Response Error")

