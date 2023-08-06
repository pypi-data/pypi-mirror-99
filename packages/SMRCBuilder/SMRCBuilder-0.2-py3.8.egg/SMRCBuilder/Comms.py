from SMRCBuilder import Exceptions
import socket
import time

class comms():
    """
    Communication Module
    """
    host = ""
    port = ""
    group = ""
    serversoc = ""
    clientsoc = ""
    connection = ""
    address = ""

    def __init__(self, host, port):
        comms.host = host
        comms.port = port
    
    def setgroup(self, group):
        """
        Sets The Type Of Self (Server Or Client)
        """
        if str(group.lower()) in ("server", "client"):
            comms.group = str(group).lower()
        else:
            Exceptions.ArgError("Group Can Only Be Server Or Client")
            
    def sendmsg(self, message, encoding="utf8"):
        """
        Sends A Message. Automatically Sent In Bytes
        """
        if comms.group == "server":
            try:
                comms.connection.send(bytes(message, encoding))
            except:
                raise Exceptions.MessageError("Error Sending Message. Server Not Initialized?")

        elif comms.group == "client":
            try:
                comms.clientsoc.sendall(bytes(message, encoding))
            except BrokenPipeError:
                raise Exceptions.SocketClosed("Host Has Been Closed. Cannot Send Anymore Messages")

            except:
                raise Exceptions.MessageError("Error Sending Message. Client Not Defined?")
            
    
    def recvmsg(self, buffer=1024, encoding="utf8"):
        """
        Waits For A Message To Be Received. Message Is Decoded For You.
        """
        print(comms.group)
        if comms.group == "server":
            try:
                recv = comms.connection.recv(buffer)
                return recv.decode(encoding)
            except:
                raise Exceptions.MessageError("Error Reciving Message")
        
        elif comms.group == "client":
            recv = comms.clientsoc.recv(buffer)
            return recv.decode(encoding)

    
    class server():
        """
        Server Part Of Communication Module
        """
        def check():
            if comms.group in ("client", ""): raise Exceptions.ArgError("Client Or Undefined Cannot Perform Server Actions")

        def start():
            """
            Starts The Host
            """
            comms.server.check()

            try:
                comms.serversoc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                comms.serversoc.bind((comms.host, comms.port))
                comms.serversoc.listen(1)
                print(f"Hosting Socket Connection Through {comms.host} On Port {comms.port}")
                comms.connection, comms.address = comms.serversoc.accept()
                print(f"Connected To Client")

            except:
                raise Exceptions.ServerHostingError("Error Hosting Connection. Incorrcect IP Or Port?")
    
    class client():
        """
        Client Part Of Communication Module
        """
        def check():
            if comms.group in ("server", ""): raise Exceptions.ArgError("Server Or Undefined Cannot Perform Client Actions")

        def connect():
            """
            Attempts Connection To A Host
            """
            comms.client.check()
            comms.clientsoc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            comms.clientsoc.connect((comms.host, comms.port))