import time
import datetime
from cutepy import HEX


class Variables:
    """
    A class for managing global variables used in the application.

    Attributes:
        None
    """

    global start_time, logger_time

    start_time      = time.time()
    logger_time     = datetime.datetime.now()
    logger_time     = logger_time.strftime("%H:%M:%S")


class Colors:
    """
    A class for defining color codes used for console output.

    Attributes:
        green (str): The color code for green.
        muted (str): The color code for muted.
        foreground (str): The color code for foreground.
        reset (str): The color code to reset formatting.
    """

    green           = HEX.print("4f8472")
    muted           = HEX.print("64b88c")
    foreground      = HEX.print("d1d5db")
    reset           = HEX.reset


class Logger:
    """
    A class for logging status messages to the console.

    Attributes:
        None

    Methods:
        __client_logger__(status): Log a status message to the console.
    """

    @staticmethod
    def __client_logger__(status):
        """
        Log a status message to the console.

        Args:
            status (str): The status message to be logged.

        Returns:
            None
        """
        from gateway.handler import Handler
        print(f"{Colors.muted}{logger_time}{Colors.reset} {Colors.green}__{Handler.on_message}__{Colors.reset}{Colors.foreground} {status} {Colors.reset}")
