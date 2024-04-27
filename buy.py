from spl.token.instructions import close_account, CloseAccountParams
from spl.token.client import Token
from spl.token.core import _TokenCore

from solana.rpc.commitment import Commitment
from solana.rpc.api import RPCException
from solders.keypair import Keypair
from solders.pubkey import Pubkey
from solana.rpc.api import Client
from create_close_account import get_token_account, get_token_account, make_swap_instruction
from utils import to_signature_string
import json

endpoint = "https://api.mainnet-beta.solana.com"
#"https://solana-mainnet.core.chainstack.com/09bd70b85bb848a5f59c0e384bdcb948"
url = 'https://solana-mainnet.g.alchemy.com/v2/z9C5AM0W9ltsD2HBSbmCgaByy9FSZASc'
solana_client = Client(endpoint)

print(solana_client.is_connected())

import time, base58


LAMPORTS_PER_SOL = 1000000000

poolkeysbonk = {'amm_id': Pubkey.from_string(
    'GGj7YKTJdavHv2F7WcCic2SqEdPcZK1EWFfGDZMbDLo4',
), 'authority': Pubkey.from_string(
    '5Q544fKrFoe6tsEbD7S8EmxGTJYAKtTVhAW5Q5pge4j1',
), 'base_mint': Pubkey.from_string(
    'So11111111111111111111111111111111111111112',
), 'base_decimals': 9, 'quote_mint': Pubkey.from_string(
    'DezXAZ8z7PnrnRJjz3wXBoRgixCa6xjnB7YaB1pPB263',
), 'quote_decimals': 5, 'lp_mint': Pubkey.from_string(
    'CEJvVaWazAhkcQqTS9EoUTrkBr3qHf18zhyfv72DAaRz',
), 'open_orders': Pubkey.from_string(
    '4mhdTamk3wCiZTmoANGvw3iZGW2Lp6jwCjK14qmDf5KC',
), 'target_orders': Pubkey.from_string(
    'CUfxi9Wu2M547HEGSZF7yA5vEQahu5ELwBZBrE3BbetL',
), 'base_vault': Pubkey.from_string(
    'B1mmGm5bveLSwYHkQXPJ7mFb5KBFNa7U9Hma3Qdw1qbd',
), 'quote_vault': Pubkey.from_string(
    'DbPFYPjgCFK6KLJFh55mtn5hEroYcm7Dzs2fYBW3GGy2',
), 'market_id': Pubkey.from_string(
    '5Bbi2ctQPRyGtMyKxeQqLihgVx8ERjedKk49W5vRnux1',
), 'market_base_vault': Pubkey.from_string(
    '71d4tKG12Z5b23REjgngGMFiVpa4WFfzRYEha9tL2XFo',
), 'market_quote_vault': Pubkey.from_string(
    'EqWGX6ajK9nsKHKXusoenxNJiuRJkSLpjCb8knzg2Abi',
), 'market_authority': Pubkey.from_string(
    'Fm5vw8v3my98VaAUezxY7ptkEHk9ki2onMEhaVQHMJog',
), 'bids': Pubkey.from_string(
    'E12pXR4HXZMwGRhudGEhWuzfuMnixezx3T3twfSwVykt',
), 'asks': Pubkey.from_string(
    'HfbAJpm3DBnH46jx1KwYaqFnd47dxgo5uZmnR9gyCWvW',
), 'event_queue': Pubkey.from_string(
    'ES5Y4HACggzRYqaWqtGD1rF2kj9BA154hDJmzwr5LUpz',
)}

poolkeysflush = {'amm_id': Pubkey.from_string(
    'DVj1swqYnqPzPvhwcGe9JvTJ46szGEVCYhrHZ6oUjia9',
), 'authority': Pubkey.from_string(
    '5Q544fKrFoe6tsEbD7S8EmxGTJYAKtTVhAW5Q5pge4j1',
), 'base_mint': Pubkey.from_string(
    'H5UVM4S9Y5kbuVCEEyJ3NZ38CM8cxUEJrm9gNhswKSdy',
), 'base_decimals': 9, 'quote_mint': Pubkey.from_string(
    'So11111111111111111111111111111111111111112',
), 'quote_decimals': 9, 'lp_mint': Pubkey.from_string(
    'Acvzwk3Q6cmEdnVzSfdKLa5786QC44Hmy6cZq5MEZPLc',
), 'open_orders': Pubkey.from_string(
    '3pncKJCXwdbd3Hs66T6r9eExiGbSa4fhPVhxzHZNwYFu',
), 'target_orders': Pubkey.from_string(
    'HAkvMss1C4rhH4xxZrzJGQSnvj8bNUEE2Q4TrDP6Qnf9',
), 'base_vault': Pubkey.from_string(
    'CQqoRGZdH57DBiTyZPjBsycY9EQHin1gHBQFpxzMH8r3',
), 'quote_vault': Pubkey.from_string(
    '9ReFnM5HCAr3QUw78mpEASoNZV2xp34Vw9AvCPG7Z1a5',
), 'market_id': Pubkey.from_string(
    'pCi9LDihfcukVajicERXEKgD68NVSKKuP1aqGDdenBT',
), 'market_base_vault': Pubkey.from_string(
    'A4MY7iRNj3oixzVKLLvHGJyJpHqwJJKPp1Gn5HT725oX',
), 'market_quote_vault': Pubkey.from_string(
    'AveWC1Z68nwR9f4fU8BWsZQRZXfNRWuDRLCuf3Acpair',
), 'market_authority': Pubkey.from_string(
    '4Pn58WJDp6CSnTGkXbZ4YCKQkLYYC5PTvAMg8xFWXuTK',
), 'bids': Pubkey.from_string(
    'BqZNSUrtfwwuzPyd4mRoLXdQCdpLohgJSZgGKdBFDWGH',
), 'asks': Pubkey.from_string(
    '6ersikwb7Srqq6fkbx36nmbBruPZXpBmxUYG6jBSyMdc',
), 'event_queue': Pubkey.from_string(
    '7CnWTUyDstVfeyWZHonGUvhGmCjhhH4iLEJSTHwV3BQv',
)}

poolkeysBoyoyo = {'amm_id': Pubkey.from_string(
    '6woyrArPvmteXbRMrNwL1hKALZVrvhuQDzPHqmc1xY4Y',
), 'authority': Pubkey.from_string(
    '5Q544fKrFoe6tsEbD7S8EmxGTJYAKtTVhAW5Q5pge4j1',
), 'base_mint': Pubkey.from_string(
    '9V2ns9yRUtn41GmuxZHESA6qVnfwcDrroDCVy2Kpu9E5',
), 'base_decimals': 9, 'quote_mint': Pubkey.from_string(
    'So11111111111111111111111111111111111111112',
), 'quote_decimals': 9, 'lp_mint': Pubkey.from_string(
    '7xmBgrNc3YpU54arsD1oNTQV3CrrSRK2fTrgfYbK4pDv',
), 'open_orders': Pubkey.from_string(
    '6BRtwM4aBw2pKTpXcUc21LyvRdy7UpXKpFYccHCub4j5',
), 'target_orders': Pubkey.from_string(
    'DFkFv57hVdnJd9vTj7i8ZDcM4HCk2ow9UrKTgHtu3FQQ',
), 'base_vault': Pubkey.from_string(
    '581fpdP6ZTVA4J6VrqX2KTfDYxnffzXgxq5CXmntsXFf',
), 'quote_vault': Pubkey.from_string(
    '9CYYe3Km613YLz5jdoKAmhqN7bSfTKT1LKm6h1RXLsHH',
), 'market_id': Pubkey.from_string(
    'GVNTrsVSrtWs6ZP15XFk3F6xZjfAYCDVDp6fBPD1cvYb',
), 'market_base_vault': Pubkey.from_string(
    '6TQVAqC256WsrztQkd3yStnBMFaQH3CJoQUbzXD8vTma',
), 'market_quote_vault': Pubkey.from_string(
    'AX3wyjQxgDhsvfrLrU7xukTNDoqY314HAw92hjB9eo4J',
), 'market_authority': Pubkey.from_string(
    'MESVKcxoPe5TSLWCTheKJ9nQynCNrAhYeCQDkGybrLQ',
), 'bids': Pubkey.from_string(
    'sdoXkRBhrB2vVDaCAScridXM6q634UhSTjrJ4Qr2C6f',
), 'asks': Pubkey.from_string(
    '4C4BcvQeDkkurkmku2L4pvj772Hwj1QGPBLCK9PdqCgZ',
), 'event_queue': Pubkey.from_string(
    'AcC2PwwHcCKzX1uDjdbDKipfR19oJZgBsd1DpFwJbuep',
)}

def buy_token(TOKEN_TO_SWAP_BUY, seed, amount):
    secret=base58.b58decode(seed)
    secret_key = secret[:32]
    payer = Keypair.from_seed(secret_key)
    mint = Pubkey.from_string(TOKEN_TO_SWAP_BUY)

    '''print(payer.pubkey())
    pool_keys = fetch_pool_keys(str(mint))
    print(pool_keys)
    if pool_keys == "failed":
        return "failed"'''
    
    """
    Calculate amount
    """
    amount_in = int(amount * LAMPORTS_PER_SOL)

    
    """Get swap token program id"""
    accountProgramId = solana_client.get_account_info_json_parsed(mint)
    TOKEN_PROGRAM_ID = accountProgramId.value.owner

    """
    Set Mint Token accounts addresses
    """
    swap_associated_token_address,swap_token_account_Instructions  = get_token_account(solana_client, payer.pubkey(), mint)


    """
    Create Wrap Sol Instructions
    """
    balance_needed = Token.get_min_balance_rent_for_exempt_for_account(solana_client)
    WSOL_token_account, swap_tx, payer, Wsol_account_keyPair, opts, = _TokenCore._create_wrapped_native_account_args(TOKEN_PROGRAM_ID, payer.pubkey(), payer,amount_in,
                                                        False, balance_needed, Commitment("confirmed"))
    """
    Create Swap Instructions
    """
    instructions_swap = make_swap_instruction(  amount_in, 
                                                WSOL_token_account,
                                                swap_associated_token_address,
                                                poolkeysBoyoyo,
                                                mint, 
                                                solana_client,
                                                payer
                                            )

    params = CloseAccountParams(account=WSOL_token_account, dest=payer.pubkey(), owner=payer.pubkey(), program_id=TOKEN_PROGRAM_ID)
    closeAcc = (close_account(params))

    if swap_token_account_Instructions != None:
        swap_tx.add(swap_token_account_Instructions)
    swap_tx.add(instructions_swap)
    swap_tx.add(closeAcc)

    try:
        txn = solana_client.send_transaction(swap_tx, payer, Wsol_account_keyPair)
        txid_string_sig = txn.value
        return txid_string_sig
    except RPCException as e:
        print(f"Error: [{e.args[0].message}]....")

def decode_signature(signature):
    try:
        txSignature = to_signature_string(signature)
        tx = solana_client.get_transaction(txSignature, max_supported_transaction_version=0)
        tx = json.loads(tx.to_json())
        outcome = tx['result']
        if outcome == None:
            return 0
        else:
            return 1
    except Exception as x:
        print("decode_signature:", x)
        import traceback
        traceback.print_exc()
        return 0

if __name__ == '__main__':
    pass
