#!/usr/bin/env python


import asyncio
import json
import logging
import websockets
import ssl


logging.basicConfig()
USERS = set()
Clicked = set()
VALUE1 = 0
VALUE2 = 0

ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)

# Generate with Lets Encrypt, chown to current user and 400 permissions
# ssl_cert = "/etc/letsencrypt/live/xxx/fullchain.pem"
# ssl_key = "/etc/letsencrypt/live/xx/privkey.pem"

ssl_context.load_cert_chain(ssl_cert, keyfile=ssl_key)

# STATE = {"value": 0}


def users_event():
   # st=""
   # for i in USERS:
   #  st += (str(i.remote_address[0])+":"+str(i.remote_address[1]))+"\r\n"
   return json.dumps({"type": "users", "count": len(USERS)})


def value_event():
   return json.dumps({"type": "value1", "value1": VALUE1})

def value2_event():
   return json.dumps({"type": "value2", "value2": VALUE2})


async def counter(websocket):
   global USERS, VALUE1, VALUE2, Clicked
   try:
       # Register user
       USERS.add(websocket)
       st = (str(websocket.remote_address[0])+":"+str(websocket.remote_address[1]))
       websockets.broadcast(USERS, users_event())

       # Send current state to user
       await websocket.send(value_event())
       await websocket.send(value2_event())
       # Manage state changes
       if(st not in Clicked):  
           async for message in websocket:
               event = json.loads(message)
               # print(st in Clicked)
               if(st not in Clicked):           
                   if event["action"] == "minus":
                       VALUE1 += 1
                       websockets.broadcast(USERS, value_event())
                       Clicked.add(st)
                   elif event["action"] == "plus":
                       VALUE2 += 1
                       websockets.broadcast(USERS, value2_event())
                       Clicked.add(st)
                   else:
                       logging.error("unsupported event: %s", event)
   finally:
       # Unregister user
       USERS.remove(websocket)
       websockets.broadcast(USERS, users_event())


async def main():
   # async with websockets.serve(counter, "192.29.5.20", 6788,ssl=ssl_context):
   async with websockets.serve(counter, "192.29.5.20", 6788):
       await asyncio.Future()  # run forever


if __name__ == "__main__":
   asyncio.run(main())
