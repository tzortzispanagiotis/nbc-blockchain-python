from collections import OrderedDict

import binascii

import Crypto
import Crypto.Random
from Crypto.Hash import SHA
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5

import requests
from flask import Flask, jsonify, request, render_template

class TransactionInput:
#input points to output
    def __init__(self, transaction, output_idx):
        previousOutputId = transaction.

class TransactionOutput:
    def __init__(self, transaction, amount):
        self.recipient = transaction.receiver_address
        self.amount = amount
        self.id = #το hash
        self.transactionId = transaction.id

    def to_dict(self):
        d = {
            'sender_address': self.sender_address
            'recipient_address': self.recipient,
            'amount': self.amount

        }
        return d


class Transaction:

    def __init__(self, wallet, recipient_address, value):

        #set


        self.sender_address = wallet.address #To public key του wallet από το οποίο προέρχονται τα χρήματα
        self.receiver_address = recipient_address #To public key του wallet στο οποίο θα καταλήξουν τα χρήματα
        self.amount = value #το ποσό που θα μεταφερθεί
        self.transaction_id =  #το hash του transaction
        self.transaction_inputs: #λίστα από Transaction Input
        self.transaction_outputs: #λίστα από Transaction Output
        self.signature


    


    def to_dict1(self,include_signature=True):
        d = {
            "inputs": list(map(TransactionInput.to_dict, self.inputs)),
            "outputs": list(map(TransactionOutput.to_dict, self.outputs)),
        
        }
        if include_signature:
            d["signature"] = self.signature
        return d
        

    def sign_transaction(self):
        """
        Sign transaction with private key
        """
       private_key = RSA.importKey(binascii.unhexlify(self.sender_private_key))
       signer = PKCS1_v1_5.new(private_key)
       h = SHA.new(str(self.to_dict()).encode('utf8'))
       return binascii.hexlify(signer.sign(h)).decode('ascii')
