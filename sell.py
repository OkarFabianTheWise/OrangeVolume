from spl.token.instructions import close_account, CloseAccountParams

from solana.rpc.types import TokenAccountOpts
from solana.rpc.api import RPCException
from solana.transaction import Transaction
from solana.rpc.api import Client
from solders.pubkey import Pubkey
from solders.keypair import Keypair
from create_close_account import sell_get_token_account,get_token_account, make_swap_instruction

endpoint = "https://api.mainnet-beta.solana.com"

solana_client = Client(endpoint)
print(solana_client.is_connected())

import time, base58

# poolkeys: used for swapping on raydium
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

LAMPORTS_PER_SOL = 1000000000

# ctx ,     TOKEN_TO_SWAP_SELL,  keypair
def sell_token(TOKEN_TO_SWAP_SELL, amount_to_sell, seed):
    try:
        secret=base58.b58decode(seed)
        secret_key = secret[:32]
        payer = Keypair.from_seed(secret_key)
        mint = Pubkey.from_string(TOKEN_TO_SWAP_SELL)
        sol = Pubkey.from_string("So11111111111111111111111111111111111111112")
        
        
        """Get swap token program id"""
        TOKEN_PROGRAM_ID = solana_client.get_account_info_json_parsed(mint).value.owner
        
        """Get token accounts"""
        #("4. Get token accounts for swap...")
        swap_token_account = sell_get_token_account(solana_client, payer.pubkey(), mint)
        WSOL_token_account, WSOL_token_account_Instructions = get_token_account(solana_client,payer.pubkey(), sol)
        
        if swap_token_account == None:
            return "failed"

        else:
            """Make swap instructions"""
            instructions_swap = make_swap_instruction(  amount_to_sell, 
                                                        swap_token_account,
                                                        WSOL_token_account,
                                                        poolkeysBoyoyo, 
                                                        mint, 
                                                        solana_client,
                                                        payer
                                                    )

            """Close wsol account"""
            params = CloseAccountParams(account=WSOL_token_account, dest=payer.pubkey(), owner=payer.pubkey(), program_id=TOKEN_PROGRAM_ID)
            closeAcc =(close_account(params))

            """Create transaction and add instructions"""

            swap_tx = Transaction()
            signers = [payer]
            if WSOL_token_account_Instructions != None:
                swap_tx.add(WSOL_token_account_Instructions)
            swap_tx.add(instructions_swap)
            swap_tx.add(closeAcc)

            """Send transaction"""
            try:
                txn = solana_client.send_transaction(swap_tx, *signers)

                """Confirm it has been sent"""
                txid_string_sig = txn.value
                
                return txid_string_sig
            except RPCException as e:
                print(f"Error: [{e.args[0].message}]...\nRetrying...")
                
    except Exception as e:
        print(f"Main sell Error: {e}...")


if __name__ == '__main__':
    pass
