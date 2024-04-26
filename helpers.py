import requests, aiohttp, asyncio

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
        

async def get_user_balance(wallet, token_address):
    try:
        url = f"https://public-api.birdeye.so/v1/wallet/token_balance?wallet={wallet}&token_address={token_address}"

        access = {
            "x-chain": "solana",
            "X-API-KEY": "5438498eb1e64d51a836e9458b2f442e"
        }
        
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=access) as response:
                if response.status == 200:
                    response_object = await response.json()
                    #print(response)
                    if not response_object['data']:
                        return 0
                    elif response_object['data']:
                        return response_object['data']['balance']
                else:
                    return 0
    except Exception as d:
        print("get_price:", d)
        return 0
