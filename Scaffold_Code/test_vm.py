import requests, json, time
from multiprocessing.dummy import Pool

pool = Pool(100)

transactions0 = []
transactions1 = []
transactions2 = []
transactions3 = []
transactions4 = []

nodeid = {
    'id0': 0,
    'id1': 1,
    'id2': 2,
    'id3': 3,
    'id4': 4
}

node = {
    '0': 'http://192.168.0.1:5000',
    '1': 'http://192.168.0.2:5001',
    '2': 'http://192.168.0.3:5002',
    '3': 'http://192.168.0.4:5003',
    '4': 'http://192.168.0.5:5004'
}





def trans(transactions, src_id):
    for t in transactions:
        temp = {
            "id": nodeid[t[0]],
	        "amount": int(t[1])
        }
        body = json.dumps(temp)
        r = requests.post(node[src_id]+'/createtransaction', data=body)

if __name__ == '__main__':
    with open('../assignment_docs/transactions/5nodes/transactions0.txt') as f:
        lines = [line.rstrip('\n') for line in f]
        for line in lines:
            transactions0.append(line.split(' '))
        # print(transactions0)
    with open('../assignment_docs/transactions/5nodes/transactions1.txt') as f:
        lines = [line.rstrip('\n') for line in f]
        for line in lines:
            transactions1.append(line.split(' '))
        # print(transactions1)
    with open('../assignment_docs/transactions/5nodes/transactions2.txt') as f:
        lines = [line.rstrip('\n') for line in f]
        for line in lines:
            transactions2.append(line.split(' '))
        # print(transactions2)
    with open('../assignment_docs/transactions/5nodes/transactions3.txt') as f:
        lines = [line.rstrip('\n') for line in f]
        for line in lines:
            transactions3.append(line.split(' '))
        # print(transactions3)
    with open('../assignment_docs/transactions/5nodes/transactions4.txt') as f:
        lines = [line.rstrip('\n') for line in f]
        for line in lines:
            transactions4.append(line.split(' '))
        # print(transactions4)
    
    futures = []

    r = requests.get(node['1']+'/selfregister')
    r = requests.get(node['2']+'/selfregister')
    r = requests.get(node['3']+'/selfregister')
    r = requests.get(node['4']+'/selfregister')

    r = requests.get(node['0']+'/timerstart')
    r = requests.get(node['1']+'/timerstart')
    r = requests.get(node['2']+'/timerstart')
    r = requests.get(node['3']+'/timerstart')
    r = requests.get(node['4']+'/timerstart')




    target_url = node['0']+'/startwork'
    futures.append(pool.apply_async(requests.get, [target_url]))
    
    target_url = node['1']+'/startwork'
    futures.append(pool.apply_async(requests.get, [target_url]))
    
    target_url = node['2']+'/startwork'
    futures.append(pool.apply_async(requests.get, [target_url]))
    
    target_url = node['3']+'/startwork'
    futures.append(pool.apply_async(requests.get, [target_url]))
    
    target_url = node['4']+'/startwork'
    futures.append(pool.apply_async(requests.get, [target_url]))

    time.sleep(5)
    futures = []
    futures.append(pool.apply_async(trans, [transactions0,'0']))
    futures.append(pool.apply_async(trans, [transactions1,'1']))
    futures.append(pool.apply_async(trans, [transactions2,'2']))
    futures.append(pool.apply_async(trans, [transactions3,'3']))
    futures.append(pool.apply_async(trans, [transactions4,'4']))
                
    for future in futures:
        future.get()