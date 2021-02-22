#!/usr/bin/python3
import sys
import requests
import os
import json
 
def pushbullet_note(atoken, title, body):
    data_send = {"type": "note", "title": title, "body": body}
 
    ACCESS_TOKEN = atoken
    resp = requests.post('https://api.pushbullet.com/v2/pushes', data=json.dumps(data_send),
                         headers={'Authorization': 'Bearer ' + ACCESS_TOKEN, 'Content-Type': 'application/json'})
    if resp.status_code != 200:
        raise Exception('Something wrong')
    else:
        print('complete sending')

argList=sys.argv

if len(argList) != 3:
   print('You need to supply a title and a body for the note.')
   sys.exit(99)

tokenpath=os.path.expanduser("~") + "/.pushbullettoken"
try:
   f = open(tokenpath, "r")
except:
   print("Your pushbullet token needs to be saved in " +tokenpath)
   sys.exit(1)

token=f.read().rstrip() 
f.close()
pushbullet_note(token, argList[1], argList[2])
