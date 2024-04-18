from spl.token.instructions import close_account, CloseAccountParams

from solana.rpc.types import TokenAccountOpts
from solana.rpc.api import RPCException
from solana.transaction import Transaction
from solana.rpc.api import Client
from solders.pubkey import Pubkey
from solders.keypair import Keypair
from create_close_account import  fetch_pool_keys, sell_get_token_account,get_token_account, make_swap_instruction
solana_client = Client("https://solana-mainnet.core.chainstack.com/09bd70b85bb848a5f59c0e384bdcb948")

import time, base58


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

poolkeysOrange = {'amm_id': Pubkey.from_string(
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

LAMPORTS_PER_SOL = 1000000000

# ctx ,     TOKEN_TO_SWAP_SELL,  keypair
def sell_token(TOKEN_TO_SWAP_SELL, amount_to_sell, seed):
    try:
        secret=base58.b58decode(seed)
        secret_key = secret[:32]
        payer = Keypair.from_seed(secret_key)
        mint = Pubkey.from_string(TOKEN_TO_SWAP_SELL)
        sol = Pubkey.from_string("So11111111111111111111111111111111111111112")
        
        print(payer.pubkey())
        pool_keys = fetch_pool_keys(str(mint))
        print(pool_keys)
        
        if pool_keys == "failed":
            return "failed"
        
        """Get swap token program id"""
        # TOKEN_PROGRAM_ID = solana_client.get_account_info_json_parsed(mint).value.owner

        # """Get token accounts"""
        # #("4. Get token accounts for swap...")
        # swap_token_account = sell_get_token_account(solana_client, payer.pubkey(), mint)
        # WSOL_token_account, WSOL_token_account_Instructions = get_token_account(solana_client,payer.pubkey(), sol)
        
        # if swap_token_account == None:
        #     return "failed"

        # else:
        #     """Make swap instructions"""
        #     instructions_swap = make_swap_instruction(  amount_to_sell, 
        #                                                 swap_token_account,
        #                                                 WSOL_token_account,
        #                                                 poolkeysflush, 
        #                                                 mint, 
        #                                                 solana_client,
        #                                                 payer
        #                                             )

        #     """Close wsol account"""
        #     params = CloseAccountParams(account=WSOL_token_account, dest=payer.pubkey(), owner=payer.pubkey(), program_id=TOKEN_PROGRAM_ID)
        #     closeAcc =(close_account(params))

        #     """Create transaction and add instructions"""

        #     swap_tx = Transaction()
        #     signers = [payer]
        #     if WSOL_token_account_Instructions != None:
        #         swap_tx.add(WSOL_token_account_Instructions)
        #     swap_tx.add(instructions_swap)
        #     swap_tx.add(closeAcc)

        #     """Send transaction"""
        #     try:
        #         txn = solana_client.send_transaction(swap_tx, *signers)

        #         """Confirm it has been sent"""
        #         txid_string_sig = txn.value
        #         return txid_string_sig
        #     except RPCException as e:
        #         print(f"Error: [{e.args[0].message}]...\nRetrying...")
    except Exception as e:
        print(f"Main sell Error: {e}...")

res = sell_token("Av6qVigkb7USQyPXJkUvAEm4f599WTRvd75PUWBA9eNm", 1000, 'S1gdi3B1uHUuYvV9Nb9XWgoH7Nx65ggFCmxpqYW3ehi6FbtAeUrKnfwffXN6gCmiP8EVoUkk1QcW8LwFsLktFoa')
print(f"res: {res}")

