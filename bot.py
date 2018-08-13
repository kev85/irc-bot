#!/usr/bin/python3
import socket

#params
ircsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server = "card.freenode.net"
channel = "#kexd"
botnick = "bbbbooooottttttt"
adminname = "kexd"
exitcode = "exit " + botnick

#connect to server via params vars
ircsock.connect((server,6667))
ircsock.send(bytes("USER "+ botnick +" "+ botnick +" "+ botnick + " " + botnick + "\n").encode("utf-8")) #filling out a form setting all the fields to the bot nickname. NB: \n char denotes newline/enter keystroke
ircsock.send(bytes("NICK "+ botnick +"\n").encode("utf-8")) #assign the botnick to the bot

#join channel command
def joinchan(chan):
    ircsock.send(bytes("JOIN " + chan + "\n").encode("utf-8"))
    ircmsg = ''
    while ircmsg.find("END of /NAMES list.") == -1: #server sends that string, so now we know we're in & can start listening
        ircmsg = ircsock.recv(2048).decode("UTF-8")
        ircmsg = ircmsg.strip('\n\r')
        print(ircmsg)

#respond to PING
def ping():
    ircsock.send(bytes("PONG :pingis\n").encode("utf-8"))

#send a message
#target=channel sets the default "target" for a message to whatever chan we set in global params
def sendmsg(msg, target=channel):
    ircsock.send(bytes("PRIVMSG "+ target +" :"+ msg +"\n").encode("utf-8"))

#main loop
#this is an infinite while loop to avoid constantly calling the function to do anything!
def main():
  joinchan(channel)
  while 1:
    ircmsg = ircsock.recv(2048).decode("UTF-8")
    ircmsg = ircmsg.strip('\n\r')
    print(ircmsg)
    if ircmsg.find("PRIVMSG") != -1:
      name = ircmsg.split('!',1)[0][1:]
      message = ircmsg.split('PRIVMSG',1)[1].split(':',1)[1]
      if len(name) < 17:
        if message.find('Hi ' + botnick) != -1:
          sendmsg("Hello " + name + "!")
        if message[:5].find('.tell') != -1:
          target = message.split(' ', 1)[1]
          if target.find(' ') != -1:
              message = target.split(' ', 1)[1]
              target = target.split(' ')[0]

          else:

            target = name
            message = "Could not parse. The message should be in the format of .tell [target] [message] to work properly."
          sendmsg(message, target)
        if name.lower() == adminname.lower() and message.rstrip() == exitcode:
          sendmsg("oh...okay. :'(")
          ircsock.send(bytes("QUIT \n", "UTF-8"))
          return
    else:
      if ircmsg.find("PING :") != -1:
        ping()

main() #call main