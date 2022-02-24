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

print("Start Websockets work!")

json_command = json.dumps(Json_Data)
json_call = json.dumps(Json_CallFunc)
print("Data prepared : " + json_command)

from websocket import create_connection
ws = create_connection(Server)
print("Sending Command to Server")
ws.send(json_call)
print("Sent")
print("Receiving...")
result =  ws.recv()
print("Received from Server '%s'" % result)
ws.close()