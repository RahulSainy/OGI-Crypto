from collections import OrderedDict
from functools import reduce
import hashlib as hl
import json
from uuid import uuid4

# import pickle

import hash_util
from transaction import Transaction
from block import Block
from verifiaction import Verification


MINNING_REWARD = 10

class Blockchain:
    def __init__(self, hosting_node_id):
        # Our starting block for the blockchain
        genesis_block = Block(0, '', [], 100, 0)
        # initializing empt blockchain list
        self.chain = [genesis_block]
        # unhandeld Transactions 
        self.open_transactions=[]
        self.load_data()
        self.hosting_node = hosting_node_id



# modified in exception handling in load_data()
# genesis_block = {'previous_hash': '',
#                  'index': 0,
#                  'transactions': [],
#                  'proof': 100}
# blockchain = [genesis_block]


    def load_data(self):
        """Initialize blockchain + open transactions data from a file."""
        try:
            with open('E:/Courses/Python - The Practical Guide [Edition]/Mycode/OGI-Crypto/blockChain.txt', mode='r') as f:

                # file_content = pickle.loads(f.read())
                file_content = f.readlines()
                # blockchain = file_content['chain']
                # open_transactions = file_content['ot']
                blockchain = json.loads(file_content[0][:-1])
                # converted  the loaded data because Transactions should use OrderedDict
                updated_blockchain = []
                for block in blockchain:
                    converted_tx = [Transaction(tx['sender'], tx['recipient'], tx['amount']) for tx in block['transactions']]
                    updated_block = Block(
                        block['index'], block['previous_hash'], converted_tx, block['proof'], block['timestamp'])
                    updated_blockchain.append(updated_block)
                self.chain = updated_blockchain
                open_transactions = json.loads(file_content[1])
                # We need to convert  the loaded data because Transactions should use OrderedDict
                updated_transactions = []
                for tx in open_transactions:
                    updated_transaction = Transaction(
                        tx['sender'], tx['recipient'], tx['amount'])
                    updated_transactions.append(updated_transaction)
                self.open_transactions = updated_transactions
        except (IOError, IndexError):
            pass
        finally:
            print('Cleanup!')


    


    def save_data(self):
        """Save blockchain + open transactions snapshot to a file."""
        try:
            with open('E:/Courses/Python - The Practical Guide [Edition]/Mycode/OGI-Crypto/blockChain.txt', mode='w') as f:
                saveable_chain = [block.__dict__ for block in [Block(block_el.index, block_el.previous_hash, [
                                                                    tx.__dict__ for tx in block_el.transactions], block_el.proof, block_el.timestamp) for block_el in self.chain]]
                f.write(json.dumps(saveable_chain))
                f.write('\n')
                saveable_tx = [tx.__dict__ for tx in self.open_transactions]
                f.write(json.dumps(saveable_tx))
                # save_data = {
                #     'chain': blockchain,
                #     'ot': open_transactions
                # }
                # f.write(pickle.dumps(save_data))

        except (IOError):
            print('Save Failed')



    def proof_of_work(self):
        last_block = self.chain[-1]
        last_hash = hash_util.hash_block(last_block)
        proof = 0
        verifier =  Verification()
        while not verifier.valid_proof(self.open_transactions,last_hash, proof):
            proof += 1
        return proof


    def get_blance(self,partcipant):
        tx_sender = [[tx.amount for tx in block.transactions
                    if tx.sender == partcipant] for block in self.chain]
        open_tx_sender = [tx.amount
                        for tx in self.open_transactions if tx.sender == partcipant]
        tx_sender.append(open_tx_sender)
        amount_sent = reduce(
            lambda tx_sum, tx_amt: tx_sum + sum(tx_amt) if len(tx_amt) > 0 else tx_sum+0, tx_sender, 0)
        # tx_amt[0] gave only first value so changed to sum(tx_amt)
        # old way below!
        # amount_sent = 0
        # for tx in tx_sender:
        #     if len(tx) > 0:
        #         amount_sent += tx[0]
        tx_recipient = [[tx.amount for tx in block.transactions
                        if tx.recipient == partcipant] for block in self.chain]

        amount_recieved = reduce(
            lambda tx_sum, tx_amt: tx_sum+sum(tx_amt) if len(tx_amt) > 0 else tx_sum + 0, tx_recipient, 0)
        # old way below!
        # amount_recieved = 0
        # for tx in tx_recipient:
        #     if len(tx) > 0:
        #         amount_recieved += tx[0]
        return amount_recieved - amount_sent


    def get_last_blockchain_value(self):
        if len(self.chain) < 1:
            return None
        return self.chain[-1]


    def add_transaction(self, recipient, sender, amount=1.0):
        """
    Arguments:
        :sender: The Sender Of Coins.
        :recipient: The Reciver Of Coins.
        :amount: The amount Of Coins ( default = 1.0).

        """
        transaction = Transaction(sender, recipient, amount)
        # transaction = {'sender': sender, 'recipient': recipient, 'amount': amount}
        #######
        # transaction = OrderedDict(
        #     [('sender', sender), ('recipient', recipient), ('amount', amount)])
        verifier =  Verification()
        if verifier.verify_transaction(transaction, self.get_blance):
            self.open_transactions.append(transaction)
            # participants.add(sender)
            # participants.add(recipient)
            self.save_data()
            return True
        return False

        # if last_transaction == None:
        #     last_transaction = [1]

        # blockchain.append([last_transaction, transaction_amount])


    def mine_block(self, node):
        last_block = self.chain[-1]
        hashed_block = hash_util.hash_block(last_block)
        proof = self.proof_of_work()
        # for key in last_block:
        #     value = last_block[key]
        #     hashed_block = hashed_block + str(value)
        # reward_transaction = {
        #     'sender': 'MINING',
        #     'recipient': owner,
        #     'amount': MINNING_REWARD
        # }
        reward_transaction = Transaction('MINING', node, MINNING_REWARD)
        # reward_transaction = transaction = OrderedDict(
        #     [('sender', 'MINING'), ('recipient', owner), ('amount', MINNING_REWARD)])
        copied_transactions = self.open_transactions
        copied_transactions.append(reward_transaction)
        block = Block(len(self.chain), hashed_block, copied_transactions, proof)
        # block = {'previous_hash': hashed_block,
        #          'index': len(blockchain),
        #          'transactions': open_transactions,
        #          'proof': proof}
        self.chain.append(block)
        return True




