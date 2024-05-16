import requests, aiohttp, asyncio

# depricated
def fetch_pools(address):
    try:
        url = "https://api.raydium.io/v2/main/pairs"
        response = requests.get(url)
        if response.status_code == 200:
            resp = response.json()
            print(resp)
        else:
            print("failed")
    except Exception as d:
        print("fetch_pools err:", d)

# dexscreener api; get token symbol
def getSymbol(token):
    # usdc and usdt
    exclude = ['EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v', 'Es9vMFrzaCERmJfrF4H2FYD4KCoNkY11McCe8BenwNYB']
    
    if token not in exclude:
        url = f"https://api.dexscreener.com/latest/dex/tokens/{token}"

        Token_Symbol = ""
        try:
            response = requests.get(url)

            # Check if the request was successful (status code 200)
            if response.status_code == 200:
                resp = response.json()
                for pair in resp['pairs']:
                    quoteToken = pair['quoteToken']['symbol']

                    if quoteToken == 'SOL':
                        Token_Symbol = pair['baseToken']['symbol']
                        Sol_symbol = quoteToken
                        return Token_Symbol


            else:
                print(f"[getSymbol] Request failed with status code {response.status_code}")

        except requests.exceptions.RequestException as e:
            print(f"[getSymbol] error occurred: {e}")
        except: 
            a = 1

        return Token_Symbol
    else:
        if token == 'EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v':
            return "USDC", "SOL"
        elif token == 'EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v':
            return "USDT", "SOL"
        
# get userbalance of a token
async def get_user_balance(wallet, token_address):
    """ ARGS:
    wallet(str): wallet address who's balance is to be queried
    token_address(str): self explanatory

    example: balance = await get_user_balance('my_wallet', 'bonk_address')
    """
    try:
        url = f"https://public-api.birdeye.so/v1/wallet/token_balance?wallet={wallet}&token_address={token_address}"

        access = {
            "x-chain": "solana",
            "X-API-KEY": "birdeye api key"
        }
        
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=access) as response:
                if response.status == 200:
                    response_object = await response.json()
                    if not response_object['data']:
                        return 0
                    elif response_object['data']:
                        return response_object['data']['balance']
                else:
                    return 0
    except Exception as d:
        print("get_price:", d)
        return 0
