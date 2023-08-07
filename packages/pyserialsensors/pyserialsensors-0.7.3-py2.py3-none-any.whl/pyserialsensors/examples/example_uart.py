# SPDX-FileCopyrightText: 2021 German Aerospace Center (DLR)
#
# SPDX-License-Identifier: MIT

"""
Example script for running a measurement using i2c senors only.
"""

__author__ = "Konstantin Niehaus"
__copyright__ = "German Aerospace Center"
__credits__ = ["Konstantin Niehaus"]
__license__ = "MIT"
__version__ = "1.0.0"
__email__ = "konstantin.niehaus [at] .dlr.de"

import argparse
import time
import logging
from threading import Thread
from pySerialMeasurement.core.toolbox import scan_uart
from pySerialMeasurement.core.comPortController import  search_comports
#logging.basicConfig(level=logging.DEBUG)

if __name__ == "__main__":
    ports = search_comports()
    devices = []
    for port in ports:
        device = scan_uart(port)
        if device is not None:
            devices.append(device)

    for device in devices:
        # setup devices
        device.start()

    # start measurement
    for device in devices:
        values = device.get_data()
        print(values)
