import logging
import threading
import time
import subprocess # Req python3

logging.basicConfig(level=logging.DEBUG, format='%(threadName)s: %(message)s')

def thread_checkNode():
    logging.debug('start')
    subprocess.run(['ls'])
    time.sleep(5)
    logging.debug('end')

def thread_connectRtc():
    logging.debug('start')
    time.sleep(2)
    logging.debug('end')

if  __name__  ==  '__main__':

    t1 = threading.Thread(target=check_node)
    t2 = threading.Thread(target=connect_rtc)

    print('## START ##')
    
    t1.start()
    t2.start()





    
