import logging
import threading
import time
import subprocess # Req python3
import json
import Queue

logging.basicConfig(level=logging.DEBUG, format='%(threadName)s: %(message)s')

manager_port ={"192.168.11.3":30281, "192.168.11.4":30282}

def thread_checkNode():
    logging.debug('start')

#    tmp_json = subprocess.run(['kubectl','get', 'node', '-o', 'json'], \
#                              stdout=subprocess.PIPE, universal_newlines=True)
#    print('')
#    print(tmp_json.stdout)
#    print('')
#    ji = json.loads(tmp_json.stdout)

    a = open('fail.txt') 
    ji = json.load(a,encoding='utf-8')

    print(ji["items"][0]["status"]["addresses"][0])
    print('')

    node_ip_list = []
    
    for i in ji["items"]:
        for j in i["status"]["addresses"]:
            print(j)
            if j["type"] == 'InternalIP':
                node_ip_list.append(j["address"])

    # ip list of nodes.
    print(node_ip_list)

    # the length of list
    print(len(ji["items"]))
    print(len(ji["items"])-1)

    # tmp node status
    tmp_node_status = 'True'

    # the no for connecing nodes
    connecting_node_number = 0

    # search master node
    master_node_number = 0
    for num, di in enumerate(ji["items"]):
        for i in di["metadata"]["labels"]:
            if 'node-role.kubernetes.io/master' in i:
                master_node_number = num
                print(master_node_number)

    # search worker node status
    for num, di in enumerate(ji['items']):
        if num != master_node_number:
            print(str(num) + ':' + di["status"]["conditions"][3].get('status'))

            # connecting node
            if 'True' == di["status"]["conditions"][3].get('status'):
                print('Conecting Node')
                connection_node_number = num
                print(node_ip_list)
                print(manager_port[node_ip_list[num]])
                time.sleep(10)
                queue.put([node_ip_list[num],manager_port[node_ip_list[num]]])
                event.set()
            
    while True:
        # check node status:
    
    time.sleep(5)
    logging.debug('end')

def thread_connectRtc():
    logging.debug('########## start')
    counter = 0

    # end condition ....
    while counter < 1:
        print('Waiting.... :' + str(counter))
        event.wait()
        counter+=1;
        print(queue.get())
    
    logging.debug('########## end')

if  __name__  ==  '__main__':

    t1 = threading.Thread(target=thread_checkNode)
    t2 = threading.Thread(target=thread_connectRtc)

    event = threading.Event()
    queue = Queue.Queue()
    
    print('## START ##')
    
    t1.start()
    t2.start()





    
