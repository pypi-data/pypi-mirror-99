"""
This file has not been tested yet.

File name: aml.py
Author: Julian Krauth
Date created: 2020/06/22
Python Version: 3.7
"""
from time import sleep
import pyvisa as visa


class SMD210:
    """
    Driver for the Dual Stepper Motor Drive SMD2 from
    Arun Microelectronics LTD using a serial RS232C interface.
    Commands and settings for serial communication are found in
    the SMD210 User Manual:
    https://arunmicro.com/documentation/Manual_SMD210.pdf
    """

    DEFAULTS = {
        'write_termination': '0D',
        'read_termination': '0D',
        'encoding': 'ascii',
        'baudrate': 9600, # But internally selectable
        'timeout': 100,
        'parity': visa.constants.Parity.odd,
        'data_bits': 7,
        'stop_bits': visa.constants.StopBits.two,
        'flow_control': visa.constants.VI_ASRL_FLOW_NONE,
        'query_termination': '?',
    }

    def __init__(self, port: str, dev_number: int):
        self.port = port # e.g.: '/dev/ttyUSB0'
        self.dev_number = dev_number # e.g.: 1

        self._device = None



    def initialize(self):
        """Connect to device."""
        port = 'ASRL'+self.port+'::INSTR'
        self._device = visa.ResourceManager('@py').open_resource(
            port,
            timeout=self.DEFAULTS['timeout'],
            encoding=self.DEFAULTS['encoding'],
            parity=self.DEFAULTS['parity'],
            baud_rate=self.DEFAULTS['baudrate'],
            data_bits=self.DEFAULTS['data_bits'],
            stop_bits=self.DEFAULTS['stop_bits'],
            flow_control=self.DEFAULTS['flow_control'],
            write_termination=self.DEFAULTS['write_termination'],
            read_termination=self.DEFAULTS['read_termination'])

        # make sure connection is established before doing anything else
        sleep(0.5)

        print(f"Connected to AML Stepper Motor Drive {self.dev_number}: {self.idn}")


    def write(self, cmd: str):
        self._device.write(cmd)

    def query(self, cmd: str) -> str:
        respons = self._device.query(cmd)
        return respons

    def close(self):
        """Close connection with device."""
        if self._device is not None:
            self._device.close()
        else:
            print('AML Stepper Motor Drive device is already closed')

    @property
    def idn(self) -> str:
        """Ask for the software version number"""
        idn = self.query("D4")
        return idn

    def select_motor(self, which: int):
        """Select motor 1 or 2"""
        self.write(f'B{which}')

    def wait_move_finish(self, interval):
        """ Interval given in seconds """
        status = self.error_and_controller_status()
        while status == self.CTRL_STATUS['B']:
            status = self.error_and_controller_status()
            sleep(interval)
        print("Movement finished")

    def error_and_controller_status(self):
        """Returns controller status"""
        respons = self.query('F')
        return respons

    CTRL_STATUS = {
        'Y': 'Yes',
        'B': 'Busy',
        'E': 'Error message',
    }

    def move_rel(self, distance: int):
        """Move in full steps by given distance.
        Direction is given by the sign.
        """
        self.write(f'{distance:+d}')

    @property
    def position(self):
        pos = self.query("V1")
        return pos

    def goto(self, pos):
        """Go to specified position"""
        self.write(f'G{pos:+d}')

    def home(self, sign: str):
        self.write(f'H{sign}')

    def get_dynamic_parameters(self):
        """Get the current parameters for
        Acceleration,
        Speed,
        minimum step rate,
        hold time and torque parameters"""
        respons = self.query('V5')
        return respons

    def get_speed(self):
        speed = self.get_dynamic_parameters()
        return speed

    def set_speed(self, value: int):
        """Set slew speed per second (10-6000)"""
        self.write(f'T{value}')

    def get_acceleration(self):
        respons = self.get_dynamic_parameters()
        return respons

    def set_acceleration(self, acceleration=100, start_stop_speed=2000, slew_speed=100):
        self.write(f"X{acceleration:4d},{start_stop_speed:4d},{slew_speed:4d}")


class SMD210Dummy:
    """For testing purpose only"""

    def __init__(self, port, dev_number):
        self.dev_number = dev_number
        self.idn = '123456'
        self.position = 0
        self.port = port
        self.pos = 0
        self._device = None

    def initialize(self):
        self._device = 1
        print(f"Connected to {self.__class__.__name__} {self.dev_number}: {self.idn}")

    def write(self, cmd):
        pass

    def query(self, cmd):
        return "1"

    def goto(self, pos):
        self.pos = pos

    def close(self):
        if self._device is not None:
            pass
        else:
            print('{self.__class__.__name__} is already closed')

    def wait_move_finish(self, interval):
        sleep(interval)
        print("Movement finished")


if __name__ == "__main__":

    print("This is the AML Conroller Driver example.")
    PORT = '/dev/ttyUSB0'
    DEV_ID = 1
    dev = SMD210(PORT, DEV_ID)
    dev.initialize()
    #Do commands here
    dev.close()
