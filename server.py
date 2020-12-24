import socket
import threading
from price import  Amazon
from time import sleep
from pandas import DataFrame
from requests import get
import  pickle as pick


class Server:
    port = 9999
    ip = socket.gethostbyname(socket.gethostname())
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((ip, port))
    format = "UTF-8"
    valid = True
    orginal =[]
    discount =[]
    offer =[]

    # def send(self, message, conn, addr):
    #     message = message.encode(self.format)
    #     messageLength = len(message)
    #     messageLength = str(messageLength).encode(self.format) + b' ' * (64 - messageLength)
    #     conn.send(messageLength)
    #     conn.send(message)

    def send(self, message, conn, addr):
        message = pick.dumps(message)
        messageLength = len(message)
        messageLength = pick.dumps(str(messageLength)) + b' ' * (64 - messageLength)
        conn.send(messageLength)
        conn.send(message)

    def start(self, conn, addr):
        try:
            while 1:
                # msg_length = conn.recv(64).decode(self.format)
                msg_length = pick.loads(conn.recv(64))
                if msg_length:
                    # message = conn.recv(int(msg_length)).decode(self.format)
                    message = pick.loads(conn.recv(int(msg_length)))
                    if ("start" in message):
                        try:
                            if (len(message.split(" ")) == 2):
                                get(message.split(" ")[-1])
                                self.send("[STARTING]", conn, addr)
                                scrap = threading.Thread(target=self.scrapy,args=(message.split(" ")[-1],))
                                scrap.start()
                            else:
                                2 / 0
                        except:
                            self.send("[ERROR] enter valid url", conn, addr)

                    elif (message == "exit"):
                        self.valid = False
                        break
                    elif (message == "get"):
                        self.send("[FETCHING DATA...]", conn, addr)
                    elif (message == "commands"):
                        self.send("start : start searching\nexit  : stop searching\nget   : get data fetched", conn,
                                  addr)
                    else:
                        self.send("[ERROR] not valid command", conn, addr)
        except:
            pass
        conn.close()
        print(f"[CLOSED]{addr}")

    def scrapy(self, link):
        while self.valid:
            try:
                if(Amazon(link).getPrice()):
                    info = Amazon(link).getPrice()
                    self.orginal.append(info[0])
                    self.discount.append(info[1])
                    self.offer.append(info[2])
                    DataFrame({"orginal":self.orginal,"discount price":self.discount,"offer":self.offer}).to_csv("data.csv",index=False)
                else:
                    self.send("[OUT OF STOCK]")
            except:
                pass

    def listen(self):
        self.server.listen()
        while 1:
            conn, addr = self.server.accept()
            sample = threading.Thread(target=self.start, args=(conn, addr))
            sample.start()
            print(f"[CONNECTION ESTABLISHED]({addr})")


ser = Server()
print(f"[SERVER HOSTED AT {ser.ip}]")
ser.listen()
