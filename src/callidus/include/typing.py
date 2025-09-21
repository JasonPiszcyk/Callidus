#!/usr/bin/env python3
'''
Typing - Types/Constants

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
# Shared variables, constants, etc

# System Modules
import enum

# Local app modules

# Imports for python variable type hints


###########################################################################
#
# Module Specific Items
#
###########################################################################
#
# Types
#
# Status
class Status(enum.Enum):
    OK                 = "OK"
    WARNING            = "WARNING"
    ERROR              = "ERROR"
    RUNNING            = "RUNNING"
    UNKNOWN            = "UNKNOWN"
    INVALID_SENDER     = "INVALID_SENDER"
    INVALID_RECEIVER   = "INVALID_RECEIVER"
    INVALID_ACTION     = "INVALID_ACTION"
    ITEM_NOT_FOUND     = "ITEM_NOT_FOUND"
    EXEC_ERROR         = "EXEC_ERROR"

# Requests
class RequestType(enum.Enum):
    NONE               = "NONE"
    ST2_ACTION         = "ST2_ACTION"
    VALIDATE_ACTION    = "VALIDATE_ACTION"

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
