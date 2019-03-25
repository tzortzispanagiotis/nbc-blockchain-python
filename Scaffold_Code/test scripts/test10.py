import requests, json, time
from multiprocessing.dummy import Pool

pool = Pool(100)

transactions0 = []
transactions1 = []
transactions2 = []
transactions3 = []
transactions4 = []
transactions5 = []
transactions6 = []
transactions7 = []
transactions8 = []
transactions9 = []


nodeid = {
    'id0': 0,
    'id1': 1,
    'id2': 2,
    'id3': 3,
    'id4': 4,
    'id5': 5,
    'id6': 6,
    'id7': 7,
    'id8': 8,
    'id9': 9,

}

node = {
    '0': 'http://127.0.0.1:5000',
    '1': 'http://127.0.0.1:5001',
    '2': 'http://127.0.0.1:5002',
    '3': 'http://127.0.0.1:5003',
    '4': 'http://127.0.0.1:5004'
    '5': 'http://127.0.0.1:5005',
    '6': 'http://127.0.0.1:5006',
    '7': 'http://127.0.0.1:5007',
    '8': 'http://127.0.0.1:5008',
    '9': 'http://127.0.0.1:5009',
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
    with open('../assignment_docs/transactions/10nodes/transactions0.txt') as f:
        lines = [line.rstrip('\n') for line in f]
        for line in lines:
            transactions0.append(line.split(' '))
        # print(transactions0)
    with open('../assignment_docs/transactions/10nodes/transactions1.txt') as f:
        lines = [line.rstrip('\n') for line in f]
        for line in lines:
            transactions1.append(line.split(' '))
        # print(transactions1)
    with open('../assignment_docs/transactions/10nodes/transactions2.txt') as f:
        lines = [line.rstrip('\n') for line in f]
        for line in lines:
            transactions2.append(line.split(' '))
        # print(transactions2)
    with open('../assignment_docs/transactions/10nodes/transactions3.txt') as f:
        lines = [line.rstrip('\n') for line in f]
        for line in lines:
            transactions3.append(line.split(' '))
        # print(transactions3)
    with open('../assignment_docs/transactions/10nodes/transactions4.txt') as f:
        lines = [line.rstrip('\n') for line in f]
        for line in lines:
            transactions4.append(line.split(' '))
        # print(transactions4)
    
    with open('../assignment_docs/transactions/10nodes/transactions5.txt') as f:
        lines = [line.rstrip('\n') for line in f]
        for line in lines:
            transactions5.append(line.split(' '))
    
    with open('../assignment_docs/transactions/10nodes/transactions6.txt') as f:
        lines = [line.rstrip('\n') for line in f]
        for line in lines:
            transactions6.append(line.split(' '))

    with open('../assignment_docs/transactions/10nodes/transactions7.txt') as f:
        lines = [line.rstrip('\n') for line in f]
        for line in lines:
            transactions7.append(line.split(' '))

    with open('../assignment_docs/transactions/10nodes/transactions8.txt') as f:
        lines = [line.rstrip('\n') for line in f]
        for line in lines:
            transactions8.append(line.split(' '))

    with open('../assignment_docs/transactions/10nodes/transactions9.txt') as f:
        lines = [line.rstrip('\n') for line in f]
        for line in lines:
            transactions9.append(line.split(' '))
    
    futures = []

    r = requests.get(node['1']+'/selfregister')
    r = requests.get(node['2']+'/selfregister')
    r = requests.get(node['3']+'/selfregister')
    r = requests.get(node['4']+'/selfregister')
    r = requests.get(node['5']+'/selfregister')
    r = requests.get(node['6']+'/selfregister')
    r = requests.get(node['7']+'/selfregister')
    r = requests.get(node['8']+'/selfregister')
    r = requests.get(node['9']+'/selfregister')

    

    r = requests.get(node['0']+'/timerstart')
    r = requests.get(node['1']+'/timerstart')
    r = requests.get(node['2']+'/timerstart')
    r = requests.get(node['3']+'/timerstart')
    r = requests.get(node['4']+'/timerstart')
    r = requests.get(node['5']+'/timerstart')
    r = requests.get(node['6']+'/timerstart')
    r = requests.get(node['7']+'/timerstart')
    r = requests.get(node['8']+'/timerstart')
    r = requests.get(node['9']+'/timerstart')



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
    target_url = node['5']+'/startwork'
    futures.append(pool.apply_async(requests.get, [target_url]))
    target_url = node['6']+'/startwork'
    futures.append(pool.apply_async(requests.get, [target_url]))
    target_url = node['7']+'/startwork'
    futures.append(pool.apply_async(requests.get, [target_url]))
    target_url = node['8']+'/startwork'
    futures.append(pool.apply_async(requests.get, [target_url]))
    target_url = node['9']+'/startwork'
    futures.append(pool.apply_async(requests.get, [target_url]))

    time.sleep(5)
    futures = []
    futures.append(pool.apply_async(trans, [transactions0,'0']))
    futures.append(pool.apply_async(trans, [transactions1,'1']))
    futures.append(pool.apply_async(trans, [transactions2,'2']))
    futures.append(pool.apply_async(trans, [transactions3,'3']))
    futures.append(pool.apply_async(trans, [transactions4,'4']))
    futures.append(pool.apply_async(trans, [transactions5,'5']))
    futures.append(pool.apply_async(trans, [transactions6,'6']))
    futures.append(pool.apply_async(trans, [transactions7,'7']))
    futures.append(pool.apply_async(trans, [transactions8,'8']))
    futures.append(pool.apply_async(trans, [transactions9,'9']))

                
    for future in futures:
        future.get()