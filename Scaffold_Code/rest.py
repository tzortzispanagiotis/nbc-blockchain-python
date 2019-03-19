import requests, json
from flask import Flask, jsonify, request, render_template
from flask_cors import CORS

# import block, chain, wallet, transaction
import node

### JUST A BASIC EXAMPLE OF A REST API WITH FLASK


app = Flask(__name__)
CORS(app)
_node = None

#blockchain = Blockchain()

#.......................................................................................
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

#bootstrap ONLY:
@app.route('/addnode', methods=['POST'])
def add_node():
    newNode = {}
    a = request.get_json(force=True)
    newNode['pkey'] = a['pkey']
    newNode['ip'] = a['ip']
    newNode['port'] = a['port']
    # print(newNode)
    _node.register_node_to_ring(newNode)
    return jsonify(status='successful')

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
    

# get all transactions in the blockchain

# @app.route('/transactions/get', methods=['GET'])
# def get_transactions():
#     transactions = blockchain.transactions
#     response = {'transactions': transactions}
#     return jsonify(response), 200



# run it once fore every node

if __name__ == '__main__':
    from argparse import ArgumentParser

    parser = ArgumentParser()
    parser.add_argument('-p', default=5000, help='port to listen on')
    parser.add_argument('-ip', help='ip to listen on')
    parser.add_argument('-bip', help='bootstrap ip, -1 if bootstrap')
    parser.add_argument('-bport', help='bootstrap port, -1 if bootstrap')
    args = parser.parse_args()
    port = args.p
    _node = node.Node(args.ip, args.p, args.bip, args.bport)
    # print (_node.bootstrapip)
    # print('a')
    app.run(host='127.0.0.1', port=port)
