import websocket
import argparse

from gateway.handler import Handler


class DiscGate:
    """
    A class for establishing a WebSocket client connection to a gateway.

    Attributes:
        None

    Methods:
        client(gateway, token="", op_codes=None): Start the WebSocket client.
    """

    @staticmethod
    def client(gateway, token="", op_codes=None):
        """
        Start the WebSocket client connection to the specified gateway.

        Args:
            gateway (str): The URL of the WebSocket gateway.
            token (str, optional): The authentication token. Defaults to an empty string.
            op_codes (list of int, optional): List of operation codes. Defaults to None.

        Returns:
            None
        """
        if op_codes is None:
            op_codes = []

        websocket.enableTrace(False)

        ws = websocket.WebSocketApp(
            gateway,
            on_message=Handler.on_message,
            on_error=Handler.on_error,
            on_close=Handler.on_close
        )

        ws.on_open = lambda ws: Handler.on_open(ws, token, op_codes)
        ws.run_forever()
