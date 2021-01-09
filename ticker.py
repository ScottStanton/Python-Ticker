#!/usr/bin/python3
# 
import json
import pprint
import re
import requests
import sys

# Let's setup some functions for later use

# This function will take the stock symbol and turn the data from it into a dictionary variable that
# is able to be used in the rest of the program.

def getStockData(symbol):
  global stockData
  URL='https://query1.finance.yahoo.com/v7/finance/quote?lang=en-US&region=US&corsDomain=finance.yahoo.com&symbols=' + symbol
  stockInfo=requests.get(URL)

  # Change the output to be a dictionary value from the psudeo json that we get.
  stockData=json.loads(stockInfo.text)        # Load up the json
  stockData = stockData["quoteResponse"]      # Strip off the first two sections
  stockData = stockData["result"]
  stockData = str(stockData).lstrip("[").rstrip("]")  # Make valid dictionary format
  stockData = stockData.replace("'",'"').replace("True",'"True"').replace("False",'"False"')
  stockData = json.loads(stockData)                 # Now we have a dictionary set
# End of getStockData function

def printStockData():
   if stockData.get('regularMarketChangePercent',0) < 0:
      upDown = 'down by'
   elif stockData.get('regularMarketChangePercent',0) > 0:
      upDown = 'up by'
   else:
      upDown = 'unchanged at'

   # marketState can be PRE, REGULAR, POST or POSTPOST
   if stockData.get('marketState','err') == 'PRE':
      txt = "{} closed yessterday at {:.2f} {} {:.2f}. Yesterday's range was {}."
   elif stockData.get('marketState','err') == 'REGULAR':
      txt = "{} is currently at {:.2f} {} {:.2f}. The day's range so far is {}."
   else:
      txt = "{} closed at {:.2f} {} {:.2f}. The day's range is {}."

   print(txt.format(stockData.get('symbol','err'),stockData.get('regularMarketPrice',0),upDown,stockData.get('regularMarketChangePercent',0),stockData.get('regularMarketDayRange','err')))
# End of printStockData


# Main program
# Deal with the command line options
argList=sys.argv
del argList[0]

if len(argList) == 0:
   print('You need to supply at least one stock symbol.')
   sys.exit(99)

# Run through each stock symbol listed on the command line
for stocks in argList:
   getStockData(stocks)
   # print(list(stockData.keys()))
   # print(list(stockData.values()))
   # print('State is ' + stockData.get('marketState','err')  + '  eol')
   printStockData()

#End of program
