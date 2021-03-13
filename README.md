# Python-Ticker
This is a small program to get stock values from Yahoo and display them on the command line.

This program is a way for me to learn two new items.
1. Python
1. Git

I guess I'm also learning markdown by writing this readme file.

If you like this idea and you want to take it and make it better, feel free to fork the project.

Thanks for looking, I hope you enjoying learning through this as much as I have.

## Usage:
```
usage: ticker.py [-h]|[--help]
       -s|--stock stock_symbol [stock_symbol ...]
       [-l|--list]
       [-a|--attributes known_attributes [known_attributes ...]]
       [-b|--boundary BOUNDARY BOUNDARY]
       [-p|--pushbullet [l] [w] [h]  [-q|--quiet]]

-s --stock --stocks:  Takes one or more stock symbols to lookup.
-l --list:            Prints a list of attributes that can be used with -a.
-a --attributes:      Takes a list of attributes and returns the values for those attributes.
-b --boundary:        Takes two values and returns "lower than XX" if the current value of the stock is lower than the lowest range.
                        or it returns "within XX and YY" if the current value of the stock is within the two values.
                        or it retuns "higher than YY" if the current value of the stock is higher than the higest value.
-p --pushbullet       Sends output to Pushbullet. Requires a pushbullet token in the file ~/.pushbullettoken.
                        The l, w, or h options only work with boundaries.  They are ignored for other options
                        If 'l' is chosen then it only sends if the value is lower.  'w' for within and 'h' for higher.
                        You can combine them (i.e. -p w h) to get data sent if it is within or higher.
-q --quiet            Stops the "Message sent" message from being diplayed when pushbullet message is sent
                        This is useful when the command is used in a cron job
```
