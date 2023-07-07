import socket
import network
import time
import json
from mode import *

class access_point():
    def __init__(self,ssid,password):
        self.ap=network.WLAN(network.AP_IF)
        self.ap.config(essid=ssid, password=password) 
        self.is_started=False
    def start(self):
        """
        start : setup the access point and the socket (run only once)
        inputs :
        /
        outputs:
        /
        """
        self.ap.active(True)
        while self.ap.active == False:
            pass
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind(('', 80))
        self.socket.listen(5)
        
    def run(self,data_path,data_size):
        """
        run : wait for a connection and send the json file
        inputs :
        data : the data we want the send (list)
        outputs:
        /
        """
        start='{"data" : ['
        end=' ]}'
        #json_data=json.dumps(data)
        conn, addr = self.socket.accept()
        request = conn.recv(1024)
        #response =json_data
        if data_size == 1 :
            comma=0
        else :
            comma = data_size-1
        response_headers = "HTTP/1.1 200 OK\nContent-Type: application/json\nContent-Length: {}\n\n".format(len(start)+6*data_size+comma*2+len(end))
        conn.send(response_headers.encode('utf-8'))
        conn.send(start)
        data=open('data.txt', 'r')
        for x in range(data_size):
            line=data.readline()
            to_send=line[:4]
            print(to_send)
            if x != 0:
                conn.send(', ')
            conn.send('"'+to_send+'"')
        conn.send(end)
        
        conn.close()
        
        print("exit transfert mode")
    def stop(self):
        """
        stop : desactivate the access point
        inputs:
        /
        outputs:
        /
        """
        self.ap.active(False)
        
    def new_instance(self):
        """
        new_instance : setup the access point if it is the first time,else reactivate the access point
        inputs :
        /
        outputs :
        /
        """
        if not self.is_started:
            self.start()
            self.is_started=True
        else :
            self.ap.active(True)
        print("Access point active")
                
            
            
            
        
        



