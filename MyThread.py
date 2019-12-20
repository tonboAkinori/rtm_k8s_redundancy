import logging
import threading
import time
import subprocess # Req python3
import json

logging.basicConfig(level=logging.DEBUG, format='%(threadName)s: %(message)s')

def thread_checkNode():
    logging.debug('start')
    tmp_json = subprocess.run(['kubectl','get', 'node', '-o', 'json'], stdout=subprocess.PIPE, universal_newlines=True)

    print('')
    print(tmp_json.stdout)
    print('')

    ji = json.loads(tmp_json.stdout)

    print(ji["items"][0]["status"]["addresses"][0])
    print('')

    node_ip_list = []
    
    for i in ji["items"]:
        for j in i["status"]["addresses"]:
            print(j)
            if j["type"] == 'InternalIP':
                node_ip_list.append(j["address"])

    # Node 
    print(node_ip_list)

    # Node 
    print(len(ji["items"]))

    time.sleep(5)
    logging.debug('end')

def thread_connectRtc():
    logging.debug('start')
    time.sleep(2)
    logging.debug('end')

if  __name__  ==  '__main__':

    t1 = threading.Thread(target=thread_checkNode)
    t2 = threading.Thread(target=thread_connectRtc)

    print('## START ##')
    
    t1.start()
    t2.start()





    
