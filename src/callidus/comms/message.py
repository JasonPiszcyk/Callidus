#!/usr/bin/env python3
'''
Message - Structure of a message sent to or received from Callidus

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
from appcore.conversion import ENCODE_METHOD, DataType
from appcore.conversion import to_json, from_json, get_value_type
from appcore.util.functions import timestamp as create_timestamp

# Local app modules

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
# CallidusMessage Class Definition
#
###########################################################################
class CallidusMessage():
    '''
    Class to describe CallidusMessage - A Callidus message.

    This describes the structure of messages passed to/from Callidus

    Attributes:
        data (Any): The data to be contained in the message
        sender (str); The message sender
        receiver (str); The message receiver
        message_type (str): Message Type (From imported message)
            This is preserved in packet
        timestamp (int): Timestamp of when the message was created
            This is preserved in packet
        ttl (int): Number of seconds for the message to be valid (0 = always)
            This is preserved in packet
        message_id (str) [ReadOnly]: Message ID (From imported message)
            This is not preserved in packet
        session_id (str): Session ID (From imported message)
            This is preserved in packet
        data_bytes (bytes): The data converted to JSON and encoded in byte
            format when possible (if not JSON compatible will be empty)
        packet (bytes): A byte encode JSON string suitable for sending over
            a messaging system. If set, will attemp to set isntance values
            from the packet
    '''

    #
    # __init__
    #
    def __init__(
            self,
            data: Any = None,
            sender: str = "",
            receiver: str = "",
            session_id: str = "",
            timestamp: int = 0,
            ttl: int = 0,
    ):
        '''
        Initialises the instance.

        Args:
            data (Any): The data to be contained in the message
            sender (str); The message sender
            receiver (str); The message receiver
            session_id (str): Session ID (From imported message)
                This is preserved in packet
            timestamp (int): Timetamp of when the message was created
            ttl (int): Number of seconds for the message to be valid
                (0 = always)

        Returns:
            None

        Raises:
            None
        '''
        # Private Attributes
        self.__message_id = ""

        # Attributes
        self.data = data
        self.sender = sender
        self.receiver = receiver
        self.session_id = session_id
        self.message_type = ""
        self.timestamp = timestamp or create_timestamp()
        self.ttl = ttl


    ###########################################################################
    #
    # Properties
    #
    ###########################################################################
    #
    # message_id
    #
    @property
    def message_id(self) -> str:
        ''' The session ID '''
        return self.__message_id


    #
    # data_bytes
    #
    @property
    def data_bytes(self) -> bytes:
        ''' Attempt to provide the data in a byte format (JSON Encoded) '''
        # Determine the data format and attempt to convert it
        if isinstance(self.data, bytes):
            return self.data

        else:
            try:
                _value_type = get_value_type(data=self.data, json_only=True)
            
            except TypeError:
                _value_type = DataType.NONE

            if _value_type == DataType.NONE:
                return b""
            else:
                _value_json = to_json(data=self.data, skip_invalid=True)
                return _value_json.encode(ENCODE_METHOD)


    @data_bytes.setter
    def data_bytes(self, value: bytes = b"") -> None:
        ''' Take the data in byte format, and convert it from JSON  '''
        if not isinstance(value, bytes):
            return

        _data_json = value.decode(ENCODE_METHOD)
        if _data_json:
            self.data = from_json(data=_data_json)
        else:
            self.data = None


    #
    # packet
    #
    @property
    def packet(self) -> bytes:
        ''' A messaage packet suitable to be sent '''
        # message_id is intentionally omitted so a new ID can be created
        _msg_dict = {
            "data": self.data,
            "properties": {
                "sender": self.sender,
                "receiver": self.receiver,
                "message_type": self.message_type,
                "session_id": self.session_id,
                "timestamp": self.timestamp,
                "ttl": self.ttl,
            }
        }

        _value_json = to_json(data=_msg_dict, skip_invalid=True)
        return _value_json.encode(ENCODE_METHOD)


    @packet.setter
    def packet(self, value: bytes = b"") -> None:
        ''' Import a received message into the Callidus message class '''
        # Convert the message
        if not isinstance(value, bytes):
            return

        _value_json = value.decode(ENCODE_METHOD)
        if _value_json:
            _msg_dict = from_json(data=_value_json)
        else:
            _msg_dict = {}

        if "data" in _msg_dict: self.data = _msg_dict["data"]

        if "properties" in _msg_dict and \
                    isinstance(_msg_dict["properties"], dict):
            _props = _msg_dict["properties"]
        else:
            _props = {}
        
        if "sender" in _props: self.sender = _props['sender']
        if "receiver" in _props: self.receiver = _props['receiver']
        if "message_type" in _props: self.message_type = _props['message_type']
        if "message_id" in _props: self.__message_id = _props['message_id']
        if "session_id" in _props: self.session_id = _props['session_id']
        if "timestamp" in _props: self.timestamp = _props['timestamp']
        if "ttl" in _props: self.ttl = _props['ttl']


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
