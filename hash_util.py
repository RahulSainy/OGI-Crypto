import json
import hashlib as hl

def hash_string_265(string):
    return hl.sha256(string).hexdigest()

def hash_block(block):
    return hl.sha256(json.dumps(block, sort_keys=True).encode()).hexdigest()
# sudo has wihtout using libeaey below!
# def hash_block(block):
#     return '-'.join([str(block[key]) for key in block ])
