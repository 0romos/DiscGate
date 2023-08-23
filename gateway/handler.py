import json
import threading
import time
import websocket

from logger import callback


class Handler:
    """
    A class that handles WebSocket communication and events.

    Attributes:
        None

    Methods:
        on_error(ws, error): Handle WebSocket error event.
        on_close(ws, close_status_code, close_msg): Handle WebSocket close event.
        on_open(ws, token, op_codes): Handle WebSocket open event.
        send_heartbeat(ws, heartbeat_interval): Send periodic heartbeat messages.
        on_message(ws, message): Handle incoming WebSocket messages.
    """

    @staticmethod
    def on_error(ws, error):
        """
        Handle WebSocket error event.

        Args:
            ws (websocket.WebSocketApp): The WebSocket connection.
            error (Exception): The error that occurred.

        Returns:
            None
        """
        print(error)

    @staticmethod
    def on_close(ws, close_status_code, close_msg):
        """
        Handle WebSocket close event.

        Args:
            ws (websocket.WebSocketApp): The WebSocket connection.
            close_status_code (int): The status code of the close event.
            close_msg (str): The close message.

        Returns:
            None
        """
        callback.Logger.__client_logger__("Websocket has closed")

    @staticmethod
    def on_open(ws, token, op_codes):
        """
        Handle WebSocket open event.

        Args:
            ws (websocket.WebSocketApp): The WebSocket connection.
            token (str): The authentication token.
            op_codes (list of int): List of operation codes.

        Returns:
            None
        """
        callback.Logger.__client_logger__("Websocket has opened")
        payload = {
            "op": 2,
            "d": {
                "token": token,
                "intents": 513,
                "properties": {
                    "$os": "linux",
                    "$browser": "chrome",
                    "$client": "web",
                    "$device": "pc"
                }
            }
        }

        if op_codes:
            payload["d"]["intents"] = sum([2 ** (i - 1) for i in op_codes])

        ws.send(json.dumps(payload))

    @staticmethod
    def send_heartbeat(ws, heartbeat_interval):
        """
        Send periodic heartbeat messages over the WebSocket.

        Args:
            ws (websocket.WebSocketApp): The WebSocket connection.
            heartbeat_interval (int): Interval for sending heartbeat in milliseconds.

        Returns:
            None
        """
        while True:
            time.sleep(heartbeat_interval / 1000)
            payload = {
                "op": 1,
                "d": None
            }
            ws.send(json.dumps(payload))

    @staticmethod
    def on_message(ws, message):
        """
        Handle incoming WebSocket messages.

        Args:
            ws (websocket.WebSocketApp): The WebSocket connection.
            message (str): The incoming message.

        Returns:
            None
        """
        data = json.loads(message)
        print(json.dumps(data, indent=4))
        op = data.get("op")
        if op == 10:
            heartbeat_interval = data["d"]["heartbeat_interval"]
            threading.Thread(
                target=Handler.send_heartbeat,
                args=[
                    ws,
                    heartbeat_interval
                ]
            ).start()
