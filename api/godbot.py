import requests
import json
import time
from datetime import datetime
import urllib.request
import os
import tweepy
import requests
import time
import urllib3

while True:
        try:
            bearer_token = 'AAAAAAAAAAAAAAAAAAAAAHJ9lgEAAAAAfvWw3CS2%2B4KhrvR%2B6R9WGgMQsYk%3DPTb0MN4lu9hGUEGlU8chMzsYr4PLSkJMjVbTxWkZNu0sS1J3OO'
            consumer_key = 'E6IeiMOy2AHPwLCgWAsI3yJpS'
            consumer_secret = 'iMh3vhqqFqJzWoURjeyJJxhZqBRnZLNvUGwgCmXHND244hq7T6'
            access_token = '1616490268248637446-m2e0yi32VX5PXGsaPx0nwAxcBorPJZ'
            access_token_secret = 'fQCeY8lCYBOZM9N5V2UNvhHvqaoe3suGPoWXaJv371jke'

            auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
            auth.set_access_token(access_token, access_token_secret)

            api = tweepy.API(auth)
            api_url = "https://api-mainnet.magiceden.dev/v2/collections/solgods/activities?type=buyNow&sort=asc&offset=0&limit=1"
            response = requests.get(api_url)

            activity_list = response.json()

            for activity in activity_list:
                if activity.get("type") == "buyNow":
                    most_recent_buyNow = activity
                    break

            filterActivity = {k: most_recent_buyNow[k] for k in ('type', 'tokenMint', 'collection', 'blockTime', 'image', 'price', 'buyer', 'seller', 'signature')}

            type_var = filterActivity['type']
            token_mint_var = filterActivity['tokenMint']
            collection_var = filterActivity['collection']
            block_time_var = filterActivity['blockTime']
            image_var = filterActivity['image']
            price_var = filterActivity['price']
            buyer_var = filterActivity['buyer']
            seller_var = filterActivity['seller']
            signature_var = filterActivity['signature']

            api_url2 = "https://api-mainnet.magiceden.dev/v2/tokens/"+token_mint_var

            response2 = requests.get(api_url2).json()

            token_id = (response2.get("name", {}))

            image_url = filterActivity['image']

            urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

            filename = 'temp_image.jpg'
            response = requests.get(image_url, verify=False)
            with open(filename, 'wb') as f:
                f.write(response.content)

            media = api.media_upload(filename)
            media_id = media.media_id

            tweet_text = " " +collection_var.replace("_", " ") +" "+str(price_var)

            os.remove(filename)

            api_url = "https://api.coingecko.com/api/v3/simple/price"

            params = {
                "ids": "ethereum,usd,solana",
                "vs_currencies": "usd"
            }

            response = requests.get(api_url, params=params)
            prices = response.json()

            eth_price = prices["ethereum"]["usd"]
            sol_price = prices["solana"]["usd"]
            usd_price = prices["usd"]["usd"]

            sol_sale_price = round(sol_price * price_var, 2)
            usd_sale_price = round(price_var / usd_price,2)
            eth_sale_price = round(sol_sale_price / eth_price, 5)

            token_url = "🛒 MagicEden v2 👉 https://magiceden.io/item-details/" + str(token_mint_var)
            buyer_url = "🧾 Buyer: https://magiceden.io/u/" + str(buyer_var)
            seller_url = "🧾 Seller: https://magiceden.io/u/" + str(seller_var)
            signature_url = "🧾 Tx: https://solscan.io/tx/" + str(signature_var)

            tweet_text = "In hindsight...  \n\n" +str(token_id)+" SOLD \n@TheFracture_ \n\n💵 " +str(price_var) + f" SOL ($"+str(sol_sale_price)+" USD) "+"\n💵 "+str(eth_sale_price)+" ETH\n"+ token_url +"\n\n"+ buyer_url + "\n" + seller_url + "\n" + signature_url

            last_tweet = api.user_timeline(count=1)[0]

            if token_id in last_tweet.text:
                print("Last tweet contained signature URL")
            else:
                api.update_status(status=tweet_text, media_ids=[media_id])
                print("Last tweet did not contain signature URL")

            time.sleep(10)

        except Exception as e:
            print(f"An error occurred: {e}")
