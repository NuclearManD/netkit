import socket, _thread
from logging import log, add_log_file
# create an INET, STREAMing socket
serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# bind the socket to a public host, and a well-known port
serversocket.bind(("localhost", 80))
# become a server socket
serversocket.listen(5)

def handle_client(sok, adr):
    log("Accepted connection from "+adr[0]+":"+str(adr[1]))
    sok.shutdown(socket.SHUT_RDWR)
    sok.close()

def run():
    while True:
        # accept connections from outside
        (sok, adr) = serversocket.accept()
        # now do something with the clientsocket
        # in this case, we'll pretend this is a threaded server
        _thread.start_new_thread(handle_client, (sok, adr))

if __name__=="__main__":
    add_log_file("logs/{}.txt")
    log("Starting remote_control.py ...")
    run()
