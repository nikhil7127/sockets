import socket
import threading
import pickle as pick

client = socket.socket()
client.connect(("192.168.55.103", 9999))
format = "UTF-8"
connection = True


# def sendToServer(message):
#     message = message.encode(format)
#     temp = len(message)
#     temp = str(temp).encode(format) + b" " * (64 - temp)
#     client.send(temp)
#     client.send(message)


def sendToServer(message):
    message = pick.dumps(message)
    temp = len(message)
    temp = pick.dumps(str(temp)) + b" " * (64 - temp)
    client.send(temp)
    client.send(message)

# def receiveThread():
#     while connection:
#         len = client.recv(64).decode(format)
#         print(len)
#         if len:
#             recvMessage = client.recv(int(len)).decode(format)
#             print(f"{recvMessage}\n>>", end=" ")
#         else:
#             print("[CLOSED CONNECTION]")
#             break

def receiveThread():
    while connection:
        len = pick.loads(client.recv(64))
        print(len)
        if len:
            recvMessage = pick.loads(client.recv(int(len)))
            print(f"{recvMessage}\n>>", end=" ")
        else:
            print("[CLOSED CONNECTION]")
            break


def sendThread():
    while 1:
        user = input(">> ")
        sendToServer(user)
        if (user == "exit"):
            connection == False
            break


receive = threading.Thread(target=receiveThread)
send = threading.Thread(target=sendThread)
send.start()
receive.start()
