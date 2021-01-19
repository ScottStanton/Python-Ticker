# Python-Ticker
This is a small program to get stock values from Yahoo and display them on the command line.

This program is a way for me to learn two new items.
1. Python
1. Git

I guess I'm also learning markdown by writing this readme file.

If you like this idea and you want to take it and make it better, feel free to fork the process.  I have some ideas on what I want to do here, but I don't know when it will get done as this is about 5th in the line of priorities and hobbies.

## Ideas:
* Integrate pushbullet to send updates 

Thanks for looking, I hope you enjoying learning through this as much as I have.

## Usage:
usage: ticker.py [-h]|[--help]<br>
       -s|--stock [stock_symbol [stock_symbol ...]]<br>
       [-l|--list]<br>
       [-p|--params [known_parameters [known_parameters ...]]]<br>
       [-b|--boundary BOUNDARY BOUNDARY]<br>
<br>
-s  --stock:     Takes one or more stock symbols to lookup<br>
-l  --list:      Prints a list of parameters that can be used with -p<br>
-p  --params:    Takes a list of paramaters and returns the values for those parameters<br>
-b  --boundary:  Takes two values and returns "low" if the current value of the stock is lower than the lowest range<br>
                 or it returns "within" if the current value of the stock is within the two values<br>
                 or it retuns "high" if the current value of the stock is higher than the higest value<br>
