from typing import Sequence
from datetime import datetime

from .utils import (
    parse_mdc_time, pack_mdc_time, parse_enum_bitmask, pack_bitmask)


class Field:
    def __init__(self, name=None):
        self.name = name or self.__class__.__name__.upper()

    def parse(self, data):
        return data

    def pack(self, value):
        return [value]


class Int(Field):
    parse_len = 1
    range = None

    def __init__(self, name=None, range=None):
        if range:
            self.range = range
        super().__init__(name)

    def pack(self, value):
        if self.range and value not in self.range:
            raise ValueError('Field not in range', self.name, self.range)
        return [int(value)]

    def parse(self, data):
        return int(data[0])


class Bool(Int):
    range = range(2)

    def parse(self, data):
        return bool(data)


class Enum(Field):
    parse_len = 1

    def __init__(self, enum, name=None):
        self.enum = enum
        super().__init__(name or enum.__name__)

    def parse(self, data):
        return self.enum(data[0])

    def pack(self, value):
        if isinstance(value, str):
            value = self.enum[value]
        return [self.enum(value).value]


class Str(Field):
    parse_len = None  # means parsing till end of line

    def __init__(self, name=None, len=None):
        self.parse_len = self.len = len or self.parse_len
        super().__init__(name)

    def parse(self, data):
        return data.decode('utf8').rstrip('\x00')

    def pack(self, value):
        if self.len is not None and len(value) > self.len:
            raise ValueError('Field length exceeded', self.name, self.len)
        return value.encode('utf8')


class Time(Field):
    parse_len = 3

    def parse(self, data):
        return parse_mdc_time(data[2], data[0], data[1])

    def pack(self, data):
        day_part, hour, minute, second = pack_mdc_time(data)
        return (hour, minute, day_part)


class DateTime(Field):
    name = 'datetime'

    def __init__(self, name=None, seconds=True):
        self.seconds = seconds
        self.parse_len = 8 if seconds else 7
        super().__init__(name)

    def parse(self, data):
        if self.seconds:
            time = parse_mdc_time(data[7], data[1], data[2], data[3])
            return (datetime(
                int.from_bytes(data[5:7], 'big'),  # year
                data[4], data[0],  # month, day
                time.hour, time.minute, time.second
            ),)

        time = parse_mdc_time(data[6], data[1], data[2])
        return (datetime(
            int.from_bytes(data[4:6], 'big'),  # year
            data[3], data[0],  # month, day
            time.hour, time.minute, time.second
        ),)

    def pack(self, value):
        day_part, hour, minute, second = pack_mdc_time(value.time())
        return (
            bytes([value.day, hour, minute])
            + (self.seconds and bytes([second]) or b'')
            + bytes([value.month])
            + int.to_bytes(value.year, 2, 'big') + bytes([day_part]))


class Bitmask(Enum):
    parse_len = 1

    def parse(self, data):
        return parse_enum_bitmask(self.enum, data[0])

    def pack(self, data):
        # print(data)
        if not isinstance(data, Sequence):
            raise ValueError('Bitmask values must be sequence')
        return [pack_bitmask(data)]
