import socket
import threading
import time

import select


class maConnection():
    def __init__(self):
        self.myConn = None
        self.sock = None
        pass

    def connect(self,server,port):

        self.serverID = (server,port)
        self.myConn = clientThread(self.serverID)
        self.myConn.daemon = True
        self.sock = self.myConn.getSocket()
        #Start the thread
        self.myConn.start()


    def send(self,arg):
        try:
            self.sock.send(arg)
        except:
            print "Fail to send data to" + str(self.serverID)

    def join(self):
        self.myConn.running = False

    def getIP(self):
        pass

    def connected(self):
        return self.myConn.connected

class clientThread(threading.Thread):

    def __init__(self,serverID):
        #Init the threads methods
        threading.Thread.__init__(self)

        self.connected = False
        #Create the socket
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #Set timeout to 30 seconds
        self.sock.settimeout(30)
        self.serverID = serverID
        #Start the thread
        self.running = True

    def run(self):
        #While unconnected, try to connect
        while self.running == True:
        #What to do while we're connected ?

            #Try to connect
            while self.connected == False and self.running == True:
            #Connect to the server
                try :
                    self.sock.connect(self.serverID)
                    self.connected = True
                    print "Connected to : " + str(self.serverID)

                except(socket.error):
                    print "\nConnection error, server : " + str(self.serverID) + " is not available - " + str(socket.error) + "\n"
                    time.sleep(5)
                    print "Retrying to connect to" +  str(self.serverID)

            try:
                ready_to_read, ready_to_write, in_error = \
                    select.select([self.sock, ], [self.sock, ], [], 5)
            except select.error:
                self.sock.shutdown(2)  # 0 = done receiving, 1 = done sending, 2 = both
                self.sock.close()
                # connection error event here, maybe reconnect
                print 'connection error'
                self.connected =False
                break
            
        if self.connected:
            print "Thread ended, closing connection to host..."
            self.sock.close()
        else:
            print "Stopped trying to connect...end of thread"

    def getSocket(self):
        return self.sock
