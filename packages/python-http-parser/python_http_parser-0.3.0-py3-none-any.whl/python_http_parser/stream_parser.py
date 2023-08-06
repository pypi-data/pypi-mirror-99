"""Stream based HTTP parser.

If needed, could be reused.
"""

__all__ = [
    'StreamParser'
]

try:
    # typing module is not required.
    from typing import BinaryIO, Dict, List, Union
except ImportError:
    pass

import re

import python_http_parser.constants as constants
import python_http_parser.utils as utils
from python_http_parser.errors import FatalParsingError


class StreamParser:
    """StreamParser class.

    Parses a HTTP message from a byte stream. Could be
    reused with a different stream.
    """

    def __init__(self, stream=None, strictness_level=constants.PARSER_NORMAL, auto_parse=False, max_header_size=constants.DEFAULT_MAX_HEADER_SIZE):
        """Construct a StreamParser.

        Arguments:\n
        ``stream`` -- Must be a text IO stream instance, or none. If None, then you must manually
        assign this StreamParser a readable text-based stream and tell it to start parsing.\n
        ``strictness_level`` -- How strict to be while parsing. Default is ``constants.PARSER_NORMAL``.\n
        ``auto_parser`` -- Whether to start parsing right after a stream is received. Default is false.\n
        ``max_header_size`` -- The maximum allowed size for a header.
        """
        self.strictness = strictness_level  # type: int
        self.auto_parse = auto_parse  # type: bool
        self.max_header_size = max_header_size  # type: int

        # Whether we are parsing a HTTP response.
        self.msg_is_response = False

        self.parsed_msg = {}  # type: Dict[str, Union[str, int, dict, list]]
        self.newline = None  # type: str

        if stream is not None:
            self.set_stream(stream)

    def set_stream(self, stream):
        """Set the stream this parser is going to parse."""
        if not stream.readable():
            raise TypeError('Stream is not readable!')

        self.stream = stream  # type: BinaryIO
        self.finished = False

        # Start parsing right away if auto_parse is True.
        if self.auto_parse and not self.finished:
            self.parse()

    def parse(self):
        stream = self.stream
        first_eight_chars = stream.read(8).decode('utf-8')

        http_ver = None  # type: float
        http_status = None  # type: int
        http_status_msg = ''  # type: str
        http_method = None  # type: str
        http_uri = None  # type: str

        # Container for storing leftover strings from parsing.
        leftovers = None  # type: str
        hdrs = {}
        raw_hdrs = {}

        if re.fullmatch(constants.HTTP_VER_REGEX, first_eight_chars):
            # First four characters is ``HTTP``. We received a response message.
            self.msg_is_response = True
            try:
                http_ver = utils.parse_http_version(first_eight_chars)
                http_status = utils.parse_http_status(
                    stream.read(4).decode('utf-8')
                )
                # Now, to parse the HTTP status message.
                while True:
                    # Keep reading 16 byte chunks until we find a newline.
                    http_status_msg += stream.read(16).decode('utf-8')
                    newline_index = http_status_msg.find('\n')
                    if bool(~newline_index):
                        # If there is a CR before the LF, assume the linebreaks are CRLF.
                        if http_status_msg[newline_index - 1] == '\r':
                            self.newline = '\r\n'
                            newline_index -= 1
                        else:
                            self.newline = '\n'

                        # Assume the stuff before the linebreak is the HTTP status message,
                        # and the stuff after the linebreak are headers.
                        leftovers = http_status_msg[newline_index +
                                                    len(self.newline):]
                        http_status_msg = http_status_msg[:newline_index]
                        break

            except Exception as ex:
                raise FatalParsingError(
                    'Failed to parse response line with error {}'.format(str(ex))
                )

        try:
            req = []  # type: List[str]
            if leftovers is not None:
                req.append(leftovers)
            
            while True:
                # Keep reading 512 byte chunks until we reach a double newline.
                chunk = stream.read(512).decode('utf-8')

                double_newline_index = chunk.find(self.newline + self.newline)

                if bool(~double_newline_index):
                    pass
        except Exception:
            pass

        return {
            'http_ver': http_ver,
            'status_code': http_status,
            'status_msg': http_status_msg,
            'req_method': http_method,
            'req_uri': http_uri
        }
