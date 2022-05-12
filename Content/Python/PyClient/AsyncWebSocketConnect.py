#import unreal
import websockets
import asyncio
import json

from websockets import connect
Server = "ws://localhost:30020"
Json_Data =\
    {
    "MessageName": "http",
    "Parameters": {
        "Url": "/remote/object/describe",
        "Verb": "PUT",
        "Body": {
            "ObjectPath": "/Game/Remote/Test.Test:PersistentLevel.NewBlueprint_2",
        }
    }
    }
Json_CallFunc = \
    {
    "MessageName": "http",
    "Parameters": {
        "Url": "/remote/object/call",
        "Verb": "PUT",
        "Body": {
    "objectPath" : "/Game/Remote/Test.Test:PersistentLevel.NewBlueprint_2",
    "functionName":"NewFunction_0"
        }
    }
    }

async def ws_endcommand(uri,command):
    async with websockets.connect(uri) as websocket:
        await websocket.send(command)
        await asyncio.sleep(0)
        print(await websocket.recv())  # Starts receive things, not only once

print("Start Websockets work!")
json_command = json.dumps(Json_Data)
json_call = json.dumps(Json_CallFunc)
print("Data prepared : " + json_command)

asyncio.run(ws_endcommand(Server, json_call))
#asyncio.get_event_loop().run_until_complete(wsrun(Server))