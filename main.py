#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: dev
"""

from flask import Flask, jsonify
from modules.blockchain import Blockchain

#Basic Web app
app = Flask(__name__)
    
#Main Blockchain object
blockchain = Blockchain()
                
#Mine fns
@app.route('/mine_block', methods = ['GET'])
def mine_block():
    previous_block = blockchain.get_previous_block()
    previous_proof = previous_block['proof']
    proof = blockchain.proof_of_work(previous_proof)            
    previous_hash = blockchain.hash(previous_block)
    block = blockchain.create_block(proof, previous_hash)
    response = {'message' : 'Dev personally congratulates you on mining a block!',
                'index' : block['index'],
                'timestamp' : block['timestamp'],
                'proof' : block['proof'],
                'previous_hash' : block['previous_hash']}

    return jsonify(response), 200 #OK http code

#Get full blockchain
@app.route('/get_chain', methods = ['GET'])
def get_chain():
    response = {'chain' : blockchain.chain,
                'length' : len(blockchain.chain)}
    
    return jsonify(response), 200

#Check validity
@app.route('/is_valid', methods = ['GET'])
def is_valid():
    message = 'No'
    if blockchain.is_chain_valid(blockchain.chain) == True:
        message = 'Yes'
    response = {'message' : message}
    
    return jsonify(response), 200

#App
app.run(host = '0.0.0.0', port = 5000)