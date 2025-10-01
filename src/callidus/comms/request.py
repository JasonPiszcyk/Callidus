#!/usr/bin/env python3
'''
Request - Structure of a request to Callidus (as data in message)

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
from appcore.conversion import to_json, from_json

# Local app modules
from callidus.include.typing import RequestType

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
# Request Class Definition
#
###########################################################################
class Request():
    '''
    Class to describe Request - A request to Callidus.

    This describes the structure of request sent to Callidus

    Attributes:
        type (RequestType): The type of request
        action (str): The actin to be carried out
        data (Any): The data to be sent as part of the request
            (MUST be serialisable via JSON)
    '''

    #
    # __init__
    #
    def __init__(
            self,
            request_type: RequestType = RequestType.NONE,
            action: str = "",
            data: Any = None
    ):
        '''
        Initialises the instance.

        Args:
            request_type (RequestType): The type of request
            action (str): The actin to be carried out
            data (Any): The data to be sent as part of the request
                (MUST be serialisable via JSON)

        Returns:
            None

        Raises:
            None
        '''
        # Private Attributes

        # Attributes
        self.type = request_type
        self.action = action        
        self.data = data        


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
        _msg_dict = {
            "type": self.type,
            "action": self.action,
            "data": self.data
        }

        # If it can't be converted just return an empty string
        try:
            _value_json = to_json(data=_msg_dict, skip_invalid=True)
        except:
            _value_json = ""

        return _value_json.encode(ENCODE_METHOD)


    @packet.setter
    def packet(self, value: bytes = b"") -> None:
        ''' Import a received message into the response class '''
        # Convert the message
        if not isinstance(value, bytes):
            return

        _msg_dict = {}
        try:
            _value_json = value.decode(ENCODE_METHOD)
            if _value_json:
                _msg_dict = from_json(data=_value_json)
        except:
            pass

        try:
            self.type = RequestType(
                _msg_dict.get('type', RequestType.NONE.value)
            )
        except:
            RequestType.NONE

        self.action = _msg_dict.get('action', None)
        self.data = _msg_dict.get('data', None)


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
