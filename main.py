import socket
from emoji import demojize
from deep_translator import GoogleTranslator

server = 'irc.chat.twitch.tv'
nickname = 'crncinimajopravic'
token = 'oauth:p520kzgbrg6ha4n4wcmhup2v0dtfvg'
channel = '#'
port = 6667

channel += str(input("Enter Twitch chanel name: "))

vticnik = socket.socket()
vticnik.connect((server, port))
vticnik.send(f"PASS {token}\n".encode('utf-8'))
vticnik.send(f"NICK {nickname}\n".encode('utf-8'))
vticnik.send(f"JOIN {channel}\n".encode('utf-8'))
resp = vticnik.recv(2048).decode('utf-8') #gets rid of the hello message from Twitch

while True:
    resp = vticnik.recv(2048).decode('utf-8')
    if resp.startswith('PING'):
        vticnik.send("PONG\n".encode('utf-8'))
    elif len(resp) > 0:
        responseList = resp.split(":", 2) #[0] is empty, [1] is the string we have to split to get the message authors username, and [2] is the message
        responseUsername = (responseList[1].split("!", 1))[0]
        translatedMsg = GoogleTranslator(source='auto', target='english').translate(text=str(responseList[2]))
        if translatedMsg is not None:
            output = responseUsername + ": " + translatedMsg
            print(f"{responseUsername}: {translatedMsg}")
        else:
            print("COULD NOT TRANSLATE")

vticnik.close()