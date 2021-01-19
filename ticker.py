#!/usr/bin/python3
# 
import argparse
import json
import requests
import sys

parser = argparse.ArgumentParser()

parser.add_argument('-s','--stock','--stocks', required=True, nargs='*',
       metavar='stock_symbol', help="List of stocks to get information for.")
parser.add_argument('-p','--params', nargs='*', metavar='known_parameters',
       help="Optional list of parameters instead of the usual output. **Not yet imple                                                                                        mented**")
parser.add_argument('-b','--boundary', nargs=2, type=int,
       help="Use to find out if the stock has reached the lower or upper boundary.")

args = parser.parse_args()

if args.params and args.boundary:
    parser.error("--params and --boundary cannot be used together.")



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

   # marketState can be PRE, REGULAR, POST or POSTPOST or CLOSED
   if stockData.get('marketState','err') == 'PRE':
      txt = "{} closed yessterday at {:.2f} {} {:.2f}%. Yesterday's range was {}."
   elif stockData.get('marketState','err') == 'REGULAR':
      txt = "{} is currently at {:.2f} {} {:.2f}%. The day's range so far is {}."
   else:
      txt = "{} closed at {:.2f} {} {:.2f}%. The day's range is {}."

   print(txt.format(stockData.get('symbol','err'),stockData.get('regularMarketPrice',0),upDown,stockData.get('regularMarketChangePercent',0),stockData.get('regularMarketDayRange','err')))
# End of printStockData


# Main program
# Deal with the command line options

# Run through each stock symbol listed on the command line
if args.params:
   #print params
   sys.exit(99)
elif args.boundary:
   #Do boundary stuff
   sys.exit(99)
else:
   for stocks in args.stock:
      getStockData(stocks)
      # print(list(stockData.keys()))
      # print(list(stockData.values()))
      # print('State is ' + stockData.get('marketState','err')  + '  eol')
      printStockData()

#End of program
