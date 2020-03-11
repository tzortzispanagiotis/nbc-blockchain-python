import requests, json, time
from flask import Flask, jsonify, request, render_template
from flask_cors import CORS

# import block, chain, wallet, transaction
import node
import config

app = Flask(__name__)
CORS(app)
_node = None

# GETTERS FOR DEBUGGING - REST CALLS
# --------------------------------------- #
@app.route('/getwallets', methods=['GET'])
def get_wallets():
    wallets = _node.ring
    # body = json.dumps(wallets)
    return jsonify(wall=wallets)

@app.route('/getutxo', methods=['GET'])
def get_utxos():
    utxos = []
    for i in _node.UTXO:
        utxos.append(i.to_dict())
    return jsonify(utxo=utxos)

@app.route('/getchain', methods=['GET'])
def get_chain():
    return jsonify(chain=_node.chain)    
# --------------------------------------- #

#BOOTSTRAP ENDPOINTS (ONLY BOOTSTRAP USES THEM):
# --------------------------------------- #
@app.route('/addnode', methods=['POST'])
def add_node():
    newNode = {}
    a = request.get_json(force=True)
    newNode['pkey'] = a['pkey']
    newNode['ip'] = a['ip']
    newNode['port'] = a['port']
    print(newNode)
    _node.register_node_to_ring(newNode)
    print('edw3')
    return jsonify(status='successful')
# --------------------------------------- #

# ENDPOINTS USED FOR INIT (WALLETS AND GENESIS) #
# --------------------------------------- #
@app.route('/selfregister', methods=['GET'])
def self_register():
    if _node.bootstrapip != '-1':
        temp = {
                'pkey': _node.wallet.address,
                'ip': _node.ring[0]['ip'],
                'port': _node.ring[0]['port']
        }
        body = json.dumps(temp)
        # print(body)
        r = requests.post('http://'+_node.bootstrapip+':'+_node.bootstrapport+'/addnode', data=body)
    return jsonify(status='OK')

@app.route('/receivegenesis', methods = ['POST'])
def receive_genesis():
    a = request.get_json(force=True)
    # print(a)
    _node.getGenesisBlock(a)
    return jsonify(status="ok")

@app.route('/receivewallets', methods = ['POST'])
def receive_wallets():
    a = request.get_json(force=True)
    print(a)
    _node.ring = a
    return jsonify(status="ok")
# --------------------------------------- #

# ENDPOINTS FOR TRANSACTIONS AND BLOCKS   #
# --------------------------------------- #    
@app.route('/createtransaction', methods = ['POST'])
def create_transaction():
    a = request.get_json(force=True)
    id = a['id']
    ring = _node.ring
    _wallet = None
    for i in ring:
        if id == i['id']:
            _wallet = i['pkey']
    amount = a['amount']
    new_transaction = _node.create_transaction(_wallet, amount)
    _node.broadcast_transaction(new_transaction)
    return jsonify(status="ok")
    
@app.route('/receivetransaction', methods = ['POST'])
def receive_transaction():
    _node.tcounter+=1
    if _node.tcounter == 10*config.numofnodes:
        _node.stop_if_empty = True
    a = request.get_json(force=True)
    # print("I ENTERED RECEIVE, HERE'S THE TRANSACTION")
    # print(a)
    _node.validate_transaction(a)
    return jsonify(status="ok")

@app.route('/receiveblock', methods = ['POST'])
def receive_block():
    a = request.get_json(force=True)
    _node.receive_block(a)
    return jsonify(status="ok")
    
# --------------------------------------- #    

# ENDPOINT USED FOR RESOLVE CONFLICTS     #
# --------------------------------------- # 
@app.route('/chainlength', methods = ['GET'])
def chain_len():
    _len = len(_node.chain)
    return jsonify(length=_len)

@app.route('/startwork', methods = ['GET'])
def try_mine():
    _node.continuous_mining()




@app.route('/timerstart', methods = ['GET'])
def start_timer():
    _node.start_time = time.time()
    return jsonify(status="ok")

@app.route('/totaltime', methods = ['GET'])
def get_timer():
    ret = _node.total_time
    if _node.btcounter == 0:
        return jsonify(time_transactions=ret,avg_time_mine=0,blocks_mined=0)
    else:
        ret_block = _node.btsum / _node.btcounter
        return jsonify(time_transactions=ret,avg_time_mine=ret_block,blocks_mined = _node.btcounter)



# @app.route('/forceminetrigger', methods = ['GET'])
# def force_mine():
#     force_result = _node.force_mine()
#     if force_result == 0:
#         return jsonify(status="did something")
#     else:
#         return jsonify(status="all work done")







@app.route('/chain', methods = ['GET'])
def chain_send():
    chain = _node.chain
    return jsonify(chain=chain)


if __name__ == '__main__':
    from argparse import ArgumentParser
    parser = ArgumentParser()
    parser.add_argument('-p', default=5000, help='port to listen on')
    parser.add_argument('-diff', default=4, help='set difficulty of POW')
    parser.add_argument('-ip', help='ip to listen on')
    parser.add_argument('-bip', help='bootstrap ip, -1 if bootstrap')
    parser.add_argument('-bport', help='bootstrap port, -1 if bootstrap')
    args = parser.parse_args()
    config.difficulty = int(args.diff)
    port = args.p
    _node = node.Node(args.ip, args.p, args.bip, args.bport)

    app.run(host='0.0.0.0', port=port, threaded=True)
