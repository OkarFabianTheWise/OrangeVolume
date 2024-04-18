from solders.pubkey import Pubkey
from solders.signature import Signature


def to_sol_string(address: str):
    return Pubkey.from_string(address)

def to_signature_string(address: str):
    return Signature.from_string(address)