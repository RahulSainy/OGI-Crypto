import utility.hash_util as hash_util

class Verification:
    
    @staticmethod
    def valid_proof(transactions, last_hash, proof):
        guess = (str([tx.to_ordered_dict for tx in transactions]) +
                str(last_hash)+str(proof)).encode()

        #  guess_hash = hl.sha256(guess).hexdigest()
        # outsourced uing hash utol lib below
        guess_hash = hash_util.hash_string_256(guess)

        return guess_hash[0:2] == '00'

    @classmethod
    def verify_chain(cls,blockchain):
        # enumrate makes list into tup;e
        for (index, block) in enumerate(blockchain):
            if index == 0:
                continue
            if block.previous_hash != hash_util.hash_block(blockchain[index - 1]):
                return False
            if not cls.valid_proof(block.transactions[:-1], block.previous_hash, block.proof):
                return False
        return True

    @staticmethod
    def verify_transaction(transaction,get_blance):
        sender_balance = get_blance(transaction.sender)
        return sender_balance >= transaction.amount

    @classmethod
    def verify_transactions(cls,open_transactions,get_balance):
        return all([cls.verify_transaction(tx, get_balance) for tx in open_transactions])
        # is_valid = True
        # for tx in open_transactions:
        #  if verify_transaction(tx):
        #     is_valid = True
        # else:
        #     is_valid = False
        # return is_valid

