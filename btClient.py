from bluetooth import * 
import time
import pickle
import numpy as np

class DataCollector: 
    def __init__(self, device_address):
        self.client_socket=BluetoothSocket( RFCOMM )
        self.client_socket.connect((device_address,1))
        self.client_socket.send('start')
        time.sleep(1)
        self.reset_time()

    
    def listen(self, filename='', col_count=5):
        """
        Example
        -------
        from btClient import DataCollector
        #data_collector = DataCollector("24:6F:28:B0:2B:1A")#Apr21
        data_collector = DataCollector("24:6F:28:96:A3:B2")#Apr22
        data_collector.listen("./tmp_data.pkl")
        data_collector.client_socket.close()
        """
        if filename!= '':
            f = open(filename,'ab');
        old_data = ''
        while True:
            data = self.client_socket.recv(1000000)                                         
            data_str = data.decode()
            data_list = data_str.split("\r\n")
            line_count = len(data_list) - 1
            if line_count==0:
                old_data += data_list[0]
            else:
                line = old_data + data_list[0]
                print(line)
                if 'f' in dir():
                    line_list = line.split("\t")
                    if len(line_list)==col_count:
                        pickle.dump(np.array(line_list, dtype='float'), f)
                old_data = ''
                for counter in range(1,line_count):
                    print(data_list[counter])
                    if 'f' in dir():
                        line_list = data_list[counter].split("\t")
                        if len(line_list)==col_count:
                            pickle.dump(np.array(line_list, dtype='float'), f)
    
                old_data = data_list[-1]
    
    def reset_time(self):
        now_time = str(time.time())
        self.client_socket.send(now_time)
        #time.sleep(0.5)
    
def read_data(filename):
    objs = []
    with open(filename,'rb') as f:
        while 1:
            try:
                objs.append(pickle.load(f))
            except EOFError:
                break
    return objs
