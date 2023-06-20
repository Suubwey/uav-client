import asyncio
import websockets
import flight
import json
import requests
import logger
log = logger.get_logger(__name__)
async def send_location(websocket):
    while True:
        # Send location data to the server
        if flight.home and flight.home.lat:
            
            await websocket.send(json.dumps({"type":"position","data":{"lat":flight.home.lat,
                                             "lon":flight.home.lon,
                                             "alt":flight.home.alt}}))
        await asyncio.sleep(1)  # sleep for 1 second

async def receive_messages(websocket):
    while True:
        # Wait for incoming message from the server
        response = await websocket.recv()
        response = json.loads(response)
        log.info(f"Received: {response}")
        flight.mission(response)

async def connect_websocket():
    uri = "ws://3.139.94.118:3000"  # Replace with your WebSocket server URL

    async with websockets.connect(uri) as websocket:
        log.info("Connected to WebSocket server")

        sender = asyncio.create_task(send_location(websocket))
        receiver = asyncio.create_task(receive_messages(websocket))
        
        done, pending = await asyncio.wait(
            [sender, receiver],
            return_when=asyncio.FIRST_COMPLETED,
        )

        for task in pending:
            task.cancel()

async def check_internet_connection(url='http://www.google.com', timeout=5):
    while True:
        try:
            response = requests.get(url, timeout=timeout)
            # If the request is successful, the status code will be 200
            if response.status_code == 200:
                log.info('Internet connection established.')
                return True
        except requests.RequestException:
            log.info('No internet connection. Retrying in 5 seconds...')
            await asyncio.sleep(5)

async def main():
    await check_internet_connection()
    await connect_websocket()

asyncio.run(main())

