#!/usr/bin/python3
# 
# 

import argparse
import json
import os
import requests
import sys


parser = argparse.ArgumentParser()

parser.add_argument('-s','--stock','--stocks', required=True, nargs='*',
       metavar='stock_symbol', help="List of stocks to get information for.")
parser.add_argument('-a','--attributes', nargs='*', metavar='known_attributes',
       help="Optional list of attributes instead of the usual output.")
parser.add_argument('-l','--list', action='store_true', help="List the parameters available")
parser.add_argument('-p','--pushbullet', nargs='*', help="Send results via Pushbullet. Requires your token to be in ~/.pushbullettoken")
parser.add_argument('-b','--boundary', nargs=2, type=int,
       help="Use to find out if the stock has reached the lower or upper boundary.")
parser.add_argument('-q','--quiet', nargs='*', help="Give no response when using boundary and pushbullet.  Good for when running from cron.")

args = parser.parse_args()

if args.attributes and args.boundary:
    parser.error("--attributes and --boundary cannot be used together.")
if args.attributes and args.list:
    parser.error("--attributes and --list cannot be used together.")
if args.boundary and args.list:
    parser.error("--boundary and --list cannot be used together.")
if args.list and args.pushbullet:
    parser.error("--list and --pushbullet cannot be used together.")
if args.quiet and not args.pushbullet:
    parser.error("--quiet requires --pushbullet")


# Let's setup some functions for later use

#Pushbullet function
def pushbullet_note(title, body):
    data_send = {"type": "note", "title": title, "body": body}
    
    tokenpath=os.path.expanduser("~") + "/.pushbullettoken"
    try:
       f = open(tokenpath, "r")
    except:
       print("Your pushbullet token needs to be saved in " + tokenpath)
       sys.exit(1)

    atoken=f.read().rstrip()
    f.close()

    resp = requests.post('https://api.pushbullet.com/v2/pushes', data=json.dumps(data_send),
                         headers={'Authorization': 'Bearer ' + atoken, 'Content-Type': 'application/json'})
    if resp.status_code != 200:
        raise Exception('Something wrong')
    else:
        if args.quiet is None:
            print('Message sent.')


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

   if args.pushbullet is not None:
      stitle=stockData.get('symbol','err')
      sbody=txt.format(stockData.get('symbol','err'),stockData.get('regularMarketPrice',0),upDown,stockData.get('regularMarketChangePercent',0),stockData.get('regularMarketDayRange','err'))
      pushbullet_note(stitle,sbody)
   else:
      print(txt.format(stockData.get('symbol','err'),stockData.get('regularMarketPrice',0),upDown,stockData.get('regularMarketChangePercent',0),stockData.get('regularMarketDayRange','err')))
# End of printStockData


# Main program
# Deal with the command line options

# Run through each stock symbol listed on the command line
if args.list:
   getStockData(args.stock[0])
   for k in stockData.keys():
       print(k)
   sys.exit(0)

elif args.attributes:
   attrbody=""
   attrtitle=""
   for stocks in args.stock:
       attrbody += stocks + "\n"
       attrtitle += "," + stocks
       getStockData(stocks)
       for p in args.attributes:
           attrbody += p + ": " + str(stockData.get(p,'err')) + "\n"
   if args.pushbullet is not None:
       attrtitle = attrtitle.lstrip(",")
       pushbullet_note(attrtitle,attrbody)
   else:
       print(attrbody)
   sys.exit(0)

elif args.boundary:
   low = args.boundary[0]
   high = args.boundary[1]
   if low > high:
      low = args.boundary[1]
      high = args.boundary[0]
   btitle = ""
   bbody = ""
   barg=""
   for stocks in args.stock:
      btitle += "," + stocks
      bbody += stocks + ": "
      getStockData(stocks)
      if stockData.get('regularMarketPrice',0) < low:
         bbody += 'lower than ' + str(low) + '\n'
         barg += 'l'
      elif stockData.get('regularMarketPrice',0) > high:
         bbody += 'higher than ' + str(high) + '\n'
         barg += 'h'
      else:
         bbody += 'within ' + str(low) + ' and ' + str(high) + '\n' 
         barg += 'w'
   if args.pushbullet is not None:
      btitle = btitle.lstrip(",")
      if 'l' in args.pushbullet and 'l' in barg:
         pushbullet_note(btitle,bbody)
      elif 'h' in args.pushbullet and 'h' in barg:
         pushbullet_note(btitle,bbody)
      elif 'w' in args.pushbullet and 'w' in barg:
         pushbullet_note(btitle,bbody)
      elif len(args.pushbullet) == 0:
         pushbullet_note(btitle,bbody) 
   else:
      print(bbody)
   sys.exit(0)

else:
   for stocks in args.stock:
      getStockData(stocks)
      printStockData()
   sys.exit(0)

#End of program
