#!/usr/bin/env python


import SocketServer 
from SocketServer import ThreadingMixIn
import threading 
import socket
import time
from Queue import Queue
import sys
import os

class ThreadingPoolMixIn(ThreadingMixIn):
    numThreads=20;
    
    def serve_forever(self):
        self.queue = Queue(self.numThreads)
        for x in range(self.numThreads):
            server_thread = threading.Thread(target = self.process_request_thread)
            server_thread.daemon = True
            server_thread.start()
        while True:
            self.handle_request()
        self.server_close()
   
    def process_request_thread(self):
        while True:
            ThreadingMixIn.process_request_thread(self, *self.queue.get())
               
    def handle_request(self):
        # Look after request		
        request, client_address = self.get_request()
        self.queue.put((request, client_address))

    		
    		            
class ThreadedTCPRequestHandler(SocketServer.BaseRequestHandler):
    def handle(self):
        data = self.request.recv(1024)
    	response= "Connected To Server"
    	global server
    	if data == "KILL_SERVICE\n":
    		os._exit(0) 
    	    	
     	elif data.startswith("HELO") and data.endswith("\n"):
     		ip, port = server.server_address
     		response= data+"IP:"+str(ip)+"\nPort:"+str(port)+"\nStudentID:12309879\n"   		
        self.request.sendall(response)
    
   
    	
    	
class ThreadedTCPServer(ThreadingPoolMixIn, SocketServer.TCPServer):
		pass

server = ThreadedTCPServer(('',int(sys.argv[1])), ThreadedTCPRequestHandler)
		
if __name__ == "__main__":
	server.serve_forever()
	



