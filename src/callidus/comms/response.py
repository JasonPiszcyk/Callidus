#!/usr/bin/env python3
'''
Response - Structure of a response from Callidus (as data in message)

Copyright (C) 2025 Jason Piszcyk
Email: Jason.Piszcyk@gmail.com

All rights reserved.

This software is private and may NOT be copied, distributed, reverse engineered,
decompiled, or modified without the express written permission of the copyright
holder.

The copyright holder makes no warranties, express or implied, about its 
suitability for any particular purpose.
'''
###########################################################################
#
# Imports
#
###########################################################################
from __future__ import annotations

# Shared variables, constants, etc

# System Modules
from appcore.conversion import ENCODE_METHOD
from appcore.conversion import to_json, from_json, to_base64, from_base64

# Local app modules
from callidus.include.typing import Status

# Imports for python variable type hints
from typing import Any


###########################################################################
#
# Module Specific Items
#
###########################################################################
#
# Types
#

#
# Constants
#

#
# Global Variables
#


###########################################################################
#
# Response Class Definition
#
###########################################################################
class Response():
    '''
    Class to describe Response - A response to a Callidus request message.

    This describes the structure of response passed from Callidus

    Attributes:
        status (Status): The status of the request
        result (Any): The result from the request
        task_id (str): ID of a running task
        session_id (str): Session ID (of and end to end request)
        msg (string): Additional info returned by the response
        timestamp (int): Timestamp of when the request was sent
        ttl (int): Time to live of the request
    '''

    #
    # __init__
    #
    def __init__(
            self,
            status: Status = Status.UNKNOWN,
            result: Any = None,
            task_id: str = "",
            session_id: str = "",
            timestamp: int = 0,
            ttl: int = 0,
            msg: str = ""
    ):
        '''
        Initialises the instance.

        Args:
            status (Status): The status of the request
            result (Any): The result from the request
            task_id (str): ID of a running task
            session_id (str): Session ID (of and end to end request)
            msg (string): Additional info returned by the response
            timestamp (int): Timestamp of when the request was sent
            ttl (int): Time to live of the request

        Returns:
            None

        Raises:
            None
        '''
        # Private Attributes

        # Attributes
        self.status = status
        self.result = result
        self.task_id = task_id
        self.session_id = session_id
        self.msg = msg
        self.timestamp = timestamp
        self.ttl = ttl


    ###########################################################################
    #
    # Properties
    #
    ###########################################################################
    #
    # packet
    #
    @property
    def packet(self) -> bytes:
        ''' The response packaged as a packet to be sent '''
        # message_id is intentionally omitted so a new ID can be created
        # session_id, timestamp, ttl omitted as in the properties
        _msg_dict = {
            "status": self.status,
            "result": self.result,
            "task_id": self.task_id,
            "msg": self.msg
        }

        # If it can't be converted just return an empty string
        _value_bytes = b""
        try:
            _value_json = to_json(data=_msg_dict, skip_invalid=True)
            _value_bytes = to_base64(
                data=_value_json.encode(ENCODE_METHOD)
            ).encode(ENCODE_METHOD)

        except:
            pass

        return _value_bytes


    @packet.setter
    def packet(self, value: bytes = b"") -> None:
        ''' Import a received message into the response class '''
        # Convert the message
        if not isinstance(value, bytes):
            return

        _msg_dict = {}
        try:
            _value_base64 = value.decode(ENCODE_METHOD)
            if _value_base64:
                _value_json = from_base64(
                    data=_value_base64
                ).decode(ENCODE_METHOD)
            else:
                _value_json = ""

            if _value_json:
                _msg_dict = from_json(data=_value_json)

        except:
            pass

        self.status = _msg_dict.get('status', Status.UNKNOWN)
        self.result = _msg_dict.get('result', None)
        self.task_id = _msg_dict.get('task_id', "")
        self.msg = _msg_dict.get('msg', "")


###########################################################################
#
# In case this is run directly rather than imported...
#
###########################################################################
'''
Handle case of being run directly rather than imported
'''
if __name__ == "__main__":
    pass
