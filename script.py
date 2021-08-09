import asyncio
import websockets
import json
from datetime import datetime
from tabulate import tabulate
from decimal import Decimal

async def connect_to_Finage():
    uri = "YOUR_SOCKET_ADDRESS"
    async with websockets.connect(uri) as websocket:
        symbols = input("Enter the symbols separated by commas: ")
        query = '{"action": "subscribe", "symbols": "%s"}' % symbols

        prices = {}
        await websocket.send(query)
        print("\033c")
        while True:
            response = await websocket.recv()
            jsonData = json.loads(response)
            try:
                symbolList = []
                priceList = []
                dateList = []
                changesList = []

                price = jsonData['lp']
                symbol = jsonData['s']
                dailyChange = jsonData['cpd']
                timestamp = jsonData['t']

                for key in prices.keys():
                    symbolList.append('\033[37m' + key)
                    priceList.append(
                        '\033[32m' + prices[key][0] if price > prices[key][0] else '\033[31m' + prices[key][0])
                    dateList.append('\033[94m' + datetime.utcfromtimestamp(
                        prices[key][2]/1000.0).strftime('%Y-%m-%d %H:%M:%S.%f'))
                    changesList.append('\033[32m' + prices[key][1] + "%" if Decimal(
                        prices[key][1]) > 0 else '\033[31m' + prices[key][1] + "%")

                prices[symbol] = [price, dailyChange, timestamp]
    
                print("\033[2J\033[1;1H")
                print(tabulate({"\033[33mSymbol": symbolList, "\033[33mPrice": priceList, "\033[33mDaily Change": changesList, "\033[33mDateTime": dateList}, headers="keys", numalign="right"))

            except Exception as e:
                print(jsonData)
                continue


asyncio.get_event_loop().run_until_complete(connect_to_Finage())
asyncio.get_event_loop().run_forever()
