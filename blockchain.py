MINNING_REWARD = 10

genesis_block = {'previos_hash': '',
                 'index': 0,
                 'transactions': []}
blockchain = [genesis_block]
open_transations = []
owner = 'Max'
participants = {'Max'}


def hash_block(block):
    return '-'.join([str(block[key]) for key in block])


def get_blance(partcipant):
    tx_sender = [[tx['ammount'] for tx in block['transactions']
                  if tx['sender'] == partcipant] for block in blockchain]
    open_tx_sender = [tx['ammount'] for tx in open_transations if tx['sender'] == partcipant]
    tx_sender.append(open_tx_sender)
    ammount_sent = 0
    for tx in tx_sender:
        if len(tx) > 0:
            ammount_sent += tx[0]
    tx_recipent = [[tx['ammount'] for tx in block['transactions']
                  if tx['recipent'] == partcipant] for block in blockchain]
    ammount_recieved = 0
    for tx in tx_recipent:
        if len(tx) > 0:
            ammount_recieved += tx[0]
    return ammount_recieved - ammount_sent


def get_last_blockchain_value():
    if len(blockchain) < 1:
        return None
    return blockchain[-1]

def verify_transaction(transaction):
    sender_balance = get_blance(transaction['sender'])
    return sender_balance >= transaction['ammount']
    

def add_transaction(recipent, sender=owner, ammount=1.0):
    """
 Arguments: 
    :sender: The Sender Of Coins.
    :recipent: The Reciver Of Coins.
    :ammount: The ammount Of Coins ( default = 1.0).

    """
    transaction = {'sender': sender, 'recipent': recipent, 'ammount': ammount}
    
    if  verify_transaction(transaction):
        open_transations.append(transaction)
        participants.add(sender)
        participants.add(recipent)
        return True
    return False

    # if last_transaction == None:
    #     last_transaction = [1]

    # blockchain.append([last_transaction, transaction_amount])


def mine_block():
    last_block = blockchain[-1]
    hashed_block = hash_block(last_block)
    # for key in last_block:
    #     value = last_block[key]
    #     hashed_block = hashed_block + str(value)
    reward_transaction = {
        'sender': 'MINING',
        'recipent': owner,
        'ammount': MINNING_REWARD
    }
    copied_transactions = open_transations
    open_transations.append(reward_transaction)
    block = {'previous_hash': hashed_block,
             'index': len(blockchain),
             'transactions': open_transations}
    blockchain.append(block)
    return True


def get_transaction_value():
    tx_recipent = input("Enter recipent of transaction : ", )
    tx_ammount = float(input("Enter Transaction ammount : ", ))

    # this is a tupel ! also can be created without pranthesis here
    return (tx_recipent, tx_ammount)


def get_user_choice():
    user_input = input("Your Choice: ")
    return user_input


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
        if block['previous_hash'] != hash_block(blockchain[index - 1]):
            return False
    return True

def verify_transactions():
    return all([verify_transaction(tx) for tx in open_transations])
    # is_valid = True
    # for tx in open_transations:
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
        recipent, ammount = tx_data
        if add_transaction(recipent, ammount=ammount):
            print('Added Transactions!')
        else:
            print('Transactions Failed!')
        print(open_transations)

    elif user_choice == '2':
        if mine_block():
            open_transations = []
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
            blockchain[0] = {'previos_hash': '',
                             'index': 0,
                             'transactions': [{'sensder': 'cris', 'recipent': 'max', 'ammount': '440.0'}]}
    elif user_choice == 'q':
        waiting_for_input = False
    else:
        print('Input was invalid, please pick a value from the list!')
    if not verify_chain():
        print_blockchain_elements()
        print('Invalid blockchain!')
        # Break out of the loop
        break
    print(get_blance('Max'))
else:
    print("-"*20)
    print("user Left")


print("done!")
