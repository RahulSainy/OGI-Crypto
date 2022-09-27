from uuid import uuid4
from blockchain import Blockchain
from verifiaction import Verification

class Node:

    def __init__(self) :
        self.id = Blockchain(uuid4())
        self.blockchain = Blockchain(self.id)

    def get_transaction_value(self):
        tx_recipient = input("Enter recipient of transaction : ", )
        tx_amount = float(input("Enter Transaction amount : ", ))

        # this is a tupel ! also can be created without pranthesis here
        return (tx_recipient, tx_amount)

    def get_user_choice(self):
        user_input = input("Your Choice: ")
        return user_input

    def print_blockchain_elements(self):
        for block in self.blockchain.chain:
            print("Outputting Block")
            print(block)
        else:
            print("-"*20)

    def listen_for_input(self):
        waiting_for_input = True
        while waiting_for_input:
            print("Please Choose")
            print("1. Add New Transaction Value ")
            print("2. Mine New Block ")
            print("3. Output The Blockchain Block")
            print("4.Check Transaction Validity ")

            # print("h. Manipulate the chain")
            print("q: Quit")

            user_choice = self.get_user_choice()
            if user_choice == '1':
                tx_data = self.get_transaction_value()
                # tuple unpacking !
                recipient, amount = tx_data
                if self.blockchain.add_transaction(recipient,self.id, amount=amount):
                    print('Added Transactions!')
                else:
                    print('Transactions Failed!')
                print(self.blockchain.get_open_transactions())

            elif user_choice == '2':
                self.blockchain.mine_block()

            elif user_choice == '3':
                self.print_blockchain_elements()
            elif user_choice == '4':
                print("runs")
                #used instance method now uses direct method callling using decorator 
                # verifier = Verification()
                if Verification.verify_transactions(self.blockchain.get_open_transactions(), self.blockchain.get_blance):
                    print("All Transacitons Are Valid")
                else:
                    print("Invalid Transactions")

            # elif user_choice == 'h':
            #     if len(blockchain) >= 1:
            #         blockchain[0] = {'previous_hash': '',
            #                          'index': 0,
            #                          'transactions': [{'sensder': 'cris', 'recipient': 'max', 'amount': '440.0'}]}
            elif user_choice == 'q':
                waiting_for_input = False
            else:
                print('Input was invalid, please pick a value from the list!')
            #used instance method now uses direct method callling using decorator 
            # verifier = Verification()
            if not Verification.verify_chain(self.blockchain.chain):
                self.print_blockchain_elements()
                print('Invalid blockchain!')
                # Break out of the loop
                break
            print('Balance of {}: {:6.2f}'.format(self.id, self.blockchain.get_blance()))
        else:
            print("-"*20)
            print("user Left")

        print("done!")

node = Node()
node.listen_for_input()