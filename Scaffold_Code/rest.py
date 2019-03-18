import requests, json
from flask import Flask, jsonify, request, render_template
from flask_cors import CORS

# from Scaffold_Code import block, chain, wallet, transaction, node

### JUST A BASIC EXAMPLE OF A REST API WITH FLASK


app = Flask(__name__)
CORS(app)


#blockchain = Blockchain()

#.......................................................................................


#bootstrap ONLY:
@app.route('/addnode', methods=['POST'])
def add_node():
    newNode = {}
    newNode['pkey'] = request.form.get('pkey')
    newNode['ip'] = request.form.get('ip')
    newNode['port'] = request.form.get('port')
    node.register_node_to_ring(newNode)
    return jsonify(status='successful')


@app.route('/receivewallets', methods = ['POST'])
def receive_wallets():
    return True
    

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
    parser.add_argument('-p', '--port', default=5000, type=int, help='port to listen on')
    parser.add_argument('-ip', help='ip to listen on')
    parser.add_argument('-bip', help='bootstrap ip, -1 if bootstrap')
    parser.add_argument('-bport', help='bootstrap port, -1 if bootstrap')
    args = parser.parse_args()
    port = args.port
    # node = Node(args.port, args.ip, args.bip, args. bport)
    if node.bootstrapip != -1:
        temp = {
				'pkey' : node.wallet.address,
				'ip'		: node.ring[0]['ip'],
				'port'   : node.ring[0]['port']
			}
        body = json.dumps(temp)
        r = requests.post(node.bootstrapip+':'+node.bootstrapport+'/addnode', data = body )
    app.run(host='127.0.0.1', port=port)