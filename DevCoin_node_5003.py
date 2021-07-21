#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: dev
"""

from flask import Flask, jsonify, request
from modules.blockchain import Blockchain
from uuid import uuid4

#Basic Web app
app = Flask(__name__)

#First node
node_address = str(uuid4()).replace('-', '')
    
#Main Blockchain object
blockchain = Blockchain()
                
#Mine fns
@app.route('/mine_block', methods = ['GET'])
def mine_block():
    previous_block = blockchain.get_previous_block()
    previous_proof = previous_block['proof']
    proof = blockchain.proof_of_work(previous_proof)            
    previous_hash = blockchain.hash(previous_block)
    blockchain.add_transaction(sender = node_address, receiver = 'Dev', amount = 50)
    block = blockchain.create_block(proof, previous_hash)
    response = {'message' : 'Dev personally congratulates you on mining a block!',
                'index' : block['index'],
                'timestamp' : block['timestamp'],
                'proof' : block['proof'],
                'previous_hash' : block['previous_hash'],
                'transactions' : block['transactions']}

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

#Add tx
@app.route('/add_transaction', methods = ['POST'])
def add_transaction():
    json = request.get_json()
    transaction_keys = {'sender', 'receiver', 'amount'}
    
    if not all (key in json for key in transaction_keys):
        return 'Key fields are missing, check request.', 400
    
    index = blockchain.add_transaction(json['sender'], json['receiver'], json['amount'])
    response = {'message' : f'Transaction added to block {index}.'}
    return jsonify(response), 201

#Connect new nodes
@app.route('/connect_node', methods = ['POST'])
def connect_node():
    json = request.get_json()
    nodes = json.get('nodes')
    
    if nodes is None:
        return "No node added.", 400
    
    for node in nodes:
        blockchain.add_node(node)
    response = {'message' : 'All nodes connected. DevCoin now contains the following nodes:',
                'total_nodes' : list(blockchain.nodes)}
    return jsonify(response), 201

#Longest chain wins
@app.route('/replace_chain', methods = ['GET'])
def replace_chain():
    is_chain_replaced = blockchain.replace_chain()
    if is_chain_replaced == True:
        message = 'Chain replaced, the longest chain won!'
    else:
        message = 'Current chain is the longest.'
        
    response = {'message' : message,
                'current_chain' : blockchain.chain}
    return jsonify(response), 200 
    
#App
app.run(host = '0.0.0.0', port = 5003)