from functools import reduce
import hashlib as hl
from collections import OrderedDict
import json
from typing import IO
# import pickle

import hash_util

MINNING_REWARD = 10
#modified in exception handling in load_data()
# genesis_block = {'previous_hash': '',
#                  'index': 0,
#                  'transactions': [],
#                  'proof': 100}
# blockchain = [genesis_block]
blockchain = []

open_transactions = []
owner = 'Max'
participants = {'Max'}


def load_data():
    """Initialize blockchain + open transactions data from a file."""
    global blockchain
    global open_transactions
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
                updated_block = {
                    'previous_hash': block['previous_hash'],
                    'index': block['index'],
                    'proof': block['proof'],
                    'transactions': [OrderedDict(
                        [('sender', tx['sender']), ('recipient', tx['recipient']), ('amount', tx['amount'])]) for tx in block['transactions']]
                }
                updated_blockchain.append(updated_block)
            blockchain = updated_blockchain
            open_transactions = json.loads(file_content[1])
            # converted  the loaded data because Transactions should use OrderedDict
            updated_transactions = []
            for tx in open_transactions:
                updated_transaction = OrderedDict(
                    [('sender', tx['sender']), ('recipient', tx['recipient']), ('amount', tx['amount'])])
                updated_transactions.append(updated_transaction)
            open_transactions = updated_transactions
    except IOError:
        genesis_block = {'previous_hash': '',
                 'index': 0,
                 'transactions': [],
                 'proof': 100}
        blockchain = [genesis_block]
        open_transactions = []
    finally:
        print('Cleanup!')
load_data()


def save_data():
    """Save blockchain + open transactions snapshot to a file."""
    try:
        with open('E:/Courses/Python - The Practical Guide [Edition]/Mycode/OGI-Crypto/blockChain.txt', mode='w') as f:
            f.write(json.dumps(blockchain))
            f.write('\n')
            f.write(json.dumps(open_transactions))
            # save_data = {
            #     'chain': blockchain,
            #     'ot': open_transactions
            # }
            # f.write(pickle.dumps(save_data))
        print('Saving failed!')
    except IOError:
        print('Save Failed')



def valid_proof(transactions, last_hash, proof):
    guess = (str(transactions) + str(last_hash)+str(proof)).encode()

    #  guess_hash = hl.sha256(guess).hexdigest()
    # outsourced uing hash utol lib below
    guess_hash = hash_util.hash_string_265(guess)

    return guess_hash[0:2] == '00'


def proof_of_work():
    last_block = blockchain[-1]
    last_hash = hash_util.hash_block(last_block)
    proof = 0
    while not valid_proof(open_transactions, last_hash, proof):
        proof += 1
    return proof


def get_blance(partcipant):
    tx_sender = [[tx['amount'] for tx in block['transactions']
                  if tx['sender'] == partcipant] for block in blockchain]
    open_tx_sender = [tx['amount']
                      for tx in open_transactions if tx['sender'] == partcipant]
    tx_sender.append(open_tx_sender)
    amount_sent = reduce(
        lambda tx_sum, tx_amt: tx_sum + sum(tx_amt) if len(tx_amt) > 0 else tx_sum+0, tx_sender, 0)
    # tx_amt[0] gave only first value so changed to sum(tx_amt)
    # old way below!
    # amount_sent = 0
    # for tx in tx_sender:
    #     if len(tx) > 0:
    #         amount_sent += tx[0]
    tx_recipient = [[tx['amount'] for tx in block['transactions']
                    if tx['recipient'] == partcipant] for block in blockchain]

    amount_recieved = reduce(
        lambda tx_sum, tx_amt: tx_sum+sum(tx_amt) if len(tx_amt) > 0 else tx_sum + 0, tx_recipient, 0)
    # old way below!
    # amount_recieved = 0
    # for tx in tx_recipient:
    #     if len(tx) > 0:
    #         amount_recieved += tx[0]
    return amount_recieved - amount_sent


def get_last_blockchain_value():
    if len(blockchain) < 1:
        return None
    return blockchain[-1]


def verify_transaction(transaction):
    sender_balance = get_blance(transaction['sender'])
    return sender_balance >= transaction['amount']


def add_transaction(recipient, sender=owner, amount=1.0):
    """
 Arguments:
    :sender: The Sender Of Coins.
    :recipient: The Reciver Of Coins.
    :amount: The amount Of Coins ( default = 1.0).

    """
    # transaction = {'sender': sender, 'recipient': recipient, 'amount': amount}
    transaction = OrderedDict(
        [('sender', sender), ('recipient', recipient), ('amount', amount)])
    if verify_transaction(transaction):
        open_transactions.append(transaction)
        participants.add(sender)
        participants.add(recipient)
        return True
    return False

    # if last_transaction == None:
    #     last_transaction = [1]

    # blockchain.append([last_transaction, transaction_amount])


def mine_block():
    last_block = blockchain[-1]
    hashed_block = hash_util.hash_block(last_block)
    proof = proof_of_work()
    # for key in last_block:
    #     value = last_block[key]
    #     hashed_block = hashed_block + str(value)
    # reward_transaction = {
    #     'sender': 'MINING',
    #     'recipient': owner,
    #     'amount': MINNING_REWARD
    # }
    reward_transaction = transaction = OrderedDict(
        [('sender', 'MINING'), ('recipient', owner), ('amount', MINNING_REWARD)])
    copied_transactions = open_transactions
    open_transactions.append(reward_transaction)
    block = {'previous_hash': hashed_block,
             'index': len(blockchain),
             'transactions': open_transactions,
             'proof': proof}
    blockchain.append(block)
    return True


def get_transaction_value():
    tx_recipient = input("Enter recipient of transaction : ", )
    tx_amount = float(input("Enter Transaction amount : ", ))

    # this is a tupel ! also can be created without pranthesis here
    return (tx_recipient, tx_amount)


def get_user_choice():
    user_input = input("Your Choice: ")
    return user_input


0000000


def print_blockchain_elements():
    for block in blockchain:
        print(block)
        print(blockchain)
    else:
        print("-"*20)


def verify_chain():
    # enumrate makes list into tup;e
    for (index, block) in enumerate(blockchain):
        if index == 0:
            continue
        if block['previous_hash'] != hash_util.hash_block(blockchain[index - 1]):
            return False
        if not valid_proof(block['transactions'][:-1], block['previous_hash'], block['proof']):
            return False
    return True


def verify_transactions():
    return all([verify_transaction(tx) for tx in open_transactions])
    # is_valid = True
    # for tx in open_transactions:
    #  if verify_transaction(tx):
    #     is_valid = True
    # else:
    #     is_valid = False
    # return is_valid


waiting_for_input = True

while waiting_for_input:
    print("Please Choose")
    print("1. Add New Transaction Value ")
    print("2. Mine New Block ")
    print("3. Output The Blockchain Block")
    print("4. Output The Participants")
    print("5.Check Transaction Validity ")

    print("h. Manipulate the chain")
    print("q: Quit")

    user_choice = get_user_choice()
    if user_choice == '1':
        tx_data = get_transaction_value()
        # tuple unpacking !
        recipient, amount = tx_data
        if add_transaction(recipient, amount=amount):
            print('Added Transactions!')
        else:
            print('Transactions Failed!')
        print(open_transactions)

    elif user_choice == '2':
        if mine_block():
            open_transactions = []
            save_data()

    elif user_choice == '3':
        print_blockchain_elements()
    elif user_choice == '4':
        print(participants)
    elif user_choice == '5':
        print("runs")
        if verify_transactions():
            print("All Transacitons Are Valid")
        else:
            print("Invalid Transactions")

    elif user_choice == 'h':
        if len(blockchain) >= 1:
            blockchain[0] = {'previous_hash': '',
                             'index': 0,
                             'transactions': [{'sensder': 'cris', 'recipient': 'max', 'amount': '440.0'}]}
    elif user_choice == 'q':
        waiting_for_input = False
    else:
        print('Input was invalid, please pick a value from the list!')
    if not verify_chain():
        print_blockchain_elements()
        print('Invalid blockchain!')
        # Break out of the loop
        break
    print('Balance of {}: {:6.2f}'.format('Max', get_blance('Max')))
else:
    print("-"*20)
    print("user Left")


print("done!")
