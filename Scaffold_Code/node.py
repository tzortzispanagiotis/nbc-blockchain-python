from Scaffold_Code import block, wallet , config ,chain , transaction

class Node: #creation of bootstap node
	def __init__(self):
		#self.NBC=100
		##set
		self.current_block  = [] #san transaction pool me transactions<=maximum
		self.chain = []
		#self.current_id_count
		self.wallet = create_wallet()
		self.transaction_pool
		self.UTXO = []
		#slef.ring[]   #here we store information for every node, as its id, its address (ip:port) its public key and its balance 




	#def create_new_block(previousHash): #an einai to proto 
				
		

		
	def create_wallet():
		##create a wallet for this node, with a public key and a private key
		return Wallet()

	def register_node_to_ring():
		#add this node to the ring, only the bootstrap node can add a node to the ring after checking his wallet and ip:port address
		#bottstrap node informs all other nodes and gives the request node an id and 100 NBCs
        return True 

	def create_transaction(sender, receiver,amount ,  signature , wallet):
		traninput = []
		#inputs ola ta outputs pou exoun os receiver ton torino sender
		for i in UTXO:
			if (i.recepient==sender):
				traninput.append(i)
        new_transaction = Transaction(wallet , receiver , amount , traninput)
		new_transaction.add_id_to_output()	    
		#remember to broadcast it


	def broadcast_transaction():


	def verify_signature(transaction):
		tr = transaction.to_dict1(False)
		pubkey= RSA.importKey(binascii.unhexlify(tr)
	    verifier = PKCS1_v1_5.new(pubkey)
		h = SHA.new(message.encode('utf8'))
	    return verifier.verify(h, binascii.unhexlify(transaction.signature))



	def validate_transaction(transaction):
		#when receiving a transaction, first validate with the signature
		#second, check if UTXOs are enough to make the transaction
		#if validation is OK, add transaction to current block
		if (verify_signature(transaction)):

			if not isinstance(transaction, GenesisTransaction): {

			# Verify input transactions
			for tx in transaction.inputs:
				if not validate_transaction(tx.transaction): 
					logging.error("Invalid parent transaction")
					return False
			}
			return True
		return False

	def add_transaction_to_block(current_block , transaction , previousHash): 
		#if
		#if enough transactions  mine
		if validate_transaction(transaction):
		{
			if (len(current_block) == max_transactions):
				new_block = Block(previousHash , current_block)
				mine_block(new_block)
			
		    else:
				current_block.append(transaction)
		}



	def mine_block( block , self  ):
		 last_block = self.chain[-1]
		 message = to_dict(last_block)
		 nonce = self.valid_proof(message)
		 block.add_nonce(nonce)
		 self.broadcast_block()
		 chain.add_block_to_mychain(block)



	def broadcast_block():


	

	def valid_proof(message , difficulty):
		i = 0
    	prefix = '0' * difficulty
    	while True:
			nonce = str(i)
			digest = dumb_hash(message + nonce)
			if digest.startswith(prefix):
				return nonce
			i += 1



	#concencus functions

	def valid_chain(self, chain):
		#check for the longer chain accroose all nodes


	def resolve_conflicts(self):
		#resolve correct chain



