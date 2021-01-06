#!/usr/bin/python3
# 
import json
import pprint
import re
import requests
import sys

# Let's setup some functions for later use

def getStockData(symbol):
  global stockData
  URL='https://query1.finance.yahoo.com/v7/finance/quote?lang=en-US&region=US&corsDomain=finance.yahoo.com&symbols=' + symbol
  stockInfo=requests.get(URL)

  stockData=json.loads(stockInfo.text)
  stockData = stockData["quoteResponse"]
  stockData = stockData["result"]
  stockData = str(stockData).lstrip("[")
  stockData = str(stockData).rstrip("]")
  stockData = stockData.replace("'",'"')
  stockData = stockData.replace("True",'"True"')
  stockData = stockData.replace("False",'"False"')
  stockData = json.loads(stockData)


# Deal with the command line options
argList=sys.argv
del argList[0]

if len(argList) == 0:
   print('You need to supply at least one stock symbol.')
   sys.exit(99)

for stocks in argList:
   getStockData(stocks)
   print(stockData.get('marketState','none'))

   if stockData.get('regularMarketChangePercent',0) < 0:
      upDown = 'down by'
   elif stockData.get('regularMarketChangePercent',0) > 0:
      upDown = 'up by'
   else:
      upDown = 'unchanged at'

   txt = "{} is currently at {:.2f} {} {:.2f}. The day's range is {}."
   print(txt.format(stockData.get('symbol','err'),stockData.get('regularMarketPrice',0),upDown,stockData.get('regularMarketChangePercent',0),stockData.get('regularMarketDayRange','err')))
