

'''
Created 10 june 2016
author : Sbenoit
'''
import socket
import threading

class FretsConnect(object):
    PORT = 5555

    def __init__(self,):
        #Defini le nom du FRETS actuel
        self.hostname = socket.gethostname()
        self.socketServer()
        #Si c'est PI0, il attend une connection sinon il se connecte
        #if self.hostname == 'FRETS_PI0':
        #   self.socketServer()
        #elif  self.hostname == 'FRETS_PI1':
        #    self.socketClient()
        #else :
        #    pass



    def socketServer(self):
        print "Starting Thread..."
        self.server_t = threading.Thread(target=self.server_thread)
        self.server_t.daemon = True
        self.server_t.start()


    def server_thread(self):
        HOST = ''
        # Create the socket
        serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Bind it to a public host
        serversocket.bind((HOST, self.PORT))

        # Listen, maximum 2 connection
        serversocket.listen(2)

        self.conn, addr = serversocket.accept()
        print 'Connected by', addr



    def closeConnection(self):
        print "Closing Connection..."
        self.conn.close()
        return

    def socketClient(self):

        pass

    def read(self):
        data = self.conn.recv(1024)

        # If there's no data do nothing
        if data:
            # Print the data
            print ("%s" % data)
        return

    def send(self):

        pass

    def __exit__(self, exc_type, exc_value, traceback):
        self.closeConnection()


if __name__ == '__main__':
    F = FretsConnect()
    while True:
        F.read()
    F.server_t.join()