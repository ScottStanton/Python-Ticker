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
       help="Optional list of parameters instead of the usual output. **Not yet implemented**")
parser.add_argument('-l','--list', action='store_true', help="List the parameters available")
parser.add_argument('-b','--boundary', nargs=2, type=int,
       help="Use to find out if the stock has reached the lower or upper boundary.")

args = parser.parse_args()

if args.params and args.boundary:
    parser.error("--params and --boundary cannot be used together.")
if args.params and args.list:
    parser.error("--params and --list cannot be used together.")
if args.boundary and args.list:
    parser.error("--boundary and --list cannot be used together.")


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
if args.list:
   getStockData(stocks)
   for k in stockData.keys():
       print(k)
   sys.exit(0)

elif args.params:
   for stocks in args.stock:
       getStockData(stocks)
       for p in args.params:
           print(p + ": " + str(stockData.get(p,'err')))
   sys.exit(0)

elif args.boundary:
   low = args.boundary[0]
   high = args.boundary[1]
   if low > high:
      low = args.boundary[1]
      high = args.boundary[0]
   for stocks in args.stock:
      getStockData(stocks)
      if stockData.get('regularMarketPrice',0) < low:
         print('low')
      elif stockData.get('regularMarketPrice',0) > high:
         print('high')
      else:
         print('within') 
   sys.exit(0)

else:
   for stocks in args.stock:
      getStockData(stocks)
      printStockData()

#End of program
