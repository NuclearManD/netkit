import socket, _thread
from logging import log
# create an INET, STREAMing socket
serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# bind the socket to a public host, and a well-known port
serversocket.bind((socket.gethostname(), 80))
# become a server socket
serversocket.listen(5)

def handle_client(sok, adr):
    log

while True:
    # accept connections from outside
    (sok, adr) = serversocket.accept()
    # now do something with the clientsocket
    # in this case, we'll pretend this is a threaded server
    _thread.start_new_thread(handle_client, (sok, adr))
