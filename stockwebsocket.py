import websocket,json,random,time

socket = websocket.WebSocket()

socket.connect("ws://localhost:8000/ws/user/1/")

for _ in range(1):
    time.sleep(1)
    socket.send(json.dumps({
        'message':{'type':'sub', 'stocks':['RELIANCE']}
    }))