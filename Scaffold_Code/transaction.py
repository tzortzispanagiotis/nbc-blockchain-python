from collections import OrderedDict

import binascii
import hashlib
import json
import Crypto
import Crypto.Random
from Crypto.Hash import SHA
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5
import requests
from flask import Flask, jsonify, request, render_template

class TransactionInput:
#input points to output
    def __init__(self, transactionoutput):
        self.parentOutputId = transactionoutput.transactionId

    def to_dict(self):
        d = {
            'parentTransaction':self.parentOutputId 
        }
        return d 

class TransactionOutput:
    def __init__(self, receiver_address, amount):
        self.recipient =receiver_address
        self.amount = amount
        self.transactionId = None

    def fill_id(self , tid):
        self.transactionId=tid

    def to_dict(self):
        d = {
            #'sender_address': self.sender_address
            'recipient': self.recipient,
            'amount': self.amount

        }
        return d


class Transaction:

    def __init__(self, wallet, recipient_address, value,UTXOS ):

        #set

        self.wallet=wallet
        self.sender_address = wallet.getAddress() #To public key του wallet από το οποίο προέρχονται τα χρήματα
        self.receiver_address = recipient_address #To public key του wallet στο οποίο θα καταλήξουν τα χρήματα
        self.amount = value #το ποσό που θα μεταφερθεί
        self.transaction_inputs= UTXOS
        self.transaction_outputs=self.createOutputs()#λίστα από Transaction Output
        self.signature =wallet.sign_transaction(self.to_dict1(False))
        self.transaction_id =self.hash_transaction() #το hash του transaction



    def createOutputs(self):
        out=[]
        #output gia ton reciever
        output1=TransactionOutput(self.receiver_address , self.amount)
        #afta pou perisepsan se afton pou esteile
        output2=TransactionOutput(self.sender_address , self.wallet.get_balance()-self.amount)
        out.append(output1)
        out.append(output2)
        return out

    def getid(self):
        return self.transaction_id 



    def to_dict1(self,include_signature=True):
        d = {
            "inputs": list(map(TransactionInput.to_dict, self.transaction_inputs)),
            "outputs": list(map(TransactionOutput.to_dict, self.transaction_outputs)),
        }
        #to message pou upografw kai meta elegxw an antistoixei stin upografi apoteleitai mono apo ta 
        #inputs kai ta outputs
        if include_signature:
            d["signature"] = self.signature
        return d
        
    def hash_transaction(self):
         return  hashlib.sha256(json.dumps(self.to_dict1(True)))
    def get_receiver(self):
         return  self.receiver_address

    def add_id_to_output(self):
        for out in self.transaction_outputs:
            out.fill_id(self.transaction_id)

   