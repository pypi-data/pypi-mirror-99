# SPDX-FileCopyrightText: 2021 German Aerospace Center (DLR)
#
# SPDX-License-Identifier: MIT

# Class : ERROR
#
# DESCRIPTION : Declaration of the different
# error types and messages for the Sensirion sensors
#
# ######################################################################################################################

import time
import signal

class Error:

    def __init__(self):
        """
        declaration of error types and error messages
        """
        # List of the errors
        self.error_list = ['crc', 'read']

    def error_dict(self, obj):
        """
        Compile error dict and provide sensor specifics
        """
        out = {'object': 'ERROR',
                'FTDIserial': obj.ftdi_serial,
                'id': obj.sensor_id,
                'sensor_type': obj.__name__,
                'serialno': obj.serial_number,
                'error_type': '',
                'message': '',
                'COMport': ''
                }
        if obj._serial_mode != "COM":
                out['MUXaddress'] = str(obj.mux.address)
                out['MUXport'] = str(obj.mux_port)
        else:
                out['COMport'] = obj.port

        return out


    def crc(self, obj):
        """
        CRC error declaration
        :return: [DICT] CRC-ERROR object
        """
        val = self.error_dict(obj)
        val["error_type"] = 'CRC'
        val["message"] = '[ERROR] CRC check failed'
        return val

    def read(self, obj):
        """
        read error declaration
        :param ftdi: [STRING] serial number of the FTDI chip (USB interface)
        :param mux: [STRING] Hex address of the multiplexer
        :param mux_port: [STRING] address of the multiplexer port
        :param sensor_id: [STRING] identifier of the sensor
        :return: [DICT] read ERROR object
        """
        val = self.error_dict(obj)
        val["error_type"] = 'read'
        val["message"] = '[ERROR] reading sensor failed'
        return val

    @staticmethod
    def msg(error):
        """
        makes error message
        :param error: [DICT] error object
        :return: [STRING] error message
        """
        if error['object'] == 'ERROR':
            return error['message'] + '! [' + error['id'] + ' @' + error['FTDIserial'] + ' | ' + \
                   error['MUXaddress'] + ' | ' + error['MUXport'] + ']'

    @staticmethod
    def checksum(byte_values, crc_value, crc_init=0xFF, crc_poly=0x131):
        """
        calculates the crc8 value based on LSB is default
        :param byte_values: [BYTE ARRAY]
        :param crc_value: [HEX] crc values of the byte_values
        :param crc_init: initialise crc (0xFF means LSB)
        :param crc_poly: crc generator polynomial
        :return: [LIST] = [crc [INT], [BOOLEAN] True=check Ok, False=check failed]
        """
        crc = crc_init
        for byte in byte_values:
            crc ^= byte
            for _ in range(8):
                if crc & 0x80:
                    crc <<= 1
                    crc ^= crc_poly
                else:
                    crc <<= 1
                    crc ^= 0x00
        if crc == crc_value:
            return [crc, True]
        else:
            return [crc, False]

## Timeout Error
# Taken from https://stackoverflow.com/questions/35490555/python-timeout-decorator
class TimeoutError(Exception):
    def __init__(self, value = "Timed Out"):
        self.value = value
    def __str__(self):
        return repr(self.value)

def timeout(seconds_before_timeout):
    def decorate(f):

        def handler(signum, frame):
            raise TimeoutError()

        def new_f(*args, **kwargs):
            old = signal.signal(signal.SIGALRM, handler)
            old_time_left = signal.alarm(seconds_before_timeout)
            if 0 < old_time_left < second_before_timeout: # never lengthen existing timer
                signal.alarm(old_time_left)
            start_time = time.time()
            try:
                result = f(*args[1:], **kwargs)
            finally:
                if old_time_left > 0: # deduct f's run time from the saved timer
                    old_time_left -= time.time() - start_time
                signal.signal(signal.SIGALRM, old)
                signal.alarm(old_time_left)
            return result

        new_f.__name__ = f.__name__
        return new_f

    return decorate

