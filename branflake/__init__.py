"""module: branflake

A Branflake represents a modified Flake ID, for which the time part is
microseconds since the beginning of the epoch and the rest is purely random. The
`to_int()` result is numerically increasing, and `to_hex_string()` result is
lexically increasing. A Branflake may be reconstituted by storing the `to_int()`
result and then calling the `from_int(int)` class method.

License: MIT. See LICENSE file for more details.
"""
from base64 import b16encode, b16decode, urlsafe_b64encode, urlsafe_b64decode
from time import time, gmtime
from secrets import token_bytes
from uuid import UUID
from math import ceil

class Branflake:
    """Encapsulates 128 bits of data, 64 of which correspond to microseconds
    since the beginning of the epoch, and 64 of which are random.

    microseconds: A 64-bit `int` corresponding to the time part of the
    `Branflake`. If omitted, the current time is used.

    random_bytes: A 8-byte array corresponding to the random part of the
    `Branflake`. If omitted, it is generated at random.

    Usage: # Create flake flake = Branflake()

        # Store flake as `int`
        branflake_int = flake.to_int()

        # Reuse flake stored as `int`
        another_flake = Branflake.from_int(branflake_int)
    """

    ONE_MILLION = 1000000
    TIME_BYTES_LEN = 8
    RANDOM_BYTES_LEN = 8
    TOTAL_BYTES_LEN = TIME_BYTES_LEN + RANDOM_BYTES_LEN
    BASE64_LEN = ceil(TOTAL_BYTES_LEN * 4 / 3)
    BASE64_PADDED_LEN = ceil(TOTAL_BYTES_LEN / 6) * 8
    MICROSECONDS_MAX = (256 ** TIME_BYTES_LEN) - 1
    BRANFLAKE_INT_MAX = (256 ** TOTAL_BYTES_LEN) - 1

    def __init__(self, microseconds=None, random_bytes=None):
        if (microseconds
                and ((microseconds < 1)
                     or (microseconds > Branflake.MICROSECONDS_MAX))):
            raise ValueError('microseconds: value out of range')
        if random_bytes and (len(random_bytes) != Branflake.RANDOM_BYTES_LEN):
            raise ValueError('random_bytes: incorrect length')

        self._time = int(microseconds or (time() * Branflake.ONE_MILLION))
        self._random_bytes = random_bytes or token_bytes(Branflake.RANDOM_BYTES_LEN)
        self._set_time_bytes()

    def __str__(self):
        return str(self.to_int())

    def __repr__(self):
        return '<Branflake %r>' % self.to_int()

    @classmethod
    def from_int(cls, branflake_int):
        """Returns a new `Branflake` corresponding to a 128-bit `int`.

        Args:
            branflake_int: A 128-bit `int` returned from another `Branflake`
        """
        if (branflake_int < 0) or (branflake_int > Branflake.BRANFLAKE_INT_MAX):
            raise ValueError('branflake_int: value out of range')

        all_bytes = branflake_int.to_bytes(Branflake.TOTAL_BYTES_LEN, byteorder='big', signed=False)
        return cls.from_bytes(all_bytes)

    @classmethod
    def from_hex_string(cls, branflake_hex_string):
        """Returns a new `Branflake` corresponding to a 32-character
        hexidecimal-encoded `string`.

        Args:
            branflake_hex_string: A 32-character hexidecimal-encoded `string`
            returned from another `Branflake`
        """
        if len(branflake_hex_string) != Branflake.TOTAL_BYTES_LEN * 2:
            raise ValueError('branflake_hex_string: incorrect length')

        all_bytes = b16decode(branflake_hex_string)
        return cls.from_bytes(all_bytes)

    @classmethod
    def from_base64_string(cls, branflake_base64_string: str):
        """Returns a new `Branflake` corresponding to a 22-character
        URL-safe base64-encoded `string`.

        Args:
            branflake_base64_string: A 22-character URL-safe base64-encoded `string`
            returned from another `Branflake`
        """
        if len(branflake_base64_string) < Branflake.BASE64_LEN:
            raise ValueError('branflake_base64_string: incorrect length')
        if len(branflake_base64_string) > Branflake.BASE64_PADDED_LEN:
            raise ValueError('branflake_base64_string: incorrect length')

        all_bytes = urlsafe_b64decode(
            branflake_base64_string.ljust(Branflake.BASE64_PADDED_LEN, '=')
        )
        return cls.from_bytes(all_bytes)

    @classmethod
    def from_bytes(cls, branflake_bytes):
        """Returns a new `Branflake` corresponding to a 16-byte array.

        Args:
            branflake_hex_string: A 16-byte array returned from another
            `Branflake`
        """
        if len(branflake_bytes) != Branflake.TOTAL_BYTES_LEN:
            raise ValueError('branflake_bytes: incorrect length')

        time_bytes = branflake_bytes[0:Branflake.TIME_BYTES_LEN]
        microseconds = int.from_bytes(
            time_bytes, byteorder='big', signed=False)
        random_bytes = branflake_bytes[Branflake.TIME_BYTES_LEN:Branflake.TOTAL_BYTES_LEN]
        return cls(microseconds, random_bytes)

    def to_seconds(self):
        """Returns a `float` corresponding to the epoch time in seconds
        of the Branflake."""
        return self._time / Branflake.ONE_MILLION

    def to_gmtime(self):
        """Returns a time structure corresponding to the Branflake."""
        return gmtime(self.to_seconds())

    def to_microseconds(self):
        """Returns an `int` corresponding to the epoch time in microseconds
        of the Branflake."""
        return self._time

    def get_time_bytes(self):
        """Returns an 8-byte array corresponding to the time part of the
        Branflake."""
        return self._time_bytes

    def get_random_bytes(self):
        """Returns an 8-byte array corresponding to the random part of the
        Branflake."""
        return self._random_bytes

    def to_bytes(self):
        """Returns a 16-byte array corresponding to the Branflake."""
        return self.get_time_bytes() + self.get_random_bytes()

    def to_hex_bytes(self):
        """Returns a 32-byte hexidecimal-encoded array corresponding
        to the Branflake."""
        return b16encode(self.to_bytes())

    def to_base64_bytes(self):
        """Returns a 24-byte URL-safe base64-encoded array corresponding
        to the Branflake."""
        return urlsafe_b64encode(self.to_bytes())

    def to_int(self):
        """Returns a 128-bit `int` corresponding to the Branflake."""
        return int.from_bytes(
            self.to_bytes(), byteorder='big', signed=False)

    def to_uuid(self):
        """Returns a UUID corresponding to the Branflake."""
        return UUID(bytes=self.to_bytes())

    def to_hex_string(self):
        """Returns a 32-character hexidecimal-encoded `string`
        corresponding to the Branflake."""
        return self.to_hex_bytes().decode('utf-8')

    def to_base64_string(self):
        """Returns a 22-character URL-safe base64-encoded `string`
        corresponding to the Branflake."""
        return self.to_base64_bytes().decode('utf-8')[0:Branflake.BASE64_LEN]

    def _set_time_bytes(self):
        self._time_bytes = self.to_microseconds().to_bytes(
            Branflake.TIME_BYTES_LEN, byteorder='big', signed=False)
