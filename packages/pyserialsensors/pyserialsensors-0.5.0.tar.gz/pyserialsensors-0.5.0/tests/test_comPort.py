# SPDX-FileCopyrightText: 2021 German Aerospace Center (DLR)
#
# SPDX-License-Identifier: MIT

import unittest
from ..core import comPortController


class TestComPort(unittest.TestCase):

    def test_scanner(self):
        """ Run test if atleast SPS30 is connected """
        ports = comPortController.search_comports()
        self.assertTrue(type(ports) == list)

