
# From: http://it-in-der-hosentasche.blogspot.com/2014/03/bluetooth-zwischen-raspberry-pi-und.html
# file: rfcomm-server.py
# auth: Albert Huang <albert@csail.mit.edu>
# desc: simple demonstration of a server application that uses RFCOMM sockets
#
# $Id: rfcomm-server.py 518 2007-08-10 07:20:07Z albert $

from bluetooth import *

def initServer():
 server_sock=BluetoothSocket( RFCOMM )
 server_sock.bind(("",PORT_ANY))
 server_sock.listen(1)

 uuid = "00001101-0000-1000-8000-00805F9B34FB"

 advertise_service(server_sock, "Echo Server",
     service_id = uuid,
     service_classes = [ uuid, SERIAL_PORT_CLASS ],
     profiles = [ SERIAL_PORT_PROFILE ]
 )
 return server_sock

def getClientConnection(server_sock):
 print("Waiting for connection")
 client_sock, client_info = server_sock.accept()
 print("accepted connection from ", client_info)
 return client_sock

def manageConnection(socket, callback):
 try:
   while True:
     data = socket.recv(1024)
     if len(data) == 0: break
     print("received [%s]" % data)
     callback(data)
     socket.send("Echo from Pi: [%s]\n" % data)

 except IOError:
   pass

def main(callback):
    server=initServer()
    while  True:
        client=getClientConnection(server)
        manageConnection(client, callback)
        client.close()
    server.close()
    print("terminating...")

if __name__ == '__main__':
    main()
