""" test_branflake.py
"""
from time import sleep, struct_time
from uuid import UUID
import pytest
from branflake import Branflake

# easier to read than a pile of zeros
ONE_MILLION = 1000000

# define low, one, and high bytearrays
LOW_BYTEARRAY = b'\x00\x00\x00\x00\x00\x00\x00\x00'
ONE_BYTEARRAY = b'\x00\x00\x00\x00\x00\x00\x00\x01'
HIGH_BYTEARRAY = b'\xff\xff\xff\xff\xff\xff\xff\xff'

# define lowest and highest integers
ONE_INT64 = int.from_bytes(ONE_BYTEARRAY, 'big', signed=False)
HIGH_INT64 = int.from_bytes(HIGH_BYTEARRAY, 'big', signed=False)
ZERO_INT128 = int.from_bytes(LOW_BYTEARRAY + LOW_BYTEARRAY, 'big', signed=False)
LOW_INT128 = int.from_bytes(ONE_BYTEARRAY + LOW_BYTEARRAY, 'big', signed=False)
HIGH_INT128 = int.from_bytes(HIGH_BYTEARRAY + HIGH_BYTEARRAY, 'big', signed=False)

# create earliest and latest possible branflakes
EARLIEST_BRANFLAKE = Branflake(ONE_INT64, LOW_BYTEARRAY)
LATEST_BRANFLAKE = Branflake(HIGH_INT64, HIGH_BYTEARRAY)

# create two branflakes at least 5 microseconds apart
FIRST_BRANFLAKE = Branflake()
sleep(5 / ONE_MILLION)
SECOND_BRANFLAKE = Branflake()

def test_earliest():
    """ Checks the integrity of the earliest branflake
    """
    assert EARLIEST_BRANFLAKE
    assert EARLIEST_BRANFLAKE.to_bytes() == (ONE_BYTEARRAY + LOW_BYTEARRAY)

def test_latest():
    """ Checks the integrity of the latest branflake
    """
    assert LATEST_BRANFLAKE
    assert LATEST_BRANFLAKE.to_bytes() == (HIGH_BYTEARRAY + HIGH_BYTEARRAY)

def test_first():
    """ Tests first branflake for types and lengths
    """
    assert FIRST_BRANFLAKE
    assert len(FIRST_BRANFLAKE.get_random_bytes()) == 8
    assert len(FIRST_BRANFLAKE.get_time_bytes()) == 8
    assert len(FIRST_BRANFLAKE.to_bytes()) == 16
    assert len(FIRST_BRANFLAKE.to_hex_bytes()) == 32
    assert len(FIRST_BRANFLAKE.to_hex_string()) == 32
    assert isinstance(FIRST_BRANFLAKE.to_gmtime(), struct_time)
    assert isinstance(FIRST_BRANFLAKE.to_uuid(), UUID)
    assert isinstance(FIRST_BRANFLAKE.to_microseconds(), int)
    assert isinstance(FIRST_BRANFLAKE.to_seconds(), float)

def test_compare():
    """ Compares second and first branflakes with inequality operator.
    """
    assert SECOND_BRANFLAKE
    assert SECOND_BRANFLAKE.to_int() > FIRST_BRANFLAKE.to_int()
    assert SECOND_BRANFLAKE.to_hex_string() > FIRST_BRANFLAKE.to_hex_string()

def test_reconstitute():
    """ Reconsitutes branflakes using 'from' methods.
    """
    assert ((Branflake.from_int(FIRST_BRANFLAKE.to_int())).to_int()
            == FIRST_BRANFLAKE.to_int())
    assert ((Branflake.from_hex_string(FIRST_BRANFLAKE.to_hex_string())).to_int()
            == FIRST_BRANFLAKE.to_int())
    assert ((Branflake.from_bytes(FIRST_BRANFLAKE.to_bytes())).to_int()
            == FIRST_BRANFLAKE.to_int())

def test_out_of_bounds():
    """ Tests creating branflakes with out-of-bounds times.
    """
    with pytest.raises(ValueError):
        Branflake(HIGH_INT64 + 1, HIGH_BYTEARRAY)
    with pytest.raises(ValueError):
        Branflake(-1, HIGH_BYTEARRAY)
    with pytest.raises(ValueError):
        Branflake.from_int(-1)

def test_wrong_length():
    """ Tests creating branflakes with inputs of wrong length.
    """
    with pytest.raises(ValueError):
        Branflake.from_bytes(b'\x00')
    with pytest.raises(ValueError):
        Branflake.from_hex_string('0')
