import requests
from flask import Flask, jsonify, request, render_template
from flask_cors import CORS

from Scaffold_Code import block, chain, wallet, transaction, node

### JUST A BASIC EXAMPLE OF A REST API WITH FLASK


app = Flask(__name__)
CORS(app)
node = Node()

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
    return jsonify(status=successful)


@app.route('/receivewallets', methods = ['POST'])
def receive_wallets():
    

# get all transactions in the blockchain

@app.route('/transactions/get', methods=['GET'])
def get_transactions():
    transactions = blockchain.transactions

    response = {'transactions': transactions}
    return jsonify(response), 200



# run it once fore every node

if __name__ == '__main__':
    from argparse import ArgumentParser

    parser = ArgumentParser()
    parser.add_argument('-p', '--port', default=5000, type=int, help='port to listen on')
    args = parser.parse_args()
    port = args.port

    app.run(host='127.0.0.1', port=port)